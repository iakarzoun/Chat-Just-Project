from flask import Flask, request, jsonify
from dotenv import load_dotenv
import os

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_google_genai import ChatGoogleGenerativeAI

# The new Internet Search tool!
from duckduckgo_search import DDGS

load_dotenv()
app = Flask(__name__)

print("Booting up the Hybrid AI Brain... Please wait.")

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
)
vectorstore = Chroma(persist_directory="chroma_db", embedding_function=embeddings)

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash", 
    temperature=0.3,
    google_api_key=os.getenv("GEMINI_API_KEY")
)

print("✅ Hybrid Brain Loaded and Ready for Students!")

@app.route('/', methods=['GET'])
def health_check():
    return jsonify({"status": "running", "message": "Knowledge Hub is online."})

@app.route('/ask', methods=['POST'])
def process_query():
    data = request.get_json()
    if not data or 'question' not in data:
         return jsonify({"error": "No question provided"}), 400
         
    student_question = data['question']
    
    try:
        # --- 1. THE OFFLINE SEARCH (PDFs) ---
        print(f"📚 Searching PDFs for: {student_question}")
        matching_docs = vectorstore.similarity_search(student_question, k=3)
        pdf_context = "\n\n".join([doc.page_content for doc in matching_docs])
        
        # --- 2. THE ONLINE SEARCH (University Website) ---
        print("🌐 Searching the JUST website...")
        web_context = ""
        try:
            with DDGS() as ddgs:
                # We force it to ONLY search the official university website
                search_query = f"{student_question} site:just.edu.jo"
                # Grab the top 2 results from the internet
                results = list(ddgs.text(search_query, max_results=2))
                for r in results:
                    web_context += r['body'] + "\n"
        except Exception as e:
            print(f"⚠️ Web search skipped (Internet issue): {e}")

        # --- 3. COMBINE BOTH FOR GEMINI ---
        prompt = f"""
        You are a helpful university assistant for Jordan University of Science and Technology. 
        Answer the student's question using the information from the Official Handbooks and the Live Website below.
        Reply in the same language as the student's question.

        📚 Official Handbook Information (from PDFs):
        {pdf_context}

        🌐 Live Website Information (from just.edu.jo):
        {web_context}

        Student Question: 
        {student_question}
        """
        
        result = llm.invoke(prompt)
        return jsonify({"answer": result.content})
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)