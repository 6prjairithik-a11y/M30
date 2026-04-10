import streamlit as st
import requests
import pandas as pd

# 🔐 Secure API Key (store in .streamlit/secrets.toml)
API_KEY = st.secrets["GROQ_API_KEY"]

GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

# Page config
st.set_page_config(page_title="Concrete AI Predictor", layout="wide")

st.title("🏗 Concrete Strength Prediction & Analysis AI")
st.markdown("### Mix Design Based Prediction (RHA + BSF)")

# =========================
# 🔹 INPUT METHOD SELECTION
# =========================
option = st.radio("Choose Input Method", ["Manual Entry", "Upload CSV"])

# =========================
# 🔹 MANUAL INPUT
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

    analyze = st.button("🔍 Predict & Analyze")

    if analyze:

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
1. Predict compressive strength (MPa).
2. Predict 28-day strength.
3. Classify concrete grade (M20, M25, M30, etc.).
4. Analyze effect of RHA and BSF.
5. Evaluate durability and cracking risk.
6. Suggest mix improvements.

Give a structured engineering report.
"""

            data = {
                "model": "llama-3.1-8b-instant",
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.3,
                "max_tokens": 800
            }

            with st.spinner("🤖 AI Analyzing..."):
                response = requests.post(GROQ_URL, headers=headers, json=data)
                result = response.json()

                if "choices" in result:
                    output = result["choices"][0]["message"]["content"]
                    st.subheader("📊 AI Engineering Report")
                    st.write(output)
                else:
                    st.error("API Error")
                    st.write(result)

# =========================
# 🔹 CSV UPLOAD MODE
# =========================
else:

    st.subheader("📂 Upload CSV File")

    file = st.file_uploader("Upload your dataset", type=["csv"])

    if file:
        df = pd.read_csv(file)

        st.write("### Preview Data")
        st.dataframe(df.head())

        required_columns = [
            "Cement_kg_m3",
            "RHA_percent",
            "BSF_percent",
            "Water_kg_m3",
            "Fine_Aggregate_kg_m3",
            "Coarse_Aggregate_kg_m3",
            "Water_Cement_Ratio",
            "Age_days"
        ]

        if all(col in df.columns for col in required_columns):

            if st.button("🔍 Analyze Dataset"):

                sample = df.iloc[0].to_dict()

                prompt = f"""
You are a professional structural engineer.

Concrete Mix Sample Data:
{sample}

Tasks:
1. Predict compressive strength.
2. Predict 28-day strength.
3. Identify concrete grade.
4. Analyze trends in dataset.
5. Suggest improvements.

Give structured report.
"""

                data = {
                    "model": "llama-3.1-8b-instant",
                    "messages": [{"role": "user", "content": prompt}],
                    "temperature": 0.3,
                    "max_tokens": 800
                }

                with st.spinner("🤖 AI Analyzing Dataset..."):
                    response = requests.post(GROQ_URL, headers=headers, json=data)
                    result = response.json()

                    if "choices" in result:
                        output = result["choices"][0]["message"]["content"]
                        st.subheader("📊 AI Dataset Report")
                        st.write(output)
                    else:
                        st.error("API Error")
                        st.write(result)

        else:
            st.error("CSV must contain required columns!")
