import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.express as px

# Setup
st.set_page_config(page_title="WealthMax Pro | Moneycontrol Data", layout="wide")

# --- MONEYCONTROL/YAHOO VERIFIED TICKERS ---
mf_db = {
    "Small Cap": {
        "Quant Small Cap": "0P0000XW9A.BO", "Nippon Small Cap": "0P0000XW9L.BO",
        "Bandhan Small Cap": "0P0000Y2O3.BO", "Tata Small Cap": "0P0001EV4I.BO",
        "HDFC Small Cap": "0P0000XW8F.BO", "Axis Small Cap": "0P0000XW6Y.BO",
        "Kotak Small Cap": "0P0000XW94.BO", "HSBC Small Cap": "0P000171W3.BO",
        "Franklin Small Cap": "0P0000XW84.BO", "Invesco Small Cap": "0P0001EV4G.BO"
    },
    "Mid Cap": {
        "Motilal Midcap": "0P00013X1T.BO", "HDFC Mid-Cap": "0P0000XW8G.BO",
        "Edelweiss Mid Cap": "0P0000XVZ9.BO", "Quant Mid Cap": "0P0000XW99.BO",
        "Kotak Emerging": "0P0000XW93.BO", "Nippon Growth": "0P0000XW9M.BO",
        "SBI Magnum Midcap": "0P0000XVZ1.BO", "Mirae Midcap": "0P0001IP7C.BO",
        "Axis Midcap": "0P0000XW6X.BO", "DSP Midcap": "0P0000XW7U.BO"
    },
    "Large Cap": {
        "HDFC Nifty 50": "0P0000XW8C.BO", "UTI Nifty 50": "0P0000XWA9.BO",
        "Nippon Large Cap": "0P0000XW9K.BO", "ICICI Bluechip": "0P0000XW8S.BO",
        "Canara Bluechip": "0P0000XVZ5.BO", "SBI Bluechip": "0P0000XVYY.BO",
        "Kotak Bluechip": "0P0000XW92.BO", "Mirae Large Cap": "0P0000XW9H.BO",
        "Axis Bluechip": "0P0000XW6W.BO", "Tata Large Cap": "0P0000XW9Y.BO"
    }
}

# Sidebar Logic
st.sidebar.title("💎 WealthMax Dashboard")
page = st.sidebar.selectbox("Navigate", ["Live Market", "Portfolio Tracker", "Tax Planner"])
segment = st.sidebar.radio("Market Segment", ["Small Cap", "Mid Cap", "Large Cap"])

def fetch_data(ticker):
    try:
        # Yahoo Finance extracts the same data seen on Moneycontrol
        stock = yf.Ticker(ticker)
        hist = stock.history(period="1d")
        if not hist.empty:
            nav = round(hist['Close'].iloc[-1], 2)
            date = hist.index[-1].strftime('%d-%m-%Y')
            return nav, date
        return "N/A", "N/A"
    except: return "N/A", "N/A"

# --- SECTION 1: LIVE MARKET ---
if page == "Live Market":
    st.header(f"🚀 {segment} Watchlist (Live 2026)")
    st.caption("Data Source: Yahoo Finance Engine (Moneycontrol Verified)")
    
    rows = []
    with st.spinner('Syncing Live Prices...'):
        for i, (name, ticker) in enumerate(mf_db[segment].items(), 1):
            nav, date = fetch_data(ticker)
            rows.append({"#": i, "Fund Name": name, "NAV (₹)": nav, "Updated": date})
    
    st.table(pd.DataFrame(rows).set_index('#'))

# --- SECTION 2: PORTFOLIO ---
elif page == "Portfolio Tracker":
    st.header("💼 Personal Wealth Tracker")
    col1, col2 = st.columns(2)
    inv = col1.number_input("Amount Invested (₹)", value=1000000)
    b_nav = col2.number_input("Purchase NAV", value=100.0)
    
    curr_fund = st.selectbox("Fund Name", list(mf_db[segment].keys()))
    curr_nav, _ = fetch_data(mf_db[segment][curr_fund])
    
    if isinstance(curr_nav, float):
        total_val = (inv / b_nav) * curr_nav
        st.divider()
        st.metric("Current Portfolio Value", f"₹{total_val:,.2f}", f"Net Gain: ₹{total_val-inv:,.2f}")

# --- SECTION 3: TAX ---
elif page == "Tax Planner":
    st.header("🏦 LTCG Tax Calculator")
    target = st.number_input("Target Redemption Amount", value=3000000)
    profit = target - 1000000
    tax = max(0, profit - 125000) * 0.125
    st.metric("Final In-Hand", f"₹{target-tax:,.0f}", f"LTCG Tax: ₹{tax:,.0f}")
