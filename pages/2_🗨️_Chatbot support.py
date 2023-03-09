import streamlit as st
from streamlit_chat import message
import requests

st.set_page_config(page_title="Chatbot support", page_icon="🗨️", layout="wide", initial_sidebar_state="expanded")

st.markdown("# 🗨️ Chatbot support")
# sidebar
with st.sidebar.form(key='Form1'):
    st.title("🌏 Energy efficiency")
    st.image("charts sig/1.png", width=250)
    st.markdown("Energy efficiency is the goal of reducing the amount of energy required to provide products and services. "
                "Energy efficiency is also a resource that can be used to provide other services, such as providing "
                "electricity during times of peak demand.")
    
    st.title("🌏 Gas emisions")
    st.image("charts sig/2.png", width=250)
    st.markdown("Gas emissions are the gases that are released into the atmosphere by human activities. "
                "These gases are released into the atmosphere by burning fossil fuels, "
                "such as coal, oil, and natural gas, and by deforestation.")

    generator = st.form_submit_button(label='Download the report')	
st.write(
    """Insert a text here"""
)

API_URL = "https://api-inference.huggingface.co/models/facebook/blenderbot-400M-distill"
headers = {"Authorization": st.secrets['api_key']}


if 'generated' not in st.session_state:
    st.session_state['generated'] = []

if 'past' not in st.session_state:
    st.session_state['past'] = []

def query(payload):
	response = requests.post(API_URL, headers=headers, json=payload)
	return response.json()

def get_text():
    input_text = st.text_input("You: ","I need help building a sustainable company", key="input")
    return input_text 


user_input = get_text()

if user_input:
    output = query({
        "inputs": {
            "past_user_inputs": st.session_state.past,
            "generated_responses": st.session_state.generated,
            "text": user_input,
        },"parameters": {"repetition_penalty": 1.33},
    })

    st.session_state.past.append(user_input)
    st.session_state.generated.append(output["generated_text"])

if st.session_state['generated']:

    for i in range(len(st.session_state['generated'])-1, -1, -1):
        message(st.session_state["generated"][i], key=str(i))
        message(st.session_state['past'][i], is_user=True, key=str(i) + '_user')