import streamlit as st
import pandas as pd
import requests
import plotly.express as px

# Page Setup
st.set_page_config(page_title="WealthMax Pro 2026", layout="wide")

# --- 1. VERIFIED DIRECT-GROWTH CODES (FOR LATEST 2026 DATA) ---
mf_db = {
    "Small Cap": {
        "Quant Small Cap": "120849", "Nippon Small Cap": "118778", "Bandhan Small Cap": "128947",
        "Tata Small Cap": "144181", "HDFC Small Cap": "119063", "Axis Small Cap": "125354",
        "Kotak Small Cap": "114389", "HSBC Small Cap": "130635", "Franklin Small Cap": "118741", "Invesco Small Cap": "143248"
    },
    "Mid Cap": {
        "Motilal Midcap": "127042", "HDFC Mid-Cap Opp": "119036", "Edelweiss Mid Cap": "121406",
        "Quant Mid Cap": "120841", "Kotak Emerging Equity": "114392", "Nippon India Growth": "118788",
        "SBI Magnum Midcap": "119551", "Mirae Asset Midcap": "146882", "Axis Midcap": "114400", "DSP Midcap": "118544"
    },
    "Large Cap": {
        "HDFC Nifty 50 Index": "119060", "UTI Nifty 50 Index": "120716", "Nippon Large Cap": "118784",
        "ICICI Pru Bluechip": "118972", "Canara Robeco Bluechip": "118671", "SBI Bluechip": "119598",
        "Kotak Bluechip": "114385", "Mirae Large Cap": "118834", "Axis Bluechip": "118471", "Tata Large Cap": "119230"
    }
}

# --- 2. SIDEBAR NAVIGATION ---
st.sidebar.title("💎 WealthMax Super App")
menu = st.sidebar.selectbox("Go to Section", ["Live Dashboard", "Deep Analysis", "Portfolio Manager", "Tax Planner"])
category = st.sidebar.radio("Select Segment", ["Small Cap", "Mid Cap", "Large Cap"])

# API Fetch Function
def fetch_nav(code):
    try:
        url = f"https://api.mfapi.in/mf/{code}"
        res = requests.get(url, timeout=10).json()
        return float(res['data'][0]['nav']), res['data'][0]['date']
    except: return None, None

# --- 3. SECTIONS ---
if menu == "Live Dashboard":
    st.header(f"📈 Live {category} Watchlist")
    watchlist = []
    with st.spinner('Fetching Latest 2026 Data...'):
        for name, code in mf_db[category].items():
            nav, date = fetch_nav(code)
            watchlist.append({"Fund Name": name, "Live NAV (₹)": nav, "Last Updated": date})
    
    df = pd.DataFrame(watchlist)
    df.index = df.index + 1 # Counting 1 to 10 fix
    st.table(df)

elif menu == "Deep Analysis":
    st.header("🔍 Fund Health & Risk Check")
    f_name = st.selectbox("Select Fund", list(mf_db[category].keys()))
    nav, date = fetch_nav(mf_db[category][f_name])
    
    c1, c2, c3 = st.columns(3)
    c1.metric("Live NAV", f"₹{nav}")
    c2.metric("Update Date", date)
    c3.metric("Risk Grade", "High" if "Small" in category else "Moderate")
    
    fig = px.pie(names=['Financials', 'IT', 'Energy', 'Other'], values=[35, 25, 20, 20], title="Sector Mix")
    st.plotly_chart(fig)

elif menu == "Portfolio Manager":
    st.header("💼 Live Portfolio Value")
    inv = st.number_input("Amount Invested (₹)", value=100000)
    b_nav = st.number_input("Purchase NAV", value=50.0)
    sel_fund = st.selectbox("Fund", list(mf_db[category].keys()))
    curr_nav, _ = fetch_nav(mf_db[category][sel_fund])
    
    if curr_nav:
        val = (inv / b_nav) * curr_nav
        st.metric("Current Value", f"₹{val:,.2f}", f"Profit: ₹{val-inv:,.2f}")

elif menu == "Tax Planner":
    st.header("🏦 LTCG Tax (Goal ₹30L)")
    target = st.number_input("Target Amount", value=3000000)
    profit = target - 1000000
    tax = max(0, profit - 125000) * 0.125
    st.metric("Net In-Hand", f"₹{target-tax:,.0f}", f"Tax: ₹{tax:,.0f}")
    st.progress(min(target/3000000, 1.0))
