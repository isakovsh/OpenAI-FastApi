from dotenv import load_dotenv
from langchain import PromptTemplate
from langchain.chains import RetrievalQA
from langchain.llms import OpenAI
from langchain.vectorstores import Qdrant
from langchain.embeddings.openai import OpenAIEmbeddings
import qdrant_client
import os
import openai
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import CharacterTextSplitter
import re
from langchain.document_loaders import WebBaseLoader
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
        llm=OpenAI(max_tokens=100),
        chain_type="stuff",
        retriever=vector_store.as_retriever(),
        
    )
  answer = qa.run(query)
  return answer


def get_pdf_text(file):
  loader = PyPDFLoader(file)
  docs = loader.load()
  text = " ".join(docs[i].page_content for i in range(len(docs)))
  text = re.sub('\n','',text)
  return text

def add_pdf_to_vector_stor(file,vector_store):
    
  # get text from pdf file
  loader = PyPDFLoader(file)
  docs = loader.load()
  text = " ".join(docs[i].page_content for i in range(len(docs)))
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

def get_web_site(web_site_link):
  loader = WebBaseLoader(web_site_link)
  docs = loader.load()
  text = " ".join(docs[i].page_content for i in range(len(docs)))
  text = re.sub('\n','',text)
  return text
   