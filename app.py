import streamlit as st
import requests

# -----------------------------
# Page config
# -----------------------------
st.set_page_config(page_title="Creator Assistant AI", page_icon="✨")
st.title("✨ Creator Assistant AI")
st.write("Generate social media content by tone and platform")

# -----------------------------
# Ollama API Key
# -----------------------------
OLLAMA_API_KEY = st.secrets.get("ollama_api_key")  # Set your Ollama API key in Streamlit secrets
OLLAMA_BASE_URL = "https://api.ollama.com"

if not OLLAMA_API_KEY:
    st.error("Ollama API key not found. Please add it to Streamlit secrets as 'ollama_api_key'.")
    st.stop()

headers = {
    "Authorization": f"Bearer {OLLAMA_API_KEY}",
    "Content-Type": "application/json"
}

# -----------------------------
# Inputs
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
# Generate content
# -----------------------------
if st.button("Generate Content"):
    if not topic.strip():
        st.warning("Please enter a topic")
    else:
        prompt = f"""
You are a professional social media content creator.

Platform: {platform}
Tone: {tone}
Topic: {topic}

Write engaging, platform-appropriate content.
"""

        payload = {
            "model": "llama2",  # replace with any model you have in Ollama
            "prompt": prompt,
            "max_tokens": 300
        }

        with st.spinner("Creating content..."):
            try:
                response = requests.post(
                    f"{OLLAMA_BASE_URL}/v1/completions",
                    headers=headers,
                    json=payload
                )
                response.raise_for_status()
                data = response.json()
                # Ollama returns output in data['choices'][0]['text']
                content = data['choices'][0]['text']
                st.subheader("Generated Content")
                st.write(content)
            except Exception as e:
                st.error(f"Failed to generate content: {e}")
