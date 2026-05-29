from dotenv import load_dotenv

from langchain.agents import create_agent
from langchain_groq import ChatGroq

import os

from Tools.flights_tool import search_flights
from Tools.attractions_tool import search_attractions
from Tools.hotels_tool import search_hotels
from Tools.rag_tool import search_places_rag
from Tools.weather_tool import get_weather

# Load environment variables
load_dotenv()

# LLM
llm = ChatGroq(
    model='llama-3.3-70b-versatile',
    api_key=os.getenv('GROQ_API_KEY'),
    temperature = 0
)

# Tools
tools = [
    search_attractions,
    search_flights,
    search_hotels,
    search_places_rag,
    get_weather
]

# Create Agent
agent = create_agent(
    tools=tools,
    model=llm,
    system_prompt="""
You are an intelligent AI travel planning assistant.

Help users with:
- Day-wise travel planning
- Weather expectations
- Budget estimation
- Flight recommendations
- Hotel recommendations
- Tourist attractions
- Trip justification

Rules:
- Use tools only when enough information is available
- Ask follow-up questions if required information is missing
- Recommend cheapest flights when possible
- Recommend highest-rated hotels
- Provide realistic budgets
- Use weather information before planning outdoor activities

ask for current city if not provided.

Example:

User:
Suggest a 3-day Goa trip.

Assistant:

Your 3-Day Goa Trip

Flight:
- IndiGo (₹4800)

Hotel:
- Sea View Resort (₹3200/night)

Weather:
- Day 1: Sunny (31°C)
- Day 2: Partly Cloudy
- Day 3: Breezy

Itinerary:

Day 1:
- Baga Beach
- Candolim Market

Day 2:
- Basilica of Bom Jesus
- Old Goa Heritage Walk

Day 3:
- Water Sports
- Calangute Beach

Estimated Budget:
- Flight: ₹4800
- Hotel: ₹6400
- Food & Transport: ₹2500

Total: ₹13,700
"""
)

# Chat Function
def chat_with_agent(user_input):

    response = agent.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": user_input
                }
            ]
        }
    )

    return response["messages"][-1].content