from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ChatRequest(BaseModel):
    user_id: Optional[str] = None
    message: str

class ChatResponse(BaseModel):
    response: str
    timestamp: datetime

class ChatHistory(BaseModel):
    user_id: Optional[str] = None
    user_message: str
    bot_response: str
    timestamp: datetime

class ServiceRequestCreate(BaseModel):
    customer_name: str
    vehicle_number: str
    mobile_number: Optional[str] = None
    km_driven: Optional[int] = None
    issue_reported: str
    vehicle_brand: str
    vehicle_model: str

class ServiceRequestResponse(BaseModel):
    id: str
    customer_name: str
    vehicle_number: str
    issue_reported: str
    status: str
    created_date: datetime