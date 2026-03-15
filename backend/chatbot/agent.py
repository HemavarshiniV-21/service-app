from dotenv import load_dotenv
import os
from langchain_openai import ChatOpenAI
from chatbot.rag import retriever, get_retriever
from chatbot.tools import get_total_service_requests, create_service_request, report_vehicle_issue, get_vehicle_maintenance_tips, estimate_repair_cost

load_dotenv()

llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0
)

system_prompt = """You are an expert vehicle service assistant. You help users with vehicle buying advice, repair troubleshooting, mechanical faults, maintenance tips, selling advice, and vehicle comparisons. Provide clear explanations and step-by-step solutions when diagnosing problems.

Always be helpful, professional, and provide detailed responses."""

def chat_agent(query: str, user_id: str = None):
    try:
        # Get context from RAG if available
        if retriever:
            docs = retriever.get_relevant_documents(query)
            context = "\n".join([doc.page_content for doc in docs])
        else:
            context = ""
        
        prompt = f"{system_prompt}\n\nContext: {context}\n\nQuestion: {query}\n\nAnswer:"
        response = llm.invoke(prompt).content
        
        return response
    except Exception as e:
        # Fallback response if OpenAI fails - provide helpful vehicle service advice
        query_lower = query.lower()
        
        if "sell" in query_lower or "selling" in query_lower:
            return "To sell your car, first check its market value using tools like Kelley Blue Book or Edmunds. Clean the car thoroughly, get a pre-sale inspection, and consider having it detailed. Price competitively based on condition, mileage, and local market. Be prepared to negotiate and have all paperwork ready including title, maintenance records, and bill of sale."
        
        elif "buy" in query_lower or "buying" in query_lower:
            return "When buying a car, research reliability ratings, read reviews, and check maintenance costs. Get a pre-purchase inspection from a trusted mechanic. Compare prices across multiple dealers, consider certified pre-owned options, and don't forget to factor in insurance, fuel efficiency, and financing terms."
        
        elif "repair" in query_lower or "repairs" in query_lower:
            return "For car repairs, start by diagnosing the problem - check engine lights, unusual noises, or performance issues. Get quotes from multiple reputable shops. For major repairs, consider the vehicle's age and mileage. Always keep records of all maintenance and repairs."
        
        elif "maintenance" in query_lower or "service" in query_lower:
            return "Regular maintenance includes oil changes every 5,000-7,500 miles, tire rotations every 5,000 miles, brake inspections, and following your manufacturer's recommended service schedule. Keep detailed records and address issues promptly to avoid costly repairs."
        
        elif "engine" in query_lower or "engine problem" in query_lower:
            return "Engine problems can range from minor issues like low oil to major failures. Common signs include unusual noises, reduced power, poor fuel economy, or warning lights. Don't drive if you suspect serious issues - have it towed to a mechanic for diagnosis."
        
        else:
            return "I'm here to help with vehicle buying, selling, repairs, maintenance, and troubleshooting. Could you please provide more details about your question? For example, are you asking about buying a car, selling one, or dealing with a specific repair issue?"
