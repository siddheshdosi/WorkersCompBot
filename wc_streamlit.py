import streamlit as st


import streamlit as st
from langchain_google_genai.chat_models import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage

from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()


chatgpt = ChatGoogleGenerativeAI(model='gemini-2.0-flash',temperature=0)

WC_PROMPT = """
You are Workers Comp Claim assistant. You are created for demo purpose to show example 
how Agent can provide the result related to worker's claim. 

Whenever anyone ask query regarding worker's claim just provide the answer. 
For example:
Question: Can you give me a quick summary of claim 234453455?
Answer: Here's a summary of claim:
        * Claimant: John Doe
        * Injury Date: 12-Jul-2025
        * Claim Type: Indemnity
        * Severity Prediction: Medium Level
        * Reserve Estimate: $3454
        * Current Statu: Open-under medical treatment
        * Assigned Handler: Sarah Thompson (High experience complexity Idemnity claims)
Question: What is the Nature of injury for claim 234453455?
Answer: The nature of injury for claim 234453455 is a Back Injury.

Question: Who is the assigned handler for claim 234453455?
Answer: The assigned handler for claim 234453455 is Sarah Thompson.

Question: What is the current status of claim 234453455?
Answer: The current status of claim 234453455 is Open - Under Medical Treatment.

Question: Provide all details of indicators for claim 234453455 at FNOL
Answer: The indicators for claim 234453455 at FNOL include:
        * Medical treatment Indicator: Yes
        * Hospitalization Indicator: No
        * Attorney Involved Indicator: No
        * insured primised Indicator: Yes
        * Witnesses Indicator: Yes
        * return to work Indicator: No
        * Lost work days Indicator: Yes
        * Doubt indicator: No

Note: 
* you can give any value of claim details as this is just need to show the examples.
* You can only provide the answer related to worker's claim. If anyone ask anything else, just respond with 
 "I am designed to answer queries related to worker's claim only. How can I assist you with that?"
* Your answer should be precise, short and related to worker's claim only.
* Don't give all details of claim, just provide the exact answer of question.
* your answer should be in bullet points if you are providing multiple information.


"""
prompt_template = ChatPromptTemplate([
    ("system", WC_PROMPT),
    ("user","{text}")
])


# Page config
st.set_page_config(page_title="Chubb Worker's Claim AI Assistant", layout="wide")

# Initialize session state
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# Custom CSS
st.markdown("""
    <style>

    .user-msg {
        background-color: #DCF8C6;
        padding: 10px;
        border-radius: 10px;
        margin: 5px;
        text-align: right;
        float: right;
        clear: both;
        max-width: 70%;
    }
    .bot-msg {
        background-color: #F1F0F0;
        padding: 10px;
        border-radius: 10px;
        margin: 5px;
        text-align: left;
        float: left;
        clear: both;
        max-width: 70%;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🤖 Chubb Worker's Claim AI Assistant")

# Chat box container
chat_box = st.container()
with chat_box:
    #st.markdown('<div class="chat-box">', unsafe_allow_html=True)
    for role, text in st.session_state["messages"]:
        if role == "user":
            st.markdown(f'<div class="user-msg">{text}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="bot-msg">{text}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Input box
user_input = st.chat_input("Type your message...")

if user_input:
    # Save user message
    st.session_state["messages"].append(("user", user_input))

    # Replace with real LLM call later
    #bot_response = f"🤖 You asked: {user_input}"
    prompt = prompt_template.invoke({"text": user_input})
    response = chatgpt.invoke(prompt)
    bot_response = '🤖 '+response.content

    st.session_state["messages"].append(("bot", bot_response))

    st.rerun()


