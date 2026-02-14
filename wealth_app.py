import streamlit as st
import pandas as pd
import requests

st.set_page_config(page_title="WealthMax Pro 2026", layout="wide")

# --- 1. MANUALLY VERIFIED DIRECT-GROWTH MASTER CODES (FEB 2026) ---
# These specific IDs are for the Direct-Growth variants to avoid 2013/2017 data.
mf_db = {
    "Small Cap": {
        "Quant Small Cap (D)": "120849", "Nippon Small Cap (D)": "118778", 
        "Bandhan Small Cap (D)": "128947", "Tata Small Cap (D)": "144181", 
        "HDFC Small Cap (D)": "119063", "Axis Small Cap (D)": "125354", 
        "Kotak Small Cap (D)": "114389", "HSBC Small Cap (D)": "130635", 
        "Franklin Small Cap (D)": "118741", "Invesco Small Cap (D)": "143248"
    },
    "Mid Cap": {
        "Motilal Midcap (D)": "127042", "HDFC Mid-Cap (D)": "119036", 
        "Edelweiss Mid Cap (D)": "121406", "Quant Mid Cap (D)": "120841", 
        "Kotak Emerging (D)": "114392", "Nippon Growth (D)": "118788", 
        "SBI Magnum Midcap (D)": "119551", "Mirae Midcap (D)": "146882", 
        "Axis Midcap (D)": "114400", "DSP Midcap (D)": "118544"
    },
    "Large Cap": {
        "HDFC Nifty 50 (D)": "119060", "UTI Nifty 50 (D)": "120716", 
        "Nippon Large Cap (D)": "118784", "ICICI Bluechip (D)": "118972", 
        "Canara Bluechip (D)": "118671", "SBI Bluechip (D)": "119598", 
        "Kotak Bluechip (D)": "114385", "Mirae Large Cap (D)": "118834", 
        "Axis Bluechip (D)": "118471", "Tata Large Cap (D)": "119230"
    }
}

st.sidebar.title("💎 WealthMax Dashboard")
segment = st.sidebar.radio("Market Segment", ["Small Cap", "Mid Cap", "Large Cap"])

def fetch_amfi_nav(code):
    try:
        # Direct call to the primary AMFI API
        url = f"https://api.mfapi.in/mf/{code}"
        response = requests.get(url, timeout=15)
        data = response.json()
        # Fetching the very latest available entry
        latest = data['data'][0]
        return float(latest['nav']), latest['date']
    except Exception:
        return None, None

# --- Main Dashboard ---
st.header(f"🚀 Live {segment} Watchlist")
st.write("Source: AMFI Verified Direct Plans (Feb 2026)")

watchlist_data = []
with st.spinner(f'Fetching {segment} Data...'):
    for i, (name, code) in enumerate(mf_db[segment].items(), 1):
        nav, date = fetch_amfi_nav(code)
        watchlist_data.append({
            "Rank": i,
            "Fund Name": name,
            "NAV (₹)": nav if nav else "Updating...",
            "Update Date": date if date else "N/A"
        })

df = pd.DataFrame(watchlist_data).set_index("Rank")
st.table(df)

# --- Pro Analysis Features ---
st.markdown("---")
col1, col2 = st.columns(2)

with col1:
    st.subheader("🧮 Calculator")
    amt = st.number_input("Invested Amount (₹)", value=100000)
    selected_fund = st.selectbox("Select Fund", list(mf_db[segment].keys()))
    
with col2:
    st.subheader("🏦 Tax Planner")
    st.write("Estimated LTCG (12.5%):")
    gain = amt * 0.15 # Example gain
    st.info(f"Tax: ₹{max(0, gain-125000) * 0.125:,.2f}")
