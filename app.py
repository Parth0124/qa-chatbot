import streamlit as st
import openai
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

import os
from dotenv import load_dotenv

load_dotenv()

os.environ['LANGCHAIN_API_KEY'] = os.getenv("LANGCHAIN_API_KEY")
os.environ['LANGCHAIN_TRACING_V2'] = "true"
os.environ["LANGCHAIN_PROJECT"] = "Question Answer Chatbot"


#Prompt template
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a helpfull assistant. please respond to the user queries."),
        ("user", "Question:{question}")
    ]
)

def generate_response(question, api_key,llm,temperature, max_tokens):
    openai.api_key = api_key
    llm = ChatOpenAI(model=llm)
    outputparser = StrOutputParser()
    chain = prompt|llm|outputparser
    answer = chain.invoke({"question": question})
    return answer


##Streamlit

st.title("Enhanced Question and Answer Chatbot")
api_key = st.sidebar.text_input("Enter your openAI api key:", type="password")

llm = st.sidebar.selectbox("Select an OpenAI model", ['gpt-4o', 'gpt-4-turbo', 'gpt-4'])

temperature = st.sidebar.slider("Temperature", min_value=0.0, max_value=1.0, value=0.7)
max_tokens = st.sidebar.slider("Maximum Tokens", min_value=50, max_value=500, value = 150)

st.write("Go ahead and ask me anything")
user_input = st.text_input("You:")

if user_input:
    response = generate_response(user_input, api_key, llm, temperature, max_tokens)
    st.write(response)
else:
    st.write("Please provide your query!")
