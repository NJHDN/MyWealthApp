import streamlit as st
import pandas as pd
import requests
import plotly.express as px
from datetime import datetime

# App Config
st.set_page_config(page_title="WealthMax Super App 2026", layout="wide", initial_sidebar_state="expanded")

# --- DATA & API FUNCTIONS ---
def get_live_nav(scheme_code):
    try:
        url = f"https://api.mfapi.in/mf/{scheme_code}"
        response = requests.get(url, timeout=10)
        data = response.json()
        return float(data['data'][0]['nav']), data['data'][0]['date']
    except:
        return None, None

mf_db = {
    
    # SMALL CAP (10)
    "Quant Small Cap (D)": "120849", "Nippon Small Cap (D)": "118778", "Bandhan Small Cap (D)": "128947",
    "Tata Small Cap (D)": "144181", "HDFC Small Cap (D)": "119063", "Axis Small Cap (D)": "125354",
    "Kotak Small Cap (D)": "114389", "HSBC Small Cap (D)": "130635", "Franklin Small Cap (D)": "118741", "Invesco Small Cap (D)": "143248",
    # MID CAP (10)
    "Motilal Midcap (D)": "127042", "HDFC Mid-Cap (D)": "119036", "Edelweiss Mid Cap (D)": "121406",
    "Quant Mid Cap (D)": "120841", "Kotak Emerging (D)": "114392", "Nippon Growth (D)": "118788",
    "SBI Magnum Midcap (D)": "119551", "Mirae Midcap (D)": "146882", "Axis Midcap (D)": "114400", "DSP Midcap (D)": "118544",
    # LARGE CAP (10)
    "HDFC Nifty 50 (D)": "119060", "UTI Nifty 50 (D)": "120716", "Nippon Large Cap (D)": "118784",
    "ICICI Bluechip (D)": "118972", "Canara Bluechip (D)": "118671", "SBI Bluechip (D)": "119598",
    "Kotak Bluechip (D)": "114385", "Mirae Large Cap (D)": "118834", "Axis Bluechip (D)": "118471", "Tata Large Cap (D)": "119230"
}

# --- SIDEBAR NAVIGATION ---
st.sidebar.title("WealthMax Filter")
category = st.sidebar.selectbox("Choose Segment", ["Small Cap", "Mid Cap", "Large Cap"])

# Grouping Logic
if category == "Small Cap":
    active_funds = dict(list(mf_db.items())[0:10])
elif category == "Mid Cap":
    active_funds = dict(list(mf_db.items())[10:20])
else:
    active_funds = dict(list(mf_db.items())[20:30])

st.header(f"Live {category} Watchlist")
# --- 1. LIVE DASHBOARD ---
if menu == "Live Dashboard":
    st.header("📈 Live Market Watchlist")
    st.write(f"Latest Updates as of: {datetime.now().strftime('%d %b, %Y')}")
    watchlist = []
    for name, code in mf_db.items():
        nav, date = get_live_nav(code)
        watchlist.append({"Fund Name": name, "Live NAV": nav, "Update Date": date})
    st.table(pd.DataFrame(watchlist))

# --- 2. DEEP ANALYSIS ---
elif menu == "Deep Analysis":
    st.header("🔍 Fund Deep Dive")
    selected_fund = st.selectbox("Select Fund", list(mf_db.keys()))
    # Simulated Deep Metrics for Demo
    col1, col2, col3 = st.columns(3)
    col1.metric("Alpha", "7.8%", "Benchmark +2.1%")
    col2.metric("Sharpe Ratio", "1.65", "High Efficiency")
    col3.metric("Expense Ratio", "0.72%", "Low Cost")
    
    fig = px.pie(names=['Financials', 'IT', 'Energy', 'Others'], values=[40, 25, 20, 15], title="Sector Weights")
    st.plotly_chart(fig)

# --- 3. PORTFOLIO TRACKER ---
elif menu == "Portfolio Tracker":
    st.header("💼 My Live Portfolio")
    amt = st.number_input("Total Invested (₹)", value=1000000)
    buy_nav = st.number_input("Average Buy NAV", value=100.0)
    current_fund = st.selectbox("Link to Fund", list(mf_db.keys()))
    
    curr_nav, _ = get_live_nav(mf_db[current_fund])
    if curr_nav:
        units = amt / buy_nav
        curr_val = units * curr_nav
        profit = curr_val - amt
        st.divider()
        c1, c2 = st.columns(2)
        c1.metric("Current Value", f"₹{curr_val:,.2f}")
        c2.metric("Profit/Loss", f"₹{profit:,.2f}", f"{(profit/amt)*100:.2f}%")

# --- 4. TAX PLANNER ---
elif menu == "Tax Planner":
    st.header("🏦 LTCG Tax Calculator")
    invested = st.number_input("Investment", value=1000000)
    target = st.number_input("Target Value", value=3000000)
    profit = target - invested
    taxable = max(0, profit - 125000)
    tax = taxable * 0.125
    st.metric("Final In-Hand (Post Tax)", f"₹{target - tax:,.2f}", f"Tax: ₹{tax:,.0f}")
    st.progress((target/3000000) if target < 3000000 else 1.0)
    st.write("Target: ₹30 Lakhs Reach Status")
