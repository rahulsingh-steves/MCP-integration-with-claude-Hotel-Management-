from http import client
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain.agents import create_agent
import os
import asyncio


from langchain_groq import ChatGroq

from dotenv import load_dotenv
load_dotenv()

os.environ["GROQ_API_KEY"]=os.getenv("GROQ_API_KEY")

async def create_client():
    client= MultiServerMCPClient(
        {"hotel_management_system":{
            "Command":"python",
            "args":["server.py"],
            "transport":"stdio"
        }}
        )
    
    
    
    try:
        tools=await client.get_tools("Hotel_Management_System")
        model=ChatGroq(model="moonshotai/kimi-k2-instruct-0905",temperature=0)
        agent=create_agent(
            model,
            tools
        )
    except Exception as e:
        print("Error creating client:",e)
        
    