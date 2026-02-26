import streamlit as st
import requests

# -----------------------------
# 🔐 HARD CODE YOUR GEMINI API KEY
# -----------------------------
API_KEY = "AIzaSyDGJeBg8ekOWLKoF_cuIhi1VPJMDl02HWk"

API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={API_KEY}"

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(page_title="Concrete AI Predictor", layout="wide")

st.title("🏗 Concrete Strength Prediction & Analysis AI")
st.markdown("Interactive Civil Engineering Assistant")

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
        area = (dimension * dimension)  # mm²
        compressive_strength = (load * 1000) / area  # N/mm²

        st.subheader("📐 Calculated Compressive Strength")
        st.success(f"{compressive_strength:.2f} N/mm²")

        # Prepare prompt for Gemini
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
3. Analyze strength development trend.
4. Evaluate thermal cracking risk.
5. Provide durability assessment.
6. Give final professional recommendation.

Be structured and technical.
"""

        payload = {
            "contents": [{
                "parts": [{"text": prompt}]
            }]
        }

        with st.spinner("Analyzing with AI..."):
            try:
                response = requests.post(API_URL, json=payload)
                result = response.json()

                if "candidates" in result:
                    output = result["candidates"][0]["content"]["parts"][0]["text"]
                    st.subheader("📊 AI Engineering Report")
                    st.write(output)
                else:
                    st.error("Unexpected API response")
                    st.write(result)

            except Exception as e:
                st.error("Error occurred")
                st.write(e)
