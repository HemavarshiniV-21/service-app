from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from database import db, chat_history_collection, service_requests_collection
from chatbot.agent import chat_agent
from schemas import ChatRequest, ChatResponse, ChatHistory, ServiceRequestCreate, ServiceRequestResponse
from datetime import datetime
import uuid
from routers.jobs import router as service_router

app = FastAPI(title="Vehicle Service Chatbot API")

# Allow local frontend dev server to call this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173", "http://localhost:5174", "http://127.0.0.1:5174"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if db is None:
    raise RuntimeError("Database connection failed. Please check MongoDB URI.")

app.include_router(service_router)

@app.get("/")
def home():
    return {"message": "Vehicle Service AI Chatbot Running"}

@app.post("/chat")
def chat(request: ChatRequest):
    try:
        response = chat_agent(request.message, request.user_id)
        timestamp = datetime.utcnow()
        
        # Store in MongoDB
        chat_doc = {
            "user_id": request.user_id,
            "user_message": request.message,
            "bot_response": response,
            "timestamp": timestamp
        }
        chat_history_collection.insert_one(chat_doc)
        
        return {"chatbot_reply": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/history", response_model=list[ChatHistory])
def get_history(user_id: str = None, limit: int = 50):
    try:
        query = {}
        if user_id:
            query["user_id"] = user_id
        
        chats = list(chat_history_collection.find(query).sort("timestamp", -1).limit(limit))
        return [
            ChatHistory(
                user_id=chat.get("user_id"),
                user_message=chat["user_message"],
                bot_response=chat["bot_response"],
                timestamp=chat["timestamp"]
            ) for chat in chats
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/service-request", response_model=ServiceRequestResponse)
def create_service_request(request: ServiceRequestCreate):
    try:
        doc = request.dict()
        doc["id"] = str(uuid.uuid4())
        doc["created_date"] = datetime.utcnow()
        doc["status"] = "created"
        
        result = service_requests_collection.insert_one(doc)
        
        return ServiceRequestResponse(
            id=doc["id"],
            customer_name=doc["customer_name"],
            vehicle_number=doc["vehicle_number"],
            issue_reported=doc["issue_reported"],
            status=doc["status"],
            created_date=doc["created_date"]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))