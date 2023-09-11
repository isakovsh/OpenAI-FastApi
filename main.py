from fastapi import FastAPI

app = FastAPI()

@app.post("/query")
async def query(question: str):
    qa = RetrievalQA.from_chain_type(llm=OpenAI(), chain_type="stuff", retriever=vectorstore.as_retriever()) 
    result = qa.run(question)
    return {"reult":result}