import streamlit as st
import pandas as pd
import requests
import plotly.express as px

# Page Config
st.set_page_config(page_title="WealthMax Super App 2026", layout="wide")

# --- 1. MANUALLY VERIFIED 2026 ACTIVE SCHEME CODES ---
mf_db = {
    "Small Cap": {
        "Quant Small Cap": "120849", "Nippon Small Cap": "118778", "Bandhan Small Cap": "128947",
        "Tata Small Cap": "144181", "HDFC Small Cap": "119063", "Axis Small Cap": "125354",
        "Kotak Small Cap": "114389", "HSBC Small Cap": "130635", "Franklin Small Cap": "118741", "Invesco Small Cap": "143248"
    },
    "Mid Cap": {
        "Motilal Oswal Midcap": "127042", "HDFC Mid-Cap Opp": "119036", "Edelweiss Mid Cap": "121406",
        "Quant Mid Cap": "120841", "Kotak Emerging": "114392", "Nippon India Growth": "118788",
        "SBI Magnum Midcap": "119551", "Mirae Asset Midcap": "146882", "Axis Midcap": "114400", "DSP Midcap": "118544"
    },
    "Large Cap": {
        "HDFC Nifty 50": "119060", "UTI Nifty 50": "120716", "Nippon Large Cap": "118784",
        "ICICI Pru Bluechip": "118972", "Canara Robeco Bluechip": "118671", "SBI Bluechip": "119598",
        "Kotak Bluechip": "114385", "Mirae Large Cap": "118834", "Axis Bluechip": "118471", "Tata Large Cap": "119230"
    }
}

# --- 2. SIDEBAR & NAVIGATION ---
st.sidebar.title("💎 WealthMax 2026")
menu = st.sidebar.selectbox("Go to Section", ["Live Dashboard", "Deep Analysis", "Portfolio Manager", "Tax Planner"])
category = st.sidebar.radio("Select Segment", ["Small Cap", "Mid Cap", "Large Cap"])

def fetch_live_data(code):
    try:
        url = f"https://api.mfapi.in/mf/{code}"
        response = requests.get(url, timeout=12)
        data = response.json()
        # Picking the absolute latest entry from the API
        return float(data['data'][0]['nav']), data['data'][0]['date']
    except:
        return None, None

# --- SECTION 1: LIVE DASHBOARD ---
if menu == "Live Dashboard":
    st.header(f"📈 {category} Top 10 Funds (Live)")
    watchlist = []
    with st.spinner('Syncing Live Data...'):
        for name, code in mf_db[category].items():
            nav, date = fetch_live_data(code)
            watchlist.append({
                "Fund Name": name,
                "Live NAV (₹)": nav,
                "As of Date": date
            })
    
    df = pd.DataFrame(watchlist)
    df.index = range(1, len(df) + 1) # Counting 1 to 10 fix
    st.table(df)

# --- SECTION 2: DEEP ANALYSIS ---
elif menu == "Deep Analysis":
    st.header("🔍 Fund Analysis & Sector Allocation")
    f_name = st.selectbox("Select Fund", list(mf_db[category].keys()))
    nav, date = fetch_live_data(mf_db[category][f_name])
    
    c1, c2, c3 = st.columns(3)
    c1.metric("Live NAV", f"₹{nav}")
    c2.metric("Date", date)
    c3.metric("Risk Grade", "High" if "Small" in category else "Moderate")
    
    fig = px.pie(names=['Banks', 'Tech', 'Auto', 'Energy', 'Others'], values=[35, 25, 15, 15, 10], title="Sector Mix")
    st.plotly_chart(fig)

# --- SECTION 3: PORTFOLIO MANAGER ---
elif menu == "Portfolio Manager":
    st.header("💼 My Real-Time Portfolio")
    inv = st.number_input("Total Invested (₹)", value=1000000)
    buy_nav = st.number_input("Purchase Price (NAV)", value=100.0)
    sel_fund = st.selectbox("Current Fund", list(mf_db[category].keys()))
    live_nav, _ = fetch_live_data(mf_db[category][sel_fund])
    
    if live_nav:
        curr_val = (inv / buy_nav) * live_nav
        st.divider()
        st.metric("Total Value", f"₹{curr_val:,.2f}", f"Profit: ₹{curr_val-inv:,.2f}")

# --- SECTION 4: TAX PLANNER ---
elif menu == "Tax Planner":
    st.header("🏦 Tax & Goal Tracker")
    target_val = st.number_input("Projected Maturity Value (₹)", value=3000000)
    profit = target_val - 1000000
    tax = max(0, profit - 125000) * 0.125
    st.metric("Net In-Hand", f"₹{target_val - tax:,.2f}", f"Estimated Tax: ₹{tax:,.0f}")
