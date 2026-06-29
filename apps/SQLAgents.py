from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langgraph.prebuilt import create_react_agent
from langchain.tools import tool
from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import create_react_agent
import streamlit as st
load_dotenv()

#llm,tools,memory
sql=SQLDatabase.from_uri("sqlite:///mytask.db")
llm=ChatGroq(model="llama-3.3-70b-versatile" ,streaming=True,temperature=0)
memory=MemorySaver()

sql.run("""
CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    description TEXT,
    status TEXT DEFAULT 'pending' CHECK (status IN ('pending', 'in_progress', 'completed')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
""")
SQLtool=SQLDatabaseToolkit(db=sql,llm=llm)
tools=SQLtool.get_tools()
system_prompt = """
You are a task management assistant that interacts with a SQL database containing a 'tasks' table. 

TASK RULES:
1. Limit SELECT queries to 10 results max with ORDER BY created_at DESC
2. After CREATE/UPDATE/DELETE, confirm with SELECT query
3. If the user requests a list of tasks, present the output in a structured table format to ensure a clean and organized display in the browser."

CRUD OPERATIONS:
    CREATE: INSERT INTO tasks(title, description, status)
    READ: SELECT * FROM tasks WHERE ... LIMIT 10
    UPDATE: UPDATE tasks SET status=? WHERE id=? OR title=?
    DELETE: DELETE FROM tasks WHERE id=? OR title=?

Table schema: id, title, description, status(pending/in_progress/completed), created_at.
"""

st.subheader("TaskBot : Manage your tools")
if "memory" not in st.session_state:
    st.session_state.memory=MemorySaver()
    st.session_state.history=[]

for msg in st.session_state.history:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

agent=create_react_agent(llm,tools,prompt=system_prompt,checkpointer=st.session_state.memory)
query=st.chat_input("Shoot your query")

if query:
    st.chat_message("user").markdown(query)
    st.session_state.history.append({"role":"user","content":query})
    response=agent.invoke({
        "messages":[{"role":"user","content":query}]},config={
            "recursion_limit":10,"configurable":{
                "thread_id":"1"
            }
        },stream_mode="messages")
    withAIcontainer=st.chat_message("ai")
    with withAIcontainer:
        space=st.empty()
        messages=""
        for chunk in response:
            messages=messages+chunk[0].content
            space.write(messages)
        
    st.session_state.history.append({"role":"ai","content":messages})
   
    # st.chat_message("ai").markdown(response["messages"][-1].content)
# while True:
#     query=input("user :")
#     if query.lower() in ["bye","exit","good bye"]:
#         print("bye bye")
#         break

#     reponse=agent.invoke({
#         "messages":[{"role":"user","content":query}]
#     },config={
#         "recursion_limit":10,
#         "configurable":{
#             "thread_id":"1"
#         }
#     })
#     print("AI:",reponse["messages"][-1].content)