from langchain.tools import tool
from database import service_requests_collection, vehicle_issues_collection
from datetime import datetime

@tool
def get_total_service_requests():
    """Return total number of service requests"""
    count = service_requests_collection.count_documents({})
    return f"Total service requests: {count}"

@tool
def create_service_request(customer_name: str, vehicle_number: str, issue: str, vehicle_brand: str, vehicle_model: str):
    """Create a new service request"""
    doc = {
        "customer_name": customer_name,
        "vehicle_number": vehicle_number,
        "issue_reported": issue,
        "vehicle_brand": vehicle_brand,
        "vehicle_model": vehicle_model,
        "status": "created",
        "created_date": datetime.utcnow()
    }
    result = service_requests_collection.insert_one(doc)
    return "Service request created successfully"

@tool
def report_vehicle_issue(vehicle_make: str, vehicle_model: str, issue_description: str):
    """Report a vehicle issue for analysis"""
    doc = {
        "vehicle_make": vehicle_make,
        "vehicle_model": vehicle_model,
        "issue_description": issue_description,
        "reported_at": datetime.utcnow(),
        "status": "open"
    }
    result = vehicle_issues_collection.insert_one(doc)
    return "Vehicle issue reported successfully"

@tool
def get_vehicle_maintenance_tips(vehicle_type: str):
    """Get maintenance tips for a specific vehicle type"""
    tips = {
        "car": "Regular oil changes, tire rotations, brake inspections",
        "bike": "Chain lubrication, tire pressure checks, brake pad inspection",
        "electric": "Battery health monitoring, software updates, tire maintenance"
    }
    return tips.get(vehicle_type.lower(), "General maintenance: regular servicing, fluid checks, tire care")

@tool
def estimate_repair_cost(issue: str, vehicle_type: str):
    """Estimate repair cost based on issue and vehicle type"""
    estimates = {
        "brake pads": {"car": 2000, "bike": 500},
        "oil change": {"car": 500, "bike": 200},
        "battery": {"car": 3000, "bike": 1000},
        "tire": {"car": 1500, "bike": 400}
    }
    issue_lower = issue.lower()
    for key in estimates:
        if key in issue_lower:
            cost = estimates[key].get(vehicle_type.lower(), 1000)
            return f"Estimated cost for {issue}: ₹{cost}"
    return "Cost estimation requires specific details. Please provide more information."