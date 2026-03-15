from fastapi import APIRouter, HTTPException
from database import service_requests_collection
from schemas import ServiceRequestCreate, ServiceRequestResponse
from datetime import datetime
import uuid

router = APIRouter(prefix="/service-requests", tags=["Service Requests"])

@router.post("/", response_model=ServiceRequestResponse)
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

@router.get("/")
def get_service_requests(limit: int = 50):
    try:
        requests = list(service_requests_collection.find().sort("created_date", -1).limit(limit))
        return requests
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))