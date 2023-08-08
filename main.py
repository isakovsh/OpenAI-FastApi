from fastapi import FastAPI
from pydantic import BaseModel
from functions import *
from dotenv import load_dotenv
from typing import Annotated
from fastapi import FastAPI, File, UploadFile


app = FastAPI()
@app.get("/")
def read_root():
    return {"Hello": "World"}

# @app.post("/query")
# def query(query: str):
#     vector_store = get_vector_store()
#     answer = get_retrieval_qa(query,vector_store)
#     return {"answer": answer}


@app.get("web_crawler")
async def web_crawler(web_site_link: str):
    text = get_web_site(web_site_link)
    print(text)
    return {"text": text}








