import streamlit as st
from groq import Groq

# -----------------------------
# Page config
# -----------------------------
st.set_page_config(page_title="Creator Assistant AI", page_icon="✨")

st.title("✨ Creator Assistant AI")
st.write("Generate social media content by tone and platform")

# -----------------------------
# Groq Client (FREE)
# -----------------------------
client = Groq(
    api_key=st.secrets["GROQ_API_KEY"]
)

# -----------------------------
# User Inputs (OLD STYLE)
# -----------------------------
platform = st.selectbox(
    "Choose social media platform",
    ["Instagram", "YouTube", "Twitter (X)", "LinkedIn"]
)

tone = st.selectbox(
    "Choose tone",
    ["Casual", "Professional", "Funny", "Motivational"]
)

topic = st.text_input("What is your content about?")

# -----------------------------
# Generate Content
# -----------------------------
if st.button("Generate Content"):
    if not topic:
        st.warning("Please enter a topic")
    else:
        prompt = f"""
You are a professional social media content creator.

Platform: {platform}
Tone: {tone}
Topic: {topic}

Write engaging, platform-appropriate content.
"""

        with st.spinner("Creating content..."):
            response = client.chat.completions.create(
                model="llama3-70b-8192",
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )

        st.subheader("Generated Content")
        st.write(response.choices[0].message.content)

