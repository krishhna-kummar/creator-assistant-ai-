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
OLLAMA_API_KEY = st.secrets.get("ollama_api_key")  # Make sure you add this in Streamlit secrets
OLLAMA_BASE_URL = "https://api.ollama.com"

if not OLLAMA_API_KEY:
    st.error("Ollama API key not found. Please add it to Streamlit secrets as 'ollama_api_key'.")
    st.stop()

headers = {
    "Authorization": f"Bearer {OLLAMA_API_KEY}",
    "Content-Type": "application/json"
}

# -----------------------------
# Verify API key and fetch models
# -----------------------------
try:
    resp = requests.get(f"{OLLAMA_BASE_URL}/v1/models", headers=headers)
    if resp.status_code == 401:
        st.error("Unauthorized: Your Ollama API key is invalid.")
        st.stop()
    elif resp.status_code != 200:
        st.error(f"Failed to fetch models. Status code: {resp.status_code}")
        st.stop()
    models_data = resp.json()
    available_models = [m['name'] for m in models_data.get('models', [])]
    if not available_models:
        st.error("No models found in your Ollama account.")
        st.stop()
except Exception as e:
    st.error(f"Error fetching models: {e}")
    st.stop()

# -----------------------------
# Automatically pick a model
# -----------------------------
# You can let the user pick, or just use the first model
model_choice = available_models[0]
st.info(f"Using model: **{model_choice}**")

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
            "model": model_choice,
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
                content = data['choices'][0]['text']
                st.subheader("Generated Content")
                st.write(content)
            except requests.exceptions.HTTPError as e:
                st.error(f"Failed to generate content: {e}")
            except Exception as e:
                st.error(f"Unexpected error: {e}")
