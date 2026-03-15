import requests

# Test the API
base_url = "http://localhost:8000"

# Test home endpoint
response = requests.get(f"{base_url}/")
print("Home:", response.json())

# Test chat endpoint
response = requests.post(f"{base_url}/chat", json={"message": "What are the maintenance tips for my car?"})
print("Chat:", response.json())