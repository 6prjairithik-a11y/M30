import streamlit as st
import requests

# -----------------------------
# 🔐 HARD CODE YOUR GROQ API KEY
# -----------------------------
API_KEY = "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"

GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(page_title="Concrete AI Predictor", layout="wide")

st.title("🏗 Concrete Strength Prediction & Analysis AI")
st.markdown("Powered by Groq (Free LLM API)")

# -----------------------------
# INPUT SECTION
# -----------------------------
st.subheader("📥 Enter Concrete Test Details")

age = st.number_input("Age of Concrete (Days)", min_value=1)
load = st.number_input("Applied Load (kN)", min_value=0.0)
dimension = st.number_input("Cube Dimension (mm)", value=150)
peak_temp = st.number_input("Peak Concrete Temperature (°C)")
ambient_temp = st.number_input("Ambient Temperature (°C)")
strength_3 = st.number_input("3-Day Strength (Optional)", value=0.0)
strength_7 = st.number_input("7-Day Strength (Optional)", value=0.0)

analyze = st.button("🔍 Predict & Analyze")

# -----------------------------
# PROCESS
# -----------------------------
if analyze:

    if load == 0 or dimension == 0:
        st.error("Please enter valid load and dimension.")
    else:
        # Calculate compressive strength
        area = dimension * dimension  # mm²
        compressive_strength = (load * 1000) / area  # N/mm²

        st.subheader("📐 Calculated Compressive Strength")
        st.success(f"{compressive_strength:.2f} N/mm²")

        prompt = f"""
You are a professional structural engineer.

Concrete Test Data:
Age: {age} days
Calculated Strength: {compressive_strength:.2f} N/mm2
3-Day Strength: {strength_3}
7-Day Strength: {strength_7}
Peak Temperature: {peak_temp} °C
Ambient Temperature: {ambient_temp} °C

Tasks:
1. Predict 28-day strength.
2. Check if it satisfies M30 grade requirement.
3. Analyze strength development.
4. Evaluate thermal cracking risk.
5. Give final professional recommendation.
Provide structured technical report.
"""

        data = {
            "model": "llama3-8b-8192",
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.3,
            "max_tokens": 800
        }

        with st.spinner("Analyzing with AI..."):
            try:
                response = requests.post(GROQ_URL, headers=headers, json=data)
                result = response.json()

                if "choices" in result:
                    output = result["choices"][0]["message"]["content"]
                    st.subheader("📊 AI Engineering Report")
                    st.write(output)
                else:
                    st.error("Unexpected API response")
                    st.write(result)

            except Exception as e:
                st.error("Error occurred")
                st.write(e)
