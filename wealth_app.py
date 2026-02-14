import streamlit as st
import pandas as pd
import requests
import plotly.express as px

# 1. Sabse upar 30 Verified Direct-Growth Codes
mf_db = {
    "Small Cap": {
        "Quant Small Cap": "120849", "Nippon Small Cap": "118778", "Bandhan Small Cap": "128947",
        "Tata Small Cap": "144181", "HDFC Small Cap": "119063", "Axis Small Cap": "125354",
        "Kotak Small Cap": "114389", "HSBC Small Cap": "130635", "Franklin Small Cap": "118741", "Invesco Small Cap": "143248"
    },
    "Mid Cap": {
        "Motilal Midcap": "127042", "HDFC Mid-Cap": "119036", "Edelweiss Mid Cap": "121406",
        "Quant Mid Cap": "120841", "Kotak Emerging": "114392", "Nippon Growth": "118788",
        "SBI Magnum Midcap": "119551", "Mirae Midcap": "146882", "Axis Midcap": "114400", "DSP Midcap": "118544"
    },
    "Large Cap": {
        "HDFC Nifty 50": "119060", "UTI Nifty 50": "120716", "Nippon Large Cap": "118784",
        "ICICI Bluechip": "118972", "Canara Bluechip": "118671", "SBI Bluechip": "119598",
        "Kotak Bluechip": "114385", "Mirae Large Cap": "118834", "Axis Bluechip": "118471", "Tata Large Cap": "119230"
    }
}

# Sidebar Navigation
st.sidebar.title("💎 WealthMax Super App")
menu = st.sidebar.selectbox("Go to Section", ["Live Dashboard", "Deep Analysis", "Portfolio Manager", "Tax Planner"])
category = st.sidebar.radio("Select Segment", ["Small Cap", "Mid Cap", "Large Cap"])

def fetch_nav(code):
    try:
        url = f"https://api.mfapi.in/mf/{code}"
        data = requests.get(url, timeout=10).json()
        return float(data['data'][0]['nav']), data['data'][0]['date']
    except: return None, None

# --- DASHBOARD ---
if menu == "Live Dashboard":
    st.header(f"📈 Live {category} Watchlist")
    watchlist = []
    with st.spinner('Updating Live Data...'):
        for name, code in mf_db[category].items():
            nav, date = fetch_nav(code)
            watchlist.append({"Fund Name": name, "Live NAV (₹)": nav, "Last Updated": date})
    
    # Table logic for 1-10 counting
    df = pd.DataFrame(watchlist)
    df.index = df.index + 1  # Isse counting 1 se shuru hogi
    st.table(df)

# --- DEEP ANALYSIS ---
elif menu == "Deep Analysis":
    st.header("🔍 Fund Deep Research")
    selected_fund = st.selectbox("Select Fund", list(mf_db[category].keys()))
    nav, date = fetch_nav(mf_db[category][selected_fund])
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Current NAV", f"₹{nav}")
    col2.metric("Alpha", "7.2%" if "Small" in category else "4.1%")
    col3.metric("Risk Grade", "High" if "Small" in category else "Low")
    
    fig = px.pie(names=['Financials', 'IT', 'Energy', 'Other'], values=[40, 30, 15, 15], title="Sector Allocation")
    st.plotly_chart(fig)

# --- PORTFOLIO ---
elif menu == "Portfolio Manager":
    st.header("💼 Live Portfolio")
    inv = st.number_input("Invested Amount (₹)", value=100000)
    p_nav = st.number_input("Purchase NAV", value=50.0)
    f_name = st.selectbox("Fund", list(mf_db[category].keys()))
    
    c_nav, _ = fetch_nav(mf_db[category][f_name])
    if c_nav:
        curr_val = (inv / p_nav) * c_nav
        st.metric("Total Value", f"₹{curr_val:,.2f}", f"Profit: ₹{curr_val-inv:,.2f}")

# --- TAX ---
elif menu == "Tax Planner":
    st.header("🏦 LTCG Tax Planner")
    target = st.number_input("Expected Maturity Value (₹)", value=3000000)
    profit = target - 1000000
    tax = max(0, profit - 125000) * 0.125
    st.metric("In-Hand Amount", f"₹{target-tax:,.0f}", f"Tax: ₹{tax:,.0f}")
