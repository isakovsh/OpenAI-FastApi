from fastapi import FastAPI, Request , UploadFile ,File
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import os, tempfile
from functions import *

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

@app.get('/dashboard',response_class=HTMLResponse)
async def get_basic_form(request:Request):
    return templates.TemplateResponse('dashboard.html',{'request':request})

@app.post('/dashboard', response_class=HTMLResponse)
async def add_data(request: Request):

    upload_files = await request.form()
    requested_file = upload_files.get('file', None)
    
    if requested_file.filename:
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_file.write(await requested_file.read())
            temp_file_path = temp_file.name
        
        result = add_pdf_to_vector_stor(temp_file_path)
        os.remove(temp_file_path)
        return templates.TemplateResponse(
                "result.html",
                {"request": request, "text": result}
        )
    return templates.TemplateResponse('dashboard.html',{'request':request})






@app.get('/chat',response_class=HTMLResponse)
async def get_basics_form(request:Request):
    return templates.TemplateResponse('chat.html',{'request':request})


@app.post('/chat',response_class=HTMLResponse)
async def get_basicz_form(request:Request):
    question = await request.form()
    question = question.get('question', None)
    print(question)
    answer = qa(question)


    return templates.TemplateResponse('chat.html',{'request':request,'answer':answer})


