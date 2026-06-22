from flask import Flask, request, jsonify
from dotenv import load_dotenv
import os

from langchain_community.document_loaders import PyMuPDFLoader 
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_google_genai import ChatGoogleGenerativeAI
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

print("Hybrid Brain Loaded and Ready for Students!")

@app.route('/', methods=['GET'])
def health_check():
    return jsonify({"status": "running", "message": "Knowledge Hub is online."})

@app.route('/ask', methods=['POST'])
def process_query():
    data = request.get_json()
    if not data or 'question' not in data:
         return jsonify({"error": "No question provided"}), 400
         
    student_question = data['question']
    # 1. Catch the history list (or use an empty list if it's the very first question)
    chat_history = data.get('history', []) 
    
    try:
        print(f"Searching PDFs for: {student_question}")
        matching_docs = vectorstore.similarity_search(student_question, k=3)
        pdf_context = "\n\n".join([doc.page_content for doc in matching_docs])
        
        print("Searching the JUST website...")
        web_context = ""
        try:
            with DDGS() as ddgs:
                search_query = f"{student_question} site:just.edu.jo"
                results = list(ddgs.text(search_query, max_results=2))
                for r in results:
                    web_context += r['body'] + "\n"
        except Exception as e:
            print(f"Web search skipped (Internet issue): {e}")

        # 2. Format the history into a readable transcript for Gemini
        transcript = ""
        for msg in chat_history:
            # .get() prevents crashes. It looks for 'user', but if it can't find it, 
            # it safely falls back to looking for 'question', or just prints "Student"
            student_text = msg.get('user', msg.get('question', 'Student'))
            ai_text = msg.get('ai', msg.get('answer', 'Assistant'))
            
            transcript += f"Student: {student_text}\nAssistant: {ai_text}\n"
        # 3. Inject the transcript into the final prompt
        prompt = f"""
        You are a helpful university assistant for Jordan University of Science and Technology. 
        Answer the student's question using the information from the Official Handbooks and the Live Website below.
        And if there is a question that you don't know the unswer for it, tell them that and recommend something to help them finding the unswer.
        Reply in the same language as the student's question.

        Previous Conversation Context:
        {transcript}

        Official Handbook Information (from PDFs):
        {pdf_context}

        Live Website Information (from just.edu.jo):
        {web_context}

        Student's New Question: 
        {student_question}
        """
        
        result = llm.invoke(prompt)
        return jsonify({"answer": result.content})
        
    except Exception as e:
        print(f"\n CRITICAL CRASH: {str(e)}\n")
        return jsonify({"error": str(e)}), 500

@app.route('/admin/documents', methods=['GET'])
def list_documents():
    # 1. The Security Check (The Bouncer)
    provided_key = request.headers.get('X-Admin-Key')
    actual_admin_key = os.getenv("ADMIN_SECRET_KEY")
    
    # If they didn't send a key, or sent the wrong one, kick them out!
    if not provided_key or provided_key != actual_admin_key:
        return jsonify({"error": "Unauthorized. Admin access only."}), 403 

    # 2. If they pass the check, gather the files
    docs_folder = "docs" 
    
    try:
        pdf_files = []
        for folder_path, subfolders, files in os.walk(docs_folder):
            for filename in files:
                if filename.endswith(".pdf"):
                    pdf_files.append(filename)
                    
        return jsonify({"documents": pdf_files}), 200
        
    except Exception as e:
        print(f"\n❌ Error reading documents: {str(e)}\n")
        return jsonify({"error": "Could not load documents."}), 500

@app.route('/admin/documents', methods=['POST'])
def upload_document():
    # 1. The Security Check
    provided_key = request.headers.get('X-Admin-Key')
    if not provided_key or provided_key != os.getenv("ADMIN_SECRET_KEY"):
        return jsonify({"error": "Unauthorized."}), 403

    # 2. Catch the file sent by Flutter
    if 'file' not in request.files:
        return jsonify({"error": "No file part in the request"}), 400
        
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    # 3. Save it to the hard drive (The Shelf)
    if file and file.filename.endswith('.pdf'):
        file_path = os.path.join("docs", file.filename)
        file.save(file_path)
        
        try:
            print(f"New file uploaded: {file.filename}. Injecting into AI Brain...")
            
            # 4. Read the new PDF
            loader = PyMuPDFLoader(file_path)
            new_docs = loader.load()
            
            # 5. Chop it into chunks (using the exact same rules as ingest.py)
            text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
            new_chunks = text_splitter.split_documents(new_docs)
            
            # 6. Inject the numbers directly into the live database!
            vectorstore.add_documents(new_chunks)
            
            print(f"Success! {file.filename} is now permanently memorized.")
            return jsonify({"message": f"Successfully uploaded and memorized {file.filename}!"}), 200
            
        except Exception as e:
            print(f"Error processing PDF for AI: {e}")
            return jsonify({"error": f"Saved the file, but failed to process AI memory: {str(e)}"}), 500
            
    return jsonify({"error": "Only PDF files are allowed."}), 400

@app.route('/admin/documents/<filename>', methods=['DELETE'])
def delete_document(filename):
    # 1. The Security Check
    provided_key = request.headers.get('X-Admin-Key')
    actual_admin_key = os.getenv("ADMIN_SECRET_KEY")
    
    if not provided_key or provided_key != actual_admin_key:
        return jsonify({"error": "Unauthorized. Admin access only."}), 403

    # 2. Hunt for the file inside the docs folder (and sub-folders)
    docs_folder = "docs"
    file_to_delete = None
    
    for folder_path, subfolders, files in os.walk(docs_folder):
        if filename in files:
            file_to_delete = os.path.join(folder_path, filename)
            break # Stop searching once we find it!

    # 3. Delete the file
    if file_to_delete and os.path.exists(file_to_delete):
        try:
            os.remove(file_to_delete)
            return jsonify({"message": f"Successfully deleted {filename}"}), 200
        except Exception as e:
            return jsonify({"error": f"Failed to delete file: {str(e)}"}), 500
    else:
        return jsonify({"error": "File not found on the server."}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True, port=5000)