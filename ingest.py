import os
from dotenv import load_dotenv
from langchain_community.document_loaders import PyMuPDFLoader 
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

load_dotenv()

# 1. We just point it to the FOLDER now, not a specific file!
DOCS_DIR = "docs" 
DB_DIR = "chroma_db"

def create_database():
    print("📚 1. Scanning the docs folder for PDFs...")
    all_documents = [] # This is our giant pile of text
    
    # 2. Tell Python to loop through every single file in the folder
    for filename in os.listdir(DOCS_DIR):
        if filename.endswith(".pdf"):  # Only grab PDFs!
            pdf_path = os.path.join(DOCS_DIR, filename)
            print(f"   -> Reading: {filename}")
            
            # Read the PDF and throw its pages into our giant pile
            loader = PyMuPDFLoader(pdf_path)
            documents = loader.load()
            all_documents.extend(documents) 
            
    # Safety check in case the folder is empty
    if len(all_documents) == 0:
        print("❌ Error: No PDFs found in the docs folder!")
        return
    
    print("✂️ 2. Chopping all the text into small chunks...")
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    # We slice up the giant pile of documents all at once
    chunks = text_splitter.split_documents(all_documents)
    print(f"   Created {len(chunks)} chunks of text from all your PDFs.")

    print("🧠 3. Saving everything to the Database...")
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
    )
    
    # Save it!
    Chroma.from_documents(
        documents=chunks, 
        embedding=embeddings, 
        persist_directory=DB_DIR
    )
    
    print("✅ Success! The free database is ready and contains ALL your PDFs.")

if __name__ == "__main__":
    create_database()