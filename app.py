import shutil, os, webbrowser, uvicorn
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from data_ingestion import load_pdf
from chunking import split_docs
from embedding import embed_and_store
from main import get_qa_chain

app = FastAPI()

# Mount the static directory to protect source code but allow access to UI assets
app.mount("/static", StaticFiles(directory="static"), name="static")

vector_store = None

@app.get("/")
async def serve_ui():
    # Ensure your HTML file matches this exact name (case-sensitive in Linux)
    return FileResponse("index.html")

@app.post("/upload")
async def handle_upload(file: UploadFile = File(...)):
    # FIX: Prepend '/tmp/' so the secure non-root user can write the file
    temp_path = f"/tmp/temp_{file.filename}"
    
    with open(temp_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    docs = load_pdf(temp_path)
    chunks = split_docs(docs)
    global vector_store
    vector_store = embed_and_store(chunks)
    
    os.remove(temp_path)
    return {"status": "Success", "message": "Knowledge Base Ready!"}

@app.post("/ask")
async def ask_question(query: str = Form(...)):
    if not vector_store:
        return {"answer": "Error: Please upload a PDF first."}
    
    qa = get_qa_chain(vector_store)
    result = qa.invoke({"query": query})
    return {"answer": result["result"]}

# Automatically open the browser when the script runs locally
if __name__ == "__main__":
    port = 8000
    uvicorn.run("app:app", host="0.0.0.0", port=port)