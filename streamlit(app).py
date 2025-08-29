import streamlit as st
import pandas as pd
import numpy as np
import random

# ------------------- Page Config -------------------
st.set_page_config(page_title="Credit Risk Prediction",
                   page_icon="💳",
                   layout="wide")

# ------------------- App Header -------------------
st.title("💳 Bank Loan Credit Risk Prediction")
st.markdown("A smart tool to predict **loan default risk** using Machine Learning.")

# Tabs for Single vs Batch Prediction
tab1, tab2 = st.tabs(["📌 Single Prediction", "📂 Batch Prediction"])

# ------------------- Single Prediction -------------------
with tab1:
    st.header("📌 Enter Applicant Details")

    # Sidebar Inputs
    with st.sidebar:
        st.subheader("🔧 Input Parameters")
        age = st.slider("Age", 18, 70, 30)
        income = st.number_input("Monthly Income (₹)", 1000, 100000, 30000, step=1000)
        loan_amount = st.number_input("Loan Amount (₹)", 1000, 1000000, 200000, step=5000)
        loan_term = st.selectbox("Loan Term (Months)", [12, 24, 36, 60, 120])
        credit_history = st.selectbox("Credit History", ["Good", "Bad"])
        predict_btn = st.button("🔍 Predict Risk")

    # Prediction Output
    if predict_btn:
        # (Dummy logic: Replace this with your team’s model)
        probability = round(random.uniform(0, 1), 2)
        prediction = "❌ High Risk" if probability > 0.5 else "✅ Low Risk"

        st.subheader("🔍 Prediction Result")
        if prediction == "❌ High Risk":
            st.error(f"**Result:** {prediction} \n\n Default Probability: {probability*100:.1f}%")
        else:
            st.success(f"**Result:** {prediction} \n\n Default Probability: {probability*100:.1f}%")

        # Feature Importance (Dummy Visualization)
        st.subheader("📊 Feature Importance (Demo)")
        st.bar_chart({"Feature": ["Age", "Income", "LoanAmount", "LoanTerm", "CreditHistory"],
                      "Importance": [0.2, 0.3, 0.25, 0.15, 0.1]})

# ------------------- Batch Prediction -------------------
with tab2:
    st.header("📂 Batch Credit Risk Prediction")

    uploaded_file = st.file_uploader("Upload CSV file with applicant data", type=["csv"])

    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        st.write("📄 Uploaded Data Preview:")
        st.dataframe(df.head())

        # (Dummy predictions: Replace with real model)
        df["Default_Probability"] = np.random.rand(len(df))
        df["Prediction"] = df["Default_Probability"].apply(lambda x: "❌ High Risk" if x > 0.5 else "✅ Low Risk")

        st.subheader("📊 Prediction Results")
        st.dataframe(df)

        # Download option
        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button(label="📥 Download Results as CSV",
                           data=csv,
                           file_name="credit_risk_predictions.csv",
                           mime="text/csv")
