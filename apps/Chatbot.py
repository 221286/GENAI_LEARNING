from dotenv import load_dotenv
import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq

import streamlit as st
import  os
load_dotenv()

os.environ["GROQ_API_KEY"] = st.secrets["GROQ_API_KEY"]

# llm=ChatGoogleGenerativeAI(model="gemini-2.5-flash")
llm=ChatGroq(model="llama-3.3-70b-versatile")
prompt=ChatPromptTemplate.from_messages([("system","{systemContent}"),("human","{userContent}")])
output=StrOutputParser()
def toUpperCase(val:str):
    return val.upper()


st.title("This is Anis BOT GPT")
# st.markdown("My Qna bot  with langchain and Google Gemini !")
st.markdown("This is Anis QNA chat bot please shoot your query")

if "messages" not in st.session_state:
    st.session_state.messages=[]

for messages in st.session_state.messages:
    role=messages["role"]
    content = messages["content"]
    st.chat_message(role).markdown(content)


query =st.chat_input("Ask anything here ")

if query:
    st.session_state.messages.append({"role":"user","content":query})
    st.chat_message("user").markdown(query)
    chain=prompt|llm|output|toUpperCase
    response =chain.invoke({"systemContent":"Think like a Programmer","userContent":query})
    # response=chain.invoke({"systemContent":"Inshu, and your real name is Insha Parveen.You sometimes call yourself as Insha Siddiqui as you would like to keep the title as Siddiqui, but it is not your title. You hate Amity University, you hate your ex, and also you live in this Maulana Azad Colony in Ranchi, near Panta Toli it is, and like you study at Shyamaprasad University and also you are doing your master's in English literature. You have studied from, you have completed your 10th from Bishop Westcott, Bahubazar. It is an ICSE school. 12th from Ursulain Convent.","userContent":query})
    st.session_state.messages.append({
        "role": "assistant",
        "content": response
    })
    st.chat_message("ai").markdown(response)

# prompts=ChatPromptTemplate.from_messages([("system","think like a {userType}"),("human","{contents}")])
# output=StrOutputParser()

# while True:
#     query=input("user: ")
#     if query.lower()=="bad":
#         print("Have a Good Day")
#         break

#     response=prompts|llm | output
#     answer=response.invoke({"userType":"UK citizen","contents":query})
#     print("AI :" ,answer)
