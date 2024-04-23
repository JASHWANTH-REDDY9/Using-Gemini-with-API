# Q&A Chatbot
from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.

import streamlit as st
import os
import pathlib
import textwrap
from PIL import Image


import google.generativeai as genai

os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

## Function to load OpenAI model and get respones

def get_gemini_response(input, image):
    model = genai.GenerativeModel('gemini-pro-vision')
    if input!="":
       response = model.generate_content([input,image])
    else:
       response = model.generate_content(image)
    return response.text

##initialize our streamlit app

st.set_page_config(page_title="Gemini Image Demo")

# Page Title
st.title("Gemini Vision Application")

# Input Prompt
input_prompt = st.text_input("Input Prompt:", key="input")

# File Uploader for Image
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

# Display Uploaded Image
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image.", use_column_width=True)

# Button to Trigger Analysis
submit_button = st.button("Analyze Image")

## If submit button is clicked
if submit_button:
    # Perform analysis
    if input_prompt:
        response = get_gemini_response(input_prompt, image)
    else:
        response = get_gemini_response("", image)
        
    # Display Response
    st.subheader("Analysis Result:")
    st.write(response)
