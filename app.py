import streamlit as st
import pandas as pd
import pickle

with open("churn_model.pkl", "rb") as f:
    model = pickle.load(f)

st.title("📊 Customer Churn Prediction")

gender = st.selectbox("Gender", ["Male", "Female"])
senior_citizen = st.selectbox("Senior Citizen", [0, 1])
partner = st.selectbox("Partner", ["Yes", "No"])
dependents = st.selectbox("Dependents", ["Yes", "No"])
tenure = st.slider("Tenure (months)", 0, 72, 12)
phone_service = st.selectbox("Phone Service", ["Yes", "No"])
internet_service = st.selectbox("Internet Service", ["DSL", "Fiber optic", "No"])
contract = st.selectbox("Contract Type", ["Month-to-month", "One year", "Two year"])
paperless_billing = st.selectbox("Paperless Billing", ["Yes", "No"])
payment_method = st.selectbox("Payment Method", [
    "Electronic check", "Mailed check",
    "Bank transfer (automatic)", "Credit card (automatic)"
])
monthly_charges = st.number_input("Monthly Charges ($)", 0.0, 150.0, 65.0)
total_charges = st.number_input("Total Charges ($)", 0.0, 10000.0, 1000.0)

if st.button("🔍 Predict Churn"):
    input_data = pd.DataFrame([[
        1 if gender == "Male" else 0,
        senior_citizen,
        1 if partner == "Yes" else 0,
        1 if dependents == "Yes" else 0,
        tenure,
        1 if phone_service == "Yes" else 0,
        {"DSL": 0, "Fiber optic": 1, "No": 2}[internet_service],
        {"Month-to-month": 0, "One year": 1, "Two year": 2}[contract],
        1 if paperless_billing == "Yes" else 0,
        {"Electronic check": 0, "Mailed check": 1,
         "Bank transfer (automatic)": 2, "Credit card (automatic)": 3}[payment_method],
        monthly_charges,
        total_charges
    ]], columns=[
        'gender', 'SeniorCitizen', 'Partner', 'Dependents', 'tenure',
        'PhoneService', 'InternetService', 'Contract',
        'PaperlessBilling', 'PaymentMethod', 'MonthlyCharges', 'TotalCharges'
    ])

    prediction = model.predict(input_data)[0]
    if prediction == 1:
        st.error("⚠️ This customer is likely to CHURN!")
    else:
        st.success("✅ This customer is NOT likely to churn.")
