import os
from dotenv import load_dotenv # Import the dotenv loader
from langchain_groq import ChatGroq
from langchain_classic.chains import RetrievalQA
from langchain_core.prompts import PromptTemplate

# 1. Load the environment variables from the .env file
# This looks for a file named '.env' in the same directory
load_dotenv()

# 2. Retrieve the keys (make sure these match the names in your .env)
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

def get_qa_chain(vectorstore):
    # Pass the API key directly or ensure it's in the environment
    llm = ChatGroq(
         model="openai/gpt-oss-20b",
        temperature=0,
        groq_api_key=GROQ_API_KEY # Explicitly passing the key
    )
    
    template = """Use the following context to answer the question.
    Context: {context}
    Question: {question}
    Answer:"""
    
    return RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=vectorstore.as_retriever(),
        chain_type_kwargs={"prompt": PromptTemplate.from_template(template)}
    )