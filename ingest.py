import os
from dotenv import load_dotenv
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma

# 1. Load the secret API key
load_dotenv()

# 2. Tell the system where the PDF is
# CHANGE 'handbook.pdf' to the actual name of your file!
PDF_PATH = "docs/calendar_seconed_semester_2025-2026.pdf" 
DB_DIR = "chroma_db" # This is the folder where the database will be saved

def create_database():
    print("1. Loading the PDF...")
    loader = PyMuPDFLoader(PDF_PATH)
    documents = loader.load()

    print(documents[0].page_content[:500]) # this line just to test the Arabic text
    
    print(" 2. Chopping the text into small chunks...")
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500, # 500 characters per chunk
        chunk_overlap=50  # Overlap slightly so sentences don't break in half
    )
    chunks = text_splitter.split_documents(documents)
    print(f"   Created {len(chunks)} chunks of text.")

    print("3. Converting text to vectors and saving to ChromaDB...")
    # This uses OpenAI to turn the text into math
    embeddings = OpenAIEmbeddings()
    
    # This creates the actual database folder on your computer
    Chroma.from_documents(
        documents=chunks, 
        embedding=embeddings, 
        persist_directory=DB_DIR
    )
    
    print("Success! The knowledge base has been created.")

if __name__ == "__main__":
    create_database()