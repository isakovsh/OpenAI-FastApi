from fastapi import FastAPI
from pydantic import BaseModel
from functions import *
from dotenv import load_dotenv
from fastapi.responses import JSONResponse
from fastapi import FastAPI, File, UploadFile
import os, tempfile

app = FastAPI()
@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/query")
def query(query: str):
    vector_store = get_vector_store()
    answer = get_retrieval_qa(query,vector_store)
    return {"answer": answer}


@app.get("/web_crawler")
async def web_crawler(web_site_link: str):
    text = get_web_site(web_site_link)
    print(text)
    return {"text": text}

@app.post('/pdf')
async def pdf_to_text(file: UploadFile = File(...)):
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        temp_file.write(file.file.read())
        temp_file_path = temp_file.name
    text = get_pdf_text(temp_file_path)
    os.remove(temp_file_path)
    return JSONResponse(content={"text":text})








