import streamlit as st
import pickle
import pandas as pd
import plotly.graph_objects as go  # NEW

with open("Classification.pkl", "rb") as f:
    loan_classifier = pickle.load(f)

with open("Regressor.pkl", "rb") as f:
    loan_regressor = pickle.load(f)


st.sidebar.title("Loan Prediction App")
menu = st.sidebar.radio("Navigation", ["Home", "Loan Approval", "Loan Prediction", "CIBIL Estimator"])

# ----------------- HOME -----------------
if menu == "Home":
    st.title("🏦 LoanBuddy")
    st.write("""
    🏦 Welcome to LoanBuddy!
    
    LoanBuddy is your smart companion for quick and reliable loan predictions.
    With just a few simple details, you can:

    - **Check your Loan Eligibility**: Check whether your loan will be approved (Yes/No)
    - **Predict Loan Amount**: Predict how much loan can be sanctioned.
    - **Estimate your CIBIL Score**: If you don’t know your score, get an approximate estimate.

    Designed to be simple, fast, and user-friendly, LoanBuddy helps you make informed financial decisions with confidence.
    """)

# ----------------- LOAN APPROVAL -----------------
elif menu == "Loan Approval":
    st.title("✅ Loan Approval Check")

    self_employed = st.selectbox("Self Employed", ["Yes", "No"])
    income_annum = st.number_input("Annual Income (₹)", 250000, 10000000, 5000000)
    loan_amount = st.number_input("Requested Loan Amount (₹)", 300000, 10000000, 5000000)
    loan_term = st.slider("Loan Term (in years)", 0, 30, 15)
    cibil_score = st.slider("CIBIL Score", 300, 900, 650)

    if st.button("Check Approval"):
        columns = ['self_employed', 'income_annum', 'loan_amount', 'loan_term', 'cibil_score']
        X1 = pd.DataFrame([[self_employed, income_annum, loan_amount, loan_term, cibil_score]],
                 columns=columns)
        pred = loan_classifier.predict(X1)[0]

        if pred == 1:
            st.success("🎉 Congratulations! Your loan is likely to be Approved.")
        else:
            st.error("❌ Sorry, your loan may not be approved.")

# ----------------- LOAN PREDICTION -----------------
elif menu == "Loan Prediction":
    st.title("💰 Loan Amount Prediction")

    self_employed = st.selectbox("Self Employed", ["Yes", "No"])
    income_annum = st.number_input("Annual Income (₹)", 250000, 10000000, 5000000)
    loan_term = st.slider("Loan Term (in years)", 0, 30, 15)
    cibil_score = st.slider("CIBIL Score", 300, 900, 650)

    if st.button("Predict Sanctioned Loan"):
        columns_2 = ['self_employed', 'income_annum', 'loan_term', 'cibil_score']
        X2 = pd.DataFrame([[self_employed, income_annum, loan_term, cibil_score]],
                 columns=columns_2)
        pred = loan_regressor.predict(X2)[0]

        st.success(f"🏦 You are likely to be sanctioned a loan of: ₹{int(pred):,}")

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
