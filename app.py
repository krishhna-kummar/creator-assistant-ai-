import streamlit as st
import subprocess

# -----------------------------
# Page config
# -----------------------------
st.set_page_config(page_title="Creator Assistant AI", page_icon="✨")
st.title("✨ Creator Assistant AI")
st.write("Generate social media content by tone and platform using local Ollama llama2 model")

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
# Function to run local llama2
# -----------------------------
def generate_with_local_model(prompt):
    try:
        result = subprocess.run(
            ["ollama", "run", "llama2", "--prompt", prompt],
            capture_output=True,
            text=True
        )
        if result.returncode != 0:
            return f"Error running local model: {result.stderr}"
        return result.stdout
    except Exception as e:
        return f"Unexpected error: {e}"

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
        with st.spinner("Generating content locally..."):
            content = generate_with_local_model(prompt)
            st.subheader("Generated Content")
            st.write(content)
