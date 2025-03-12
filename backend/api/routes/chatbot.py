from fastapi import APIRouter, FastAPI
from backend.services.chatbot_service import handle_query, generate_llm_response

router = APIRouter()
app = FastAPI()

  

@router.post("/chat-llm")
def chat_with_llm(user_query: str):
    """Handle user queries with integrated expense categorization and vendor detection"""
    documents = handle_query(user_query) 
    if not documents:
        return {"answer": "I couldn't find relevant information."}

    answer = generate_llm_response(user_query, documents)
    return {"answer": answer}
