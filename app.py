import streamlit as st
import requests
import pandas as pd

# 🔐 Direct API Key (NOT SAFE for public repos)
API_KEY = "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"

GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

st.set_page_config(page_title="Concrete AI Predictor", layout="wide")

st.title("🏗 Concrete Strength Prediction & Analysis AI")
st.markdown("### Mix Design Based Prediction (RHA + BSF)")

# =========================
# INPUT METHOD
# =========================
option = st.radio("Choose Input Method", ["Manual Entry", "Upload CSV"])

# =========================
# MANUAL ENTRY
# =========================
if option == "Manual Entry":

    st.subheader("📥 Enter Concrete Mix Details")

    col1, col2 = st.columns(2)

    with col1:
        cement = st.number_input("Cement (kg/m³)", min_value=0.0)
        rha = st.number_input("RHA (%)", min_value=0.0)
        bsf = st.number_input("BSF (%)", min_value=0.0)
        water = st.number_input("Water (kg/m³)", min_value=0.0)

    with col2:
        fine_agg = st.number_input("Fine Aggregate (kg/m³)", min_value=0.0)
        coarse_agg = st.number_input("Coarse Aggregate (kg/m³)", min_value=0.0)
        wcr = st.number_input("Water-Cement Ratio", min_value=0.0)
        age = st.number_input("Age (days)", min_value=1)

    if st.button("🔍 Predict & Analyze"):

        if cement == 0 or water == 0:
            st.error("Please enter valid mix values.")
        else:

            prompt = f"""
You are a professional structural engineer.

Concrete Mix Data:
Cement: {cement} kg/m³
RHA: {rha} %
BSF: {bsf} %
Water: {water} kg/m³
Fine Aggregate: {fine_agg} kg/m³
Coarse Aggregate: {coarse_agg} kg/m³
Water-Cement Ratio: {wcr}
Age: {age} days

Tasks:
1. Predict compressive strength (MPa)
2. Predict 28-day strength
3. Classify grade
4. Analyze RHA & BSF effects
5. Check durability & cracking risk
6. Suggest improvements
"""

            data = {
                "model": "llama-3.1-8b-instant",
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.3,
                "max_tokens": 800
            }

            with st.spinner("🤖 AI Analyzing..."):
                response = requests.post(GROQ_URL, headers=headers, json=data)

                if response.status_code == 200:
                    result = response.json()
                    output = result["choices"][0]["message"]["content"]
                    st.subheader("📊 AI Report")
                    st.write(output)
                else:
                    st.error("API Error")
                    st.write(response.text)

# =========================
# CSV MODE
# =========================
else:

    st.subheader("📂 Upload CSV")

    file = st.file_uploader("Upload CSV", type=["csv"])

    if file:
        df = pd.read_csv(file)
        st.dataframe(df.head())

        if st.button("🔍 Analyze Dataset"):

            sample = df.iloc[0].to_dict()

            prompt = f"""
You are a structural engineer.

Analyze this concrete data:
{sample}

Give:
- Strength prediction
- Grade classification
- Mix improvement suggestions
"""

            data = {
                "model": "llama-3.1-8b-instant",
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.3,
                "max_tokens": 800
            }

            with st.spinner("🤖 AI Analyzing..."):
                response = requests.post(GROQ_URL, headers=headers, json=data)

                if response.status_code == 200:
                    result = response.json()
                    output = result["choices"][0]["message"]["content"]
                    st.write(output)
                else:
                    st.error("API Error")
                    st.write(response.text)
