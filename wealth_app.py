import streamlit as st
import pandas as pd
import yfinance as yf
import requests

st.set_page_config(page_title="WealthMax 2026 Final", layout="wide")

# --- TICKER & AMFI HYBRID DATABASE ---
mf_db = {
    "Small Cap": {
        "Quant Small Cap": ["0P0000XW9A.BO", "120849"], "Nippon Small Cap": ["0P0000XW9L.BO", "118778"],
        "Bandhan Small Cap": ["0P0000Y2O3.BO", "128947"], "Tata Small Cap": ["0P0001EV4I.BO", "144181"],
        "HDFC Small Cap": ["0P0000XW8F.BO", "119063"], "Axis Small Cap": ["0P0000XW6Y.BO", "125354"],
        "Kotak Small Cap": ["0P0000XW94.BO", "114389"], "HSBC Small Cap": ["0P000171W3.BO", "130635"],
        "Franklin Small Cap": ["0P0000XW84.BO", "118741"], "Invesco Small Cap": ["0P0001EV4G.BO", "143248"]
    },
    "Mid Cap": {
        "Motilal Midcap": ["0P00013X1T.BO", "127042"], "HDFC Mid-Cap": ["0P0000XW8G.BO", "119036"],
        "Edelweiss Mid Cap": ["0P0000XVZ9.BO", "121406"], "Quant Mid Cap": ["0P0000XW99.BO", "120841"],
        "Kotak Emerging": ["0P0000XW93.BO", "114392"], "Nippon Growth": ["0P0000XW9M.BO", "118788"],
        "SBI Magnum Midcap": ["0P0000XVZ1.BO", "119551"], "Mirae Midcap": ["0P0001IP7C.BO", "146882"],
        "Axis Midcap": ["0P0000XW6X.BO", "114400"], "DSP Midcap": ["0P0000XW7U.BO", "118544"]
    },
    "Large Cap": {
        "HDFC Nifty 50": ["0P0000XW8C.BO", "119060"], "UTI Nifty 50": ["0P0000XWA9.BO", "120716"],
        "Nippon Large Cap": ["0P0000XW9K.BO", "118784"], "ICICI Bluechip": ["0P0000XW8S.BO", "118972"],
        "Canara Bluechip": ["0P0000XVZ5.BO", "118671"], "SBI Bluechip": ["0P0000XVYY.BO", "119598"],
        "Kotak Bluechip": ["0P0000XW92.BO", "114385"], "Mirae Large Cap": ["0P0000XW9H.BO", "118834"],
        "Axis Bluechip": ["0P0000XW6W.BO", "118471"], "Tata Large Cap": ["0P0000XW9Y.BO", "119230"]
    }
}

st.sidebar.title("💎 WealthMax Dashboard")
segment = st.sidebar.radio("Market Segment", ["Small Cap", "Mid Cap", "Large Cap"])
page = st.sidebar.selectbox("Go to", ["Live Watchlist", "Portfolio Tracker", "Tax Planner"])

def fetch_data(ticker, amfi):
    # Try Yahoo First (Live 2026)
    try:
        data = yf.Ticker(ticker).history(period="1d")
        if not data.empty:
            return round(data['Close'].iloc[-1], 2), data.index[-1].strftime('%d-%m-%Y')
    except: pass
    # Backup: AMFI API
    try:
        res = requests.get(f"https://api.mfapi.in/mf/{amfi}", timeout=10).json()
        return float(res['data'][0]['nav']), res['data'][0]['date']
    except: return "Updating", "Wait"

if page == "Live Watchlist":
    st.header(f"🚀 {segment} (Verified 2026)")
    rows = []
    with st.spinner('Syncing Multi-Source Data...'):
        for i, (name, codes) in enumerate(mf_db[segment].items(), 1):
            nav, date = fetch_data(codes[0], codes[1])
            rows.append({"#": i, "Fund Name": name, "NAV (₹)": nav, "Updated": date})
    st.table(pd.DataFrame(rows).set_index('#'))

elif page == "Portfolio Tracker":
    st.header("💼 Wealth Tracker")
    inv = st.number_input("Invested Amount (₹)", value=100000)
    b_nav = st.number_input("Buy NAV", value=100.0)
    sel = st.selectbox("Fund", list(mf_db[segment].keys()))
    nav, _ = fetch_data(mf_db[segment][sel][0], mf_db[segment][sel][1])
    if isinstance(nav, (float, int)):
        val = (inv / b_nav) * nav
        st.metric("Current Value", f"₹{val:,.2f}", f"Gain: ₹{val-inv:,.2f}")

elif page == "Tax Planner":
    st.header("🏦 LTCG Tax Calculator")
    target = st.number_input("Target Amount", value=3000000)
    profit = target - 1000000
    tax = max(0, profit - 125000) * 0.125
    st.metric("Net After Tax", f"₹{target-tax:,.0f}", f"Tax: ₹{tax:,.0f}")
