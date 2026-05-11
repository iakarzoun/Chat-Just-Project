from flask import Flask, request, jsonify
from dotenv import load_dotenv
import os

# The AI tools (Notice we deleted the broken .chains import!)
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_google_genai import ChatGoogleGenerativeAI

# 1. Load the secret keys
load_dotenv()

app = Flask(__name__)

print("Booting up the AI Brain... Please wait.")

# 2. Load the EXACT SAME free Arabic math model
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
)

# 3. Connect to the Chroma Database
vectorstore = Chroma(persist_directory="chroma_db", embedding_function=embeddings)

# 4. Hire the Gemini Waiter
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash", 
    temperature=0.3,
    google_api_key=os.getenv("GEMINI_API_KEY")
)

print("✅ AI Brain Loaded and Ready for Students!")

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
        # --- THE CUSTOM RAG PROCESS (Bulletproof) ---
        
        # Step 1: Search the Chroma database for the 3 most relevant paragraphs
        print(f" Searching database for: {student_question}")
        matching_docs = vectorstore.similarity_search(student_question, k=3)
        
        # Step 2: Glue those 3 paragraphs together into one big text string
        context_text = "\n\n".join([doc.page_content for doc in matching_docs])
        
        # Step 3: Write the strict instructions for Gemini
        prompt = f"""
        You are a helpful university assistant. Answer the student's question using ONLY the information provided in the context below.
        If the answer is not in the context, politely say that you don't know based on the handbook.
        Reply in the same language as the question.

        Context:
        {context_text}

        Student Question: 
        {student_question}
        """
        
        # Step 4: Send the combined prompt directly to Gemini!
        result = llm.invoke(prompt)
        
        # Return Gemini's text response
        return jsonify({"answer": result.content})
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)