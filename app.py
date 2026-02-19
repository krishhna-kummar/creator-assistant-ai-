import streamlit as st
from openai import OpenAI
import os

st.title("Creator Assistant AI")

prompt = st.text_input("Enter your prompt")

# Create client (reads OPENAI_API_KEY automatically)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

if prompt:
    response = client.responses.create(
        model="gpt-4.1-mini",
        input=prompt
    )

    st.write(response.output_text)
