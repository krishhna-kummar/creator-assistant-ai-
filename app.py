import streamlit as st
from groq import Groq

# -----------------------------
# Page config
# -----------------------------
st.set_page_config(page_title="Creator Assistant AI", page_icon="✨")
st.title("✨ Creator Assistant AI")
st.write("Generate social media content by tone and platform")

# -----------------------------
# Load Groq API key
# -----------------------------
if "gsk" not in st.secrets:
    st.error("API key not found! Please add your Groq API key in Streamlit secrets as `gsk`.")
    st.stop()

api_key = st.secrets["gsk"]

try:
    client = Groq(api_key=api_key)
except Exception as e:
    st.error(f"Failed to initialize Groq client: {e}")
    st.stop()

# -----------------------------
# List available models
# -----------------------------
try:
    available_models = client.models.list()
    text_models = [m[0] for m in available_models if "chat" not in m[0].lower()]
    
    if not text_models:
        st.error("No completion models available in your account. Please check your Groq dashboard.")
        st.stop()
    
    model_choice = text_models[0]  # Automatically pick the first available text model
    st.info(f"Using model: **{model_choice}**")
    
except Exception as e:
    st.error(f"Failed to fetch models: {e}")
    st.stop()

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
        with st.spinner("Creating content..."):
            try:
                response = client.completions.create(
                    model=model_choice,
                    prompt=prompt,
                    max_tokens=300,
                    temperature=0.7
                )
                st.subheader("Generated Content")
                st.write(response.choices[0].text)
            except Exception as e:
                st.error(f"Failed to generate content: {e}")
