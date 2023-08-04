from dotenv import load_dotenv
import streamlit as st
from langchain.chains import RetrievalQA
from langchain.llms import OpenAI
from langchain.vectorstores import Qdrant
from langchain.embeddings.openai import OpenAIEmbeddings
import qdrant_client
import os
import openai
from pypdf import PyPDFLoader
from langchain.text_splitter import CharacterTextSplitter
import re
load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")
def get_vector_store():
  client = qdrant_client.QdrantClient(
        os.getenv("QDRANT_HOST"),
        api_key=os.getenv("QDRANT_API_KEY")
    )
    
  embeddings = OpenAIEmbeddings()

  vector_store = Qdrant(
        client=client, 
        collection_name=os.getenv("QDRANT_COLLECTION_NAME"), 
        embeddings=embeddings,
    )
    
  return vector_store

def get_retrieval_qa(query,vector_store):
  qa = RetrievalQA.from_chain_type(
        llm=OpenAI(),
        chain_type="stuff",
        retriever=vector_store.as_retriever()
    )
  answer = qa.run(query)
  return answer

def get_pdf_text(file):
  loader = PyPDFLoader(file)
  docs = loader.load()
  text = ""
  for i in range(len(docs)):
    text += docs[i].page_content
  text = re.sub('\n','',text)
  return text

def get_chunks(text):
  splitter = CharacterTextSplitter(
      separator = "\n",
      chunk_size = 1000,
      chunk_overlap = 200,
      length_function = len
  )

def add_pdf_to_vector_stor(file,vector_store):
    
  # get text from pdf file
  loader = PyPDFLoader(file)
  docs = loader.load()
  text = ""
  for i in range(len(docs)):
    text += docs[i].page_content
  text = re.sub('\n','',text)

  # create chunks
  splitter = CharacterTextSplitter(
       separator='\n',
       chunk_size =1000,
       chunk_overlap = 200,
       length_function = len
    )
  text = splitter.split_text(text)

  # add text chunks to vector store
  vector_store.add_texts(text)

  return True




      
