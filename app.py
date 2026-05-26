import streamlit as st
import pickle
import pandas as pd

st.set_page_config(
    page_title="Retail Sales Intelligence System",
    page_icon="📊",
    layout="wide"
)

st.markdown("""
<style>
.main { background-color: #f5f7fa; }
.big-title {
    font-size: 42px;
    font-weight: 800;
    text-align: center;
    color: #1f4e79;
}
.subtitle {
    text-align: center;
    font-size: 18px;
    color: #555;
}
.card {
    background-color: white;
    padding: 25px;
    border-radius: 18px;
    box-shadow: 0px 4px 18px rgba(0,0,0,0.08);
}
.result-profit {
    background-color: #d4edda;
    color: #155724;
    padding: 25px;
    border-radius: 15px;
    font-size: 26px;
    text-align: center;
    font-weight: bold;
}
.result-loss {
    background-color: #f8d7da;
    color: #721c24;
    padding: 25px;
    border-radius: 15px;
    font-size: 26px;
    text-align: center;
    font-weight: bold;
}
.stButton>button {
    background-color: #1f4e79;
    color: white;
    border-radius: 12px;
    height: 3em;
    width: 100%;
    font-size: 18px;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

model = pickle.load(open("profit_prediction_model.pkl", "rb"))
model_columns = pickle.load(open("model_columns.pkl", "rb"))

st.markdown('<div class="big-title">📊 Retail Sales Intelligence System</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">AI-powered Profit/Loss Prediction for Retail Orders</div>', unsafe_allow_html=True)
st.write("")

left, right = st.columns([2, 1])

with left:
    

    st.subheader("🧾 Order Details")

    col1, col2 = st.columns(2)

    with col1:
        ship_mode = st.selectbox("🚚 Ship Mode", ["Standard Class", "Second Class", "First Class", "Same Day"])
        segment = st.selectbox("👥 Customer Segment", ["Consumer", "Corporate", "Home Office"])
        region = st.selectbox("🌍 Region", ["West", "East", "Central", "South"])
        category = st.selectbox("📦 Category", ["Furniture", "Office Supplies", "Technology"])

    with col2:
        sub_category = st.selectbox("🏷️ Sub-Category", [
            "Bookcases", "Chairs", "Labels", "Tables", "Storage", "Furnishings",
            "Art", "Phones", "Binders", "Appliances", "Paper", "Accessories",
            "Envelopes", "Fasteners", "Supplies", "Machines", "Copiers"
        ])
        sales = st.slider("💰 Sales", 0.0, 25000.0, 500.0)
        quantity = st.slider("📦 Quantity", 1, 15, 3)
        discount = st.slider("🏷️ Discount", 0.0, 0.8, 0.1)

    

with right:
    

    st.subheader("📌 Input Summary")

    st.metric("Sales", f"${sales:,.2f}")
    st.metric("Quantity", quantity)
    st.metric("Discount", f"{discount*100:.0f}%")

    

st.write("")

input_data = pd.DataFrame({
    "Ship Mode": [ship_mode],
    "Segment": [segment],
    "Region": [region],
    "Category": [category],
    "Sub-Category": [sub_category],
    "Sales": [sales],
    "Quantity": [quantity],
    "Discount": [discount]
})

input_encoded = pd.get_dummies(input_data)
input_encoded = input_encoded.reindex(columns=model_columns, fill_value=0)

if st.button("🔮 Predict Profit / Loss"):
    prediction = model.predict(input_encoded)[0]

    if prediction == 1:
        st.markdown('<div class="result-profit">✅ Prediction: PROFITABLE ORDER</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="result-loss">❌ Prediction: LOSS MAKING ORDER</div>', unsafe_allow_html=True)

    st.write("")
    st.subheader("📊 Order Preview")
    st.dataframe(input_data, use_container_width=True)