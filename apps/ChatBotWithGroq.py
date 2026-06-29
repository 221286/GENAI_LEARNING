#llm
#Tool- google Search Tool
#Agents
#Memory
#Streaming
#web Interface
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langgraph.prebuilt import create_react_agent
from langchain_community.utilities import GoogleSerperAPIWrapper
from langchain.tools import tool
from langgraph.checkpoint.memory import MemorySaver
import streamlit as st

load_dotenv()
llm=ChatGroq(model="llama-3.3-70b-versatile" ,streaming=True,temperature=0)
googleSearch=GoogleSerperAPIWrapper()
# memory=MemorySaver()
if "memory" not in st.session_state:
  st.session_state.memory=MemorySaver()
  st.session_state.history=[]

st.subheader("QuickAnswers - Answers at the speed of throught")

for messages in st.session_state.history:
    role=messages["role"]
    content = messages["content"]
    st.chat_message(role).markdown(content)



@tool
def google_search(query:str)->str:
     """
    Search Google once for current/latest information.
    Return the result to the assistant so it can answer directly.
    """
     return googleSearch.run(query)

tools=[google_search]
systemPrompt="""Think like a java developer 4 years of experience
"""
agent=create_react_agent(llm,tools,prompt=systemPrompt,checkpointer=st.session_state.memory)

query=st.chat_input("Ask me anything")

if query:
     st.chat_message("user").markdown(query)
     st.session_state.history.append({"role":"user","content":query})
     response= agent.invoke({"messages":[query]},
                            config={"recursion_limit": 10,"configurable":{"thread_id": "1"}},
                            stream_mode="messages")
     withAiContainer=st.chat_message("ai")
     with withAiContainer:
         space=st.empty()

         messages=""

         for chunk in response:
             messages=messages+chunk[0].content
             space.write(messages)
             
         st.session_state.history.append({"role":"ai","content":messages})


    #  st.chat_message("ai").markdown(response["messages"][-1].content)


# while True:
#      query=input("User :")
#      if query.lower() in ["bye","bad","quit","exit"]:
#           print("bye bye all")
#           break
#      response= agent.invoke({"messages":[query]},config={"recursion_limit": 10,"configurable":{"thread_id": "1"}})
#      print("AI :",response["messages"][-1].content)
