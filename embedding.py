import os
import time
from dotenv import load_dotenv
from pinecone import Pinecone, ServerlessSpec
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_pinecone import PineconeVectorStore

load_dotenv()

def embed_and_store(chunks):
    api_key = os.getenv("PINECONE_API_KEY")
    index_name = "multi-query-rag-index"
    
    # 1. Initialize Pinecone Client
    pc = Pinecone(api_key=api_key)
    
    # 2. Check if index exists; if not, create it
    if not pc.has_index(index_name):
        print(f"Index '{index_name}' not found. Creating new serverless index...")
        pc.create_index(
            name=index_name,
            dimension=384, # Must match 'all-MiniLM-L6-v2' dimensions
            metric="cosine",
            spec=ServerlessSpec(cloud="aws", region="us-east-1") # Recommended spec
        )
        
        # 3. Wait until the index is ready to avoid 404/403 errors
        while not pc.describe_index(index_name).status['ready']:
            time.sleep(1)
    
    # 4. Initialize Embeddings and Vector Store
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    
    vectorstore = PineconeVectorStore.from_documents(
        chunks, 
        embeddings, 
        index_name=index_name
    )
    return vectorstore