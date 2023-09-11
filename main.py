from fastapi import FastAPI,Request ,Form
from pydantic import BaseModel
from functions import *
from dotenv import load_dotenv
from fastapi.responses import JSONResponse ,HTMLResponse
from fastapi import FastAPI, File, UploadFile
import os, tempfile
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

app = FastAPI()

templates = Jinja2Templates(directory='templates')
app.mount("/static",StaticFiles(directory='static'),name = 'static')

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get('/query',response_class=HTMLResponse)
async def get_basic_form(request:Request):
    return templates.TemplateResponse('basic.html',{'request':request})

@app.post("/query",response_class=HTMLResponse)
def query(request:Request,question: str = Form(...) ):
    vector_store = get_vector_store()
    answer = get_retrieval_qa(query=question,vector_store=vector_store)
    print(question)
    return templates.TemplateResponse('basic.html',{'request':request,'answer':answer[:100]})


# add web site text
@app.get('/dashboard',response_class=HTMLResponse)
async def get_basic_form(request:Request):
    return templates.TemplateResponse('dashboard.html',{'request':request})

@app.post('/dashboard')
async def add_data(request: Request, link: str = Form(...)):
    return templates.TemplateResponse('dashboard.html',{'request':request})




# add pdf text
vector_store = get_vector_store()

@app.get('/pdf', response_class=HTMLResponse)
def get_form(request: Request):
    return templates.TemplateResponse("pdf.html", {"request": request})

@app.post('/pdf', response_class=HTMLResponse)
def post_form(request: Request,file: UploadFile = File(...)):
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        temp_file.write(file.file.read())
        temp_file_path = temp_file.name
    result = add_pdf_to_vector_stor(temp_file_path,vector_store)
    os.remove(temp_file_path)
    return templates.TemplateResponse('pdf.html',{'request':request,'text':result})









