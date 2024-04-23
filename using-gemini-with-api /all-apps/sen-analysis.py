import streamlit as st
from dotenv import load_dotenv
import os
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Configure GenAi with your API key
genai.configure(api_key=os.getenv("AIzaSyC-6CFCa1-O6xfskb_Xs2rirUJ7YIdd6Ws"))

# Function to load Gemini Pro model and get responses
def get_gemini_response(question):
    model = genai.GenerativeModel('gemini-1.5-pro-latest')

    chat = model.start_chat(history=[
    {
        "role": "user",
        "parts": ["Analyze the sentiment of the following Tweets and classify them as POSITIVE, NEGATIVE, or NEUTRAL. \"It's so beautiful today!\""]
    },
    {
        "role": "model",
        "parts": ["POSITIVE"]
    },
    {
        "role": "user",
        "parts": ["\"It's so cold today I can't feel my feet...\""]
    },
    {
        "role": "model",
        "parts": ["NEGATIVE"]
    },
    {
        "role": "user",
        "parts": ["\"The weather today is perfectly adequate.\""]
    },
    {
        "role": "model",
        "parts": ["NEUTRAL"]
    },
    ])
    chat.send_message(question)
    if chat is None:
        return "Error: Unable to initiate chat with Gemini Pro model."
    response = chat.last
    if response is None:
        return "Error: No response received from Gemini Pro model."
    return response.text

# Initialize Streamlit app
st.set_page_config(page_title="Sentiment Analysis Demo")
st.header("Sentiment Analysis using Gemini LLM")

# Input text box for user query
input_text = st.text_input("Enter text for sentiment analysis:", "")

# Button to trigger sentiment analysis
submit_button = st.button("Analyze Sentiment")

# Perform sentiment analysis when button is clicked
if submit_button and input_text:
    sentiment = get_gemini_response(input_text)
    st.subheader("Sentiment Analysis Result:")
    st.write(sentiment)

# Display chat history
st.subheader("Chat History:")
for role, text in st.session_state.get("chat_history", []):
    st.write(f"{role}: {text}")
