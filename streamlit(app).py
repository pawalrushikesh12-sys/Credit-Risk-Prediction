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
tab1, tab2 = st.tabs([" Single Prediction", " Batch Prediction"])

# ------------------- Single Prediction -------------------
with tab1:
    st.header(" Enter Applicant Details")

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

# ----------------- CIBIL ESTIMATOR -----------------

elif menu == "CIBIL Estimator":
    st.title("📊 CIBIL Score Estimator")

    st.write("Fill in the details below to estimate your CIBIL score (approximate).")

    # Inputs
    payment_history = st.selectbox("How often do you miss EMI/Credit Card payments?", 
                                   ["Never", "Rarely (1-2 times)", "Often (3+ times)"])
    credit_utilization = st.slider("Credit Utilization (% of limit used)", 0, 100, 30)
    credit_age = st.slider("Credit History Length (years)", 0, 20, 5)
    num_loans = st.number_input("Number of Active Loans", 0, 10, 2)
    recent_inquiries = st.number_input("Recent Loan/Credit Card Applications (last 6 months)", 0, 10, 1)

    if st.button("Estimate My CIBIL Score"):
        # Base Score
        score = 700  

        # Payment history impact
        if payment_history == "Never":
            score += 100
        elif payment_history == "Rarely (1-2 times)":
            score -= 50
        else:  # Often
            score -= 100

        # Credit utilization impact
        if credit_utilization < 30:
            score += 50
        elif credit_utilization > 60:
            score -= 100

        # Credit age impact
        if credit_age > 5:
            score += 50
        elif credit_age < 2:
            score -= 50

        # Loan inquiries impact
        if recent_inquiries > 3:
            score -= 50

        # Loan mix (simplified)
        if num_loans > 1:
            score += 20

        # Keep within 300–900
        score = max(300, min(900, score))

        # Display result
        st.subheader(f"Your Estimated CIBIL Score: **{score}** / 900")

        # Gauge Chart
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=score,
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': "CIBIL Score", 'font': {'size': 24}},
            gauge={
                'axis': {'range': [300, 900]},
                'bar': {'color': "darkblue"},
                'steps': [
                    {'range': [300, 500], 'color': "red"},
                    {'range': [500, 650], 'color': "orange"},
                    {'range': [650, 750], 'color': "yellow"},
                    {'range': [750, 900], 'color': "green"}
                ]
            }
        ))
        st.plotly_chart(fig, use_container_width=True)

        # Text feedback
        if score >= 750:
            st.success("🌟 Excellent Credit Health!")
        elif score >= 650:
            st.info("👍 Good Credit Health")
        elif score >= 500:
            st.warning("⚠️ Fair Credit Health – Needs Improvement")
        else:
            st.error("❌ Poor Credit Health – High Risk")

        # Tips
        st.write("💡 Tips to improve your score:")
        st.write("- Pay EMIs and credit card bills on time.")
        st.write("- Keep credit utilization below 30%.")
        st.write("- Avoid too many loan/credit applications.")
        st.write("- Maintain a long credit history.")
