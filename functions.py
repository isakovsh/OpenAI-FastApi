from langchain.chains import RetrievalQA
from langchain.llms import OpenAI
from langchain.vectorstores import Qdrant
from langchain.embeddings.openai import OpenAIEmbeddings
import qdrant_client
import os
import openai
from dotenv import load_dotenv
from fastapi import FastAPI



load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

client = qdrant_client.QdrantClient(
    os.getenv("QDRANT_HOST"),
    api_key = os.getenv("QDRANT_API_KEY")
)

embeddings = OpenAIEmbeddings()

vectorstore = Qdrant(
        client=client,
        collection_name=os.getenv("QDRANT_COLLECTION_NAME"),
        embeddings=embeddings
    )

llm = OpenAI()
qa_chain = RetrievalQA.from_chain_type(
    llm,
    retriever=vectorstore.as_retriever()
)

# question = input("Query:")
qa = RetrievalQA.from_chain_type(llm=OpenAI(openai_api_key=""), chain_type="stuff", retriever=vectorstore.as_retriever()) 
