from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_community.utilities import GoogleSerperAPIWrapper
from langgraph.prebuilt import create_react_agent
from langchain.tools import tool
import os


load_dotenv()
llm=ChatGroq(model="llama-3.3-70b-versatile",temperature=0)
googleSearch=GoogleSerperAPIWrapper()

@tool
def google_search(query: str) -> str:
    """
    Search Google once for current/latest information.
    Return the result to the assistant so it can answer directly.
    """

    return googleSearch.run(query)


tools=[google_search]
systemInstruction ="""
You are a helpful AI assistant.
Use google_search whenever the user asks about current events, latest information,
sports scores, recent matches, live data, or facts that may have changed.
Do not answer current questions from memory.
"""
agent=create_react_agent(llm,tools,prompt=systemInstruction)
while True :
   query=input("Users :")
   if(query.lower() in ["bye","bad","quit","exit"]):
      print("bye bye")
      break 
   response=agent.invoke({"messages":[("user", query)]},config={"recursion_limit": 10})
   print("AI :",response["messages"][-1].content)  
