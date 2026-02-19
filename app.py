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
# Fetch available models
# -----------------------------
try:
    available_models = client.models.list()
    model_names = [m.name for m in available_models if "chat" in m.name.lower()]
    if not model_names:
        st.error("No chat models available in your account. Please check your Groq dashboard.")
        st.stop()
except Exception as e:
    st.error(f"Failed to fetch models: {e}")
    st.stop()

model_choice = st.selectbox("Select a model", model_names)

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
                response = client.chat.completions.create(
                    model=model_choice,
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.7
                )
                st.subheader("Generated Content")
                st.write(response.choices[0].content)
            except Exception as e:
                st.error(f"Failed to generate content: {e}")
