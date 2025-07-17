import streamlit as st
import subprocess

st.set_page_config(page_title="📈 Trading Bot", page_icon="💹", layout="centered")


st.markdown("""
<style>
body {
    background: linear-gradient(120deg, #e0f7fa, #ffffff);
}
.stApp {
    background-image: url("https://images.unsplash.com/photo-1612831455544-bfbb4e413b38?ixlib=rb-4.0.3&auto=format&fit=crop&w=1950&q=80");
    background-size: cover;
    background-attachment: fixed;
}
.main-card {
    background-color: rgba(255, 255, 255, 0.85);
    padding: 20px;
    border-radius: 10px;
    box-shadow: 0 4px 6px rgba(0,0,0,0.1);
}
div.stButton > button {
    background-color: #007bff;
    color: white;
    font-weight: bold;
    border-radius: 0.25rem;
    padding: 0.5rem 1rem;
    border: none;
}
div.stButton > button:hover {
    background-color: #0056b3;
}
.success-box {
    background-color: #d4edda;
    color: #155724;
    border: 1px solid #c3e6cb;
    padding: 10px;
    border-radius: 4px;
    margin-top: 10px;
}
.error-box {
    background-color: #f8d7da;
    color: #721c24;
    border: 1px solid #f5c6cb;
    padding: 10px;
    border-radius: 4px;
    margin-top: 10px;
}
</style>
""", unsafe_allow_html=True)

# Header with an image
st.markdown("<h1 style='text-align: center; color: #007bff;'>📈 Trading Bot Dashboard</h1>", unsafe_allow_html=True)
st.markdown(
    "<div style='text-align:center'><img src='https://cdn-icons-png.flaticon.com/512/2620/2620457.png' width='80'></div>", 
    unsafe_allow_html=True
)
st.write("<p style='text-align:center'>Hello 👋 — I am Finn, your stock prediction bot. Please enter a stock symbol and timeframe below!</p>", unsafe_allow_html=True)

# Main form card
with st.container():
    st.markdown("<div class='main-card'>", unsafe_allow_html=True)
    with st.form("prediction_form"):
        ticker = st.text_input("🔷 Stock Ticker Symbol", placeholder="e.g. AAPL, TSLA")
        timeframe = st.selectbox("🔷 Select Timeframe", 
            options=["1d", "5d", "1mo", "3mo", "6mo", "1y"])
        submitted = st.form_submit_button("Get Prediction")
    st.markdown("</div>", unsafe_allow_html=True)

if submitted:
    if not ticker or not timeframe:
        st.markdown('<div class="error-box">⚠️ Please fill all fields correctly.</div>', unsafe_allow_html=True)
    else:
        with st.spinner("⏳ Running prediction… Please wait."):
            result = subprocess.run(
                ['python', 'Trading_Bot.py', ticker, timeframe],
                stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
            )

        if result.returncode == 0:
            prediction = result.stdout.strip()
            st.markdown(f'<div class="success-box">✅ The bot suggests: <strong>{prediction}</strong></div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="error-box">❌ Error running prediction script.</div>', unsafe_allow_html=True)
            with st.expander("Show error details"):
                st.text(result.stderr)


st.markdown("""
<hr>
<div style='text-align:center; font-size: small'>
Made with  using Streamlit & Bootstrap theme.
</div>
""", unsafe_allow_html=True)
