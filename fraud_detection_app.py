import streamlit as st
import pandas as pd
import pickle 
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score

# Load dataset (Ensure you have your dataset loaded correctly)
df = pd.read_csv("processed_dataset.csv")  # Change to your actual dataset path

def train_models():
    features = ['step', 'amount', 'oldbalanceOrg', 'newbalanceOrig', 'oldbalanceDest', 'newbalanceDest']
    target = 'isFraud'
    
    X = df[features]
    y = df[target]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
    rf_model.fit(X_train, y_train)
    accuracy_rf = accuracy_score(y_test, rf_model.predict(X_test))
    
    log_model = LogisticRegression(max_iter=1000, random_state=42)
    log_model.fit(X_train, y_train)
    accuracy_log = accuracy_score(y_test, log_model.predict(X_test))
    
    xgb_model = XGBClassifier(eval_metric='logloss', random_state=42)
    xgb_model.fit(X_train, y_train)
    accuracy_xgb = accuracy_score(y_test, xgb_model.predict(X_test))
    
    return {
        "Random Forest": (rf_model, accuracy_rf),
        "Logistic Regression": (log_model, accuracy_log),
        "XGBoost": (xgb_model, accuracy_xgb)
    }

def predict_fraud(transaction, model):
    transaction_df = pd.DataFrame([transaction])
    prediction = model.predict(transaction_df)
    return "Fraud" if prediction[0] == 1 else "Not Fraud"

st.title("Health Insurance Claim Fraud Detection System")

st.header("Enter Transaction Details:")
step = st.number_input("Step (Time Indicator)", min_value=1, value=50)
amount = st.number_input("Transaction Amount", min_value=0.0, value=5000.0)
oldbalanceOrg = st.number_input("Old Balance (Sender)", min_value=0.0, value=25000.0)
newbalanceOrig = st.number_input("New Balance (Sender)", min_value=0.0, value=25000.0)
oldbalanceDest = st.number_input("Old Balance (Receiver)", min_value=0.0, value=50000.0)
newbalanceDest = st.number_input("New Balance (Receiver)", min_value=0.0, value=25000.0)

st.header("Choose Model for Prediction:")
models = train_models()
model_choice = st.selectbox("Select Model", list(models.keys()))
model, accuracy = models[model_choice]

st.markdown(f"### Selected Model: **{model_choice}** (Accuracy: {accuracy * 100:.2f}%)")

if st.button("Predict Fraud"):
    transaction = {
        "step": step,
        "amount": amount,
        "oldbalanceOrg": oldbalanceOrg,
        "newbalanceOrig": newbalanceOrig,
        "oldbalanceDest": oldbalanceDest,
        "newbalanceDest": newbalanceDest
    }
    result = predict_fraud(transaction, model)
    st.subheader(f"Prediction: {result}")
    
    if result == "Fraud":
        st.error("🚨 This transaction is likely fraudulent!")
    else:
        st.success("✅ This transaction is safe!")

st.markdown("---")
st.markdown("**Developed with ❤️ by thiru**")

#python -m streamlit run fraud_detection_app.py

