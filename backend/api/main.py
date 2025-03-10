from fastapi import FastAPI
from backend.api.routes import indexing, chatbot

app = FastAPI()

app.include_router(indexing.router, prefix="/api")
app.include_router(chatbot.router, prefix="/api")

@app.get("/")
def root():
    return {"message": "Welcome to Azure AI Search RAG Chatbot"}
