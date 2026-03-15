# Vehicle Service AI Chatbot

A comprehensive AI-powered chatbot for vehicle service assistance using Python, FastAPI, LangChain, OpenAI, and MongoDB.

## Features

- Intelligent vehicle-related Q&A covering buying, selling, repairs, maintenance, etc.
- RAG (Retrieval-Augmented Generation) using vehicle manuals and knowledge base
- Chat history storage in MongoDB
- Service request management
- Vehicle issue reporting
- Maintenance tips and repair cost estimation
- Modular architecture with tools and agents

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set up MongoDB:
- Install MongoDB locally or use MongoDB Atlas
- Update MONGODB_URI in .env file

3. Set up environment variables in .env:
```
OPENAI_API_KEY=your-openai-api-key
MONGODB_URI=mongodb://localhost:27017/
```

4. Run the application:
```bash
uvicorn main:app --reload
```

## API Endpoints

- `GET /` - API status
- `POST /chat` - Send chat message
- `GET /history` - Get chat history
- `POST /service-requests/` - Create service request
- `GET /service-requests/` - Get service requests

## Usage

### Chat API
```python
import requests

response = requests.post("http://localhost:8000/chat", json={
    "message": "What are the maintenance tips for my car?",
    "user_id": "user123"  # optional
})
print(response.json())
```

### Get Chat History
```python
response = requests.get("http://localhost:8000/history?user_id=user123&limit=10")
print(response.json())
```

## Project Structure

```
├── main.py                 # FastAPI application
├── database.py             # MongoDB connection
├── models.py               # Pydantic models
├── schemas.py              # API schemas
├── chatbot/
│   ├── agent.py           # LangChain agent with tools
│   ├── rag.py             # RAG system
│   └── tools.py           # Custom tools
├── routers/
│   └── jobs.py            # Service request routes
├── data/
│   └── service_docs.txt   # Knowledge base
├── requirements.txt        # Dependencies
└── .env                    # Environment variables
```

## Technologies Used

- **FastAPI**: Web framework
- **LangChain**: AI agent framework
- **OpenAI GPT-4**: Language model
- **MongoDB**: Database
- **FAISS**: Vector search for RAG
- **Pydantic**: Data validation