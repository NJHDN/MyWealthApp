import streamlit as st
import pandas as pd
import requests

st.set_page_config(page_title="WealthMax Pro 2026", layout="wide")

# --- 1. MANUALLY VERIFIED DIRECT-GROWTH MASTER CODES (FEB 2026) ---
# These specific IDs are for Direct-Growth variants to avoid old 2013/2017 data.
mf_db = {
    "Small Cap": {
        "Quant Small Cap (D)": "120849", "Nippon Small Cap (D)": "118778", 
        "Bandhan Small Cap (D)": "128947", "Tata Small Cap (D)": "144181", 
        "HDFC Small Cap (D)": "119063", "Axis Small Cap (D)": "125354", 
        "Kotak Small Cap (D)": "114389", "HSBC Small Cap (D)": "130635", 
        "Franklin Small Cap (D)": "118741", "Invesco Small Cap (D)": "143248"
    },
    "Mid Cap": {
        "Motilal Midcap (D)": "127042", "HDFC Mid-Cap Opp (D)": "119036", 
        "Edelweiss Mid Cap (D)": "121406", "Quant Mid Cap (D)": "120841", 
        "Kotak Emerging (D)": "114392", "Nippon Growth (D)": "118788", 
        "SBI Magnum Midcap (D)": "119551", "Mirae Asset Midcap (D)": "146882", 
        "Axis Midcap (D)": "114400", "DSP Midcap (D)": "118544"
    },
    "Large Cap": {
        "HDFC Nifty 50 (D)": "119060", "UTI Nifty 50 (D)": "120716", 
        "Nippon Large Cap (D)": "118784", "ICICI Pru Bluechip (D)": "118972", 
        "Canara Robeco Bluechip (D)": "118671", "SBI Bluechip (D)": "119598", 
        "Kotak Bluechip (D)": "114385", "Mirae Asset Large Cap (D)": "118834", 
        "Axis Bluechip (D)": "118471", "Tata Large Cap (D)": "119230"
    }
}

st.sidebar.title("💎 WealthMax Dashboard")
segment = st.sidebar.radio("Market Segment", ["Small Cap", "Mid Cap", "Large Cap"])

def fetch_nav(code):
    try:
        url = f"https://api.mfapi.in/mf/{code}"
        response = requests.get(url, timeout=15)
        data = response.json()
        # Fetching the very latest available entry (Index 0)
        latest = data['data'][0]
        return float(latest['nav']), latest['date']
    except Exception:
        return "N/A", "N/A"

# --- Main Dashboard ---
st.header(f"🚀 Live {segment} Watchlist")
st.write("Verified Data Source: AMFI India (Direct-Growth Plans)")

watchlist_data = []
with st.spinner(f'Updating {segment} NAVs...'):
    for i, (name, code) in enumerate(mf_db[segment].items(), 1):
        nav, date = fetch_nav(code)
        watchlist_data.append({
            "Rank": i,
            "Fund Name": name,
            "Live NAV (₹)": nav,
            "Update Date": date
        })

df = pd.DataFrame(watchlist_data).set_index("Rank")
st.table(df)

st.info("Tip: If data looks old, click 'Manage app' -> 'Reboot app' to clear system cache.")
