import streamlit as st
import requests

# -----------------------------
# 🔐 HARD CODE YOUR API KEY HERE
# -----------------------------
API_KEY = "AIzaSyC0KJNhoK5DN0Imzz0StzcIww_gKZk2wYk"

API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={API_KEY}"

# -----------------------------
# PAGE SETUP
# -----------------------------
st.set_page_config(page_title="Concrete AI Predictor", layout="wide")

st.title("🏗 M30 Concrete AI Prediction System")
st.markdown("LLM-Based Engineering Analysis")

# -----------------------------
# USER INPUT
# -----------------------------
st.subheader("📥 Paste Experimental Data")
user_data = st.text_area("Enter Concrete Data Below", height=350)

analyze_button = st.button("🔍 Analyze")

# -----------------------------
# PROCESS
# -----------------------------
if analyze_button:

    if not user_data.strip():
        st.error("Please paste your experimental data.")
    else:
        with st.spinner("Analyzing concrete behavior..."):

            prompt = f"""
You are a senior structural engineer.

Analyze the following M30 concrete experimental dataset:

{user_data}

Provide a structured professional engineering report including:

1. Strength development analysis (3, 7, 28 days)
2. Whether M30 grade requirement is satisfied
3. Comparison between mixes (if available)
4. Peak temperature and hydration analysis
5. Thermal cracking risk evaluation
6. Long-term durability assessment
7. Final engineering recommendation

Be technical and structured.
"""

            payload = {
                "contents": [{
                    "parts": [{"text": prompt}]
                }]
            }

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
