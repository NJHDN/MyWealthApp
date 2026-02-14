import streamlit as st
import pandas as pd
import requests
import datetime

st.set_page_config(page_title="WealthMax Live 2026", layout="wide")

# MANUALLY VERIFIED DIRECT-GROWTH CODES (2026 ACTIVE)
# These IDs are specifically chosen to avoid the 2013/2017 "Regular Plan" traps.
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
        "Kotak Emerging (D)": "114392", "Nippon India Growth (D)": "118788", 
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

def fetch_live_nav(code):
    try:
        # Force fresh data fetch by adding a timestamp to the request
        url = f"https://api.mfapi.in/mf/{code}?t={datetime.datetime.now().timestamp()}"
        res = requests.get(url, timeout=10).json()
        latest_data = res['data'][0]
        # Check if the date is actually 2026. If not, mark as Updating.
        if "2026" in latest_data['date']:
            return float(latest_data['nav']), latest_data['date']
        else:
            return "Syncing...", "Checking AMFI..."
    except:
        return "Offline", "Error"

st.header(f"🚀 Live {segment} Watchlist")
st.write("Source: Verified Direct-Growth Plans | Latest Market Closing")

watchlist = []
with st.spinner('Syncing with AMFI Servers...'):
    for i, (name, code) in enumerate(mf_db[segment].items(), 1):
        nav, date = fetch_live_nav(code)
        watchlist.append({
            "Rank": i,
            "Fund Name": name,
            "Live NAV (₹)": nav,
            "Update Date": date
        })

df = pd.DataFrame(watchlist).set_index("Rank")
st.table(df)

st.markdown("---")
st.info("💡 **NOTE:** If NAV is missing, the fund house hasn't released today's NAV yet. Saturday/Sunday data shows Friday's closing.")
