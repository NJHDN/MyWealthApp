import streamlit as st
import requests
import pandas as pd

# Page Configuration
st.set_page_config(page_title="WealthMax 2026 Final", layout="wide")

# --- 1. MANUALLY VERIFIED DIRECT-GROWTH CODES (FEB 2026 ACTIVE) ---
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
        "HDFC Nifty 50 Index": "119060", "UTI Nifty 50 Index": "120716", "Nippon India Large Cap": "118784",
        "ICICI Pru Bluechip": "118972", "Canara Robeco Bluechip": "118671", "SBI Bluechip": "119598",
        "Kotak Bluechip": "114385", "Mirae Asset Large Cap": "118834", "Axis Bluechip": "118471", "Tata Large Cap": "119230"
    }
}

# --- 2. UI LOGIC ---
st.sidebar.title("💎 WealthMax Dashboard")
# Error Prevention: Explicit variable definition
segment = st.sidebar.radio("Market Segment", ["Small Cap", "Mid Cap", "Large Cap"])

def fetch_nav(code):
    try:
        # Direct API call to get the absolute latest closing price
        url = f"https://api.mfapi.in/mf/{code}"
        res = requests.get(url, timeout=12).json()
        # Always pick index 0 (the most recent day)
        return res['data'][0]['nav'], res['data'][0]['date']
    except:
        return "N/A", "N/A"

st.header(f"🚀 Live {segment} Watchlist")
st.write("Source: AMFI India | Latest Market Closing (Feb 2026)")

# --- 3. DATA RENDERING ---
watchlist = []
with st.spinner('Syncing Verified 2026 Data...'):
    for i, (name, code) in enumerate(mf_db[segment].items(), 1):
        nav, date = fetch_nav(code)
        watchlist.append({
            "Rank": i, 
            "Fund Name": name, 
            "Live NAV (₹)": nav, 
            "Update Date": date
        })

# Displaying as a clean table
df = pd.DataFrame(watchlist).set_index("Rank")
st.table(df)

# Footer Tip
st.info("Tip: If data looks old, please click 'Manage App' -> 'Reboot App' to clear old cache.")
