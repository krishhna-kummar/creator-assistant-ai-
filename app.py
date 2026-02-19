import streamlit as st
from openai import OpenAI
import os

st.title("Creator Assistant AI")

# Dropdowns
platform = st.selectbox(
    "Choose social media platform",
    ["YouTube", "Instagram", "Twitter (X)", "LinkedIn", "Blog"]
)

tone = st.selectbox(
    "Choose tone",
    ["Professional", "Casual", "Funny", "Motivational", "Friendly"]
)

prompt = st.text_input("What do you want to create?")

# OpenAI client (reads API key from Streamlit Secrets)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

if prompt:
    full_prompt = f"""
You are a creator assistant.
Create content for {platform}.
Use a {tone} tone.

User request: {prompt}
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": full_prompt}
        ]
    )

    st.subheader("Generated Content")
    st.write(response.choices[0].message.content)

