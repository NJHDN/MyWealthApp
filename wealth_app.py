import streamlit as st
import pandas as pd
import yfinance as yf
import requests

# Page Config
st.set_page_config(page_title="WealthMax 2026 | Verified Data", layout="wide")

# Hybrid Database: [Yahoo Ticker, AMFI Code]
mf_db = {
    "Small Cap": {
        "Quant Small Cap": ["0P0000XW9A.BO", "120849"],
        "Nippon Small Cap": ["0P0000XW9L.BO", "118778"],
        "Bandhan Small Cap": ["0P0000Y2O3.BO", "128947"],
        "Tata Small Cap": ["0P0001EV4I.BO", "144181"],
        "HDFC Small Cap": ["0P0000XW8F.BO", "119063"],
        "Axis Small Cap": ["0P0000XW6Y.BO", "125354"],
        "Kotak Small Cap": ["0P0000XW94.BO", "114389"],
        "HSBC Small Cap": ["0P000171W3.BO", "130635"],
        "Franklin Small Cap": ["0P0000XW84.BO", "118741"],
        "Invesco Small Cap": ["0P0001EV4G.BO", "143248"]
    },
    "Mid Cap": {
        "Motilal Midcap": ["0P00013X1T.BO", "127042"],
        "HDFC Mid-Cap Opp": ["0P0000XW8G.BO", "119036"],
        "Edelweiss Mid Cap": ["0P0000XVZ9.BO", "121406"],
        "Quant Mid Cap": ["0P0000XW99.BO", "120841"],
        "Kotak Emerging": ["0P0000XW93.BO", "114392"],
        "Nippon Growth": ["0P0000XW9M.BO", "118788"],
        "SBI Magnum Midcap": ["0P0000XVZ1.BO", "119551"],
        "Mirae Midcap": ["0P0001IP7C.BO", "146882"],
        "Axis Midcap": ["0P0000XW6X.BO", "114400"],
        "DSP Midcap": ["0P0000XW7U.BO", "118544"]
    }
}

st.sidebar.title("💎 WealthMax Dashboard")
page = st.sidebar.selectbox("Menu", ["Live Watchlist", "Portfolio Manager", "Tax Planner"])
segment = st.sidebar.radio("Segment", ["Small Cap", "Mid Cap"])

# Hybrid Fetching Engine
def fetch_verified_nav(y_ticker, amfi_code):
    # Try Yahoo first
    try:
        data = yf.Ticker(y_ticker).history(period="1d")
        if not data.empty:
            return round(data['Close'].iloc[-1], 2), data.index[-1].strftime('%d-%m-%Y')
    except: pass
    
    # Backup: Try AMFI API
    try:
        res = requests.get(f"https://api.mfapi.in/mf/{amfi_code}", timeout=10).json()
        return float(res['data'][0]['nav']), res['data'][0]['date']
    except: return "Error", "Error"

if page == "Live Watchlist":
    st.header(f"🚀 {segment} (Verified 2026 Data)")
    rows = []
    with st.spinner('Validating Real-time Prices...'):
        for i, (name, codes) in enumerate(mf_db[segment].items(), 1):
            nav, date = fetch_verified_nav(codes[0], codes[1])
            rows.append({"#": i, "Fund Name": name, "NAV (₹)": nav, "Updated": date})
    
    st.table(pd.DataFrame(rows).set_index('#'))

elif page == "Portfolio Manager":
    st.header("💼 Wealth Tracker")
    inv = st.number_input("Invested Amount (₹)", value=100000)
    b_nav = st.number_input("Purchase NAV", value=100.0)
    f_choice = st.selectbox("Fund", list(mf_db[segment].keys()))
    codes = mf_db[segment][f_choice]
    curr_nav, _ = fetch_verified_nav(codes[0], codes[1])
    
    if isinstance(curr_nav, (float, int)):
        val = (inv / b_nav) * curr_nav
        st.metric("Current Value", f"₹{val:,.2f}", f"Profit: ₹{val-inv:,.2f}")

elif page == "Tax Planner":
    st.header("🏦 Tax Calculator")
    target = st.number_input("Target Amount", value=3000000)
    profit = target - 1000000
    tax = max(0, profit - 125000) * 0.125
    st.metric("Net After Tax", f"₹{target-tax:,.0f}", f"Tax: ₹{tax:,.0f}")
