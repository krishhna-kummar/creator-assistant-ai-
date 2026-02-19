import streamlit as st
from openai import OpenAI

client = OpenAI(api_key="PASTE_YOUR_API_KEY_HERE")

st.title("🎥 Creator Assistant AI")

niche = st.text_input("Your niche (e.g. fitness, tech, fashion)")
platform = st.selectbox("Platform", ["YouTube", "TikTok", "Twitter/X"])
tone = st.selectbox("Tone", ["Educational", "Casual", "Energetic", "Spicy"])

if st.button("Generate Ideas"):
    prompt = f"""
    You are a creator assistant.
    Generate 5 viral content ideas for a {niche} creator on {platform}.
    Tone: {tone}.
    Include a hook for each idea.
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    st.write(response.choices[0].message.content)
