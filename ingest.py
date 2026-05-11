import os
from dotenv import load_dotenv
from langchain_community.document_loaders import PyMuPDFLoader 
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

load_dotenv()

DOCS_DIR = "docs" 
DB_DIR = "chroma_db"

def create_database():
    print("📚 1. Scanning ALL folders and sub-folders for PDFs...")
    all_documents = [] 
    
    for folder_path, subfolders, files in os.walk(DOCS_DIR):
        for filename in files:
            if filename.endswith(".pdf"):
                pdf_path = os.path.join(folder_path, filename)
                print(f"   -> Reading: {filename} (found in {folder_path})")
                try:
                    loader = PyMuPDFLoader(pdf_path)
                    documents = loader.load()
                    all_documents.extend(documents)
                except Exception as e:
                    print(f"      ❌ Skipping {filename} due to an error: {e}")
            
    if len(all_documents) == 0:
        print("❌ Error: No PDFs found anywhere in the docs folders!")
        return
    
    print(f"✂️ 2. Chopping all {len(all_documents)} pages of text into small chunks...")
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = text_splitter.split_documents(all_documents)
    print(f"   Created {len(chunks)} chunks of text from all your PDFs.")

    print("🧠 3. Saving everything to the Database...")
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
    )
    
    Chroma.from_documents(
        documents=chunks, 
        embedding=embeddings, 
        persist_directory=DB_DIR
    )
    
    print("✅ Success! The free database is ready and contains ALL your PDFs.")

if __name__ == "__main__":
    create_database()