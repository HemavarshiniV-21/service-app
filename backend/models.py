from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class User(BaseModel):
    name: str
    email: str
    phone: Optional[str] = None
    created_at: datetime = datetime.utcnow()

class ChatMessage(BaseModel):
    user_id: Optional[str] = None
    user_message: str
    bot_response: str
    timestamp: datetime = datetime.utcnow()

class VehicleIssue(BaseModel):
    user_id: Optional[str] = None
    vehicle_make: str
    vehicle_model: str
    issue_description: str
    reported_at: datetime = datetime.utcnow()
    status: str = "open"

class ServiceRequest(BaseModel):
    user_id: Optional[str] = None
    customer_name: str
    vehicle_number: str
    mobile_number: Optional[str] = None
    km_driven: Optional[int] = None
    issue_reported: str
    vehicle_brand: str
    vehicle_model: str
    status: str = "created"
    created_date: datetime = datetime.utcnow()
    start_time: Optional[datetime] = None
    employee_id: Optional[int] = None