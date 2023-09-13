from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi import FastAPI, File, UploadFile
import os, tempfile

from functions import *

app = FastAPI()

@app.get("/")
async def root():
    return {"Projet healthy"}

@app.post("/query")
async def query(question: str):
    result = qa(question)
    return result
    

@app.post('/pdf')
async def pdf_to_text(file: UploadFile = File(...)):
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        temp_file.write(file.file.read())
        temp_file_path = temp_file.name
    result = add_pdf_to_vector_stor(temp_file_path)
    os.remove(temp_file_path)
    return result