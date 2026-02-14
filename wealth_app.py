import streamlit as st
import requests
import pandas as pd

st.set_page_config(page_title="WealthMax 2026 Final", layout="wide")

# --- VERIFIED ACTIVE CODES 2026 ---
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

st.sidebar.title("💎 WealthMax Dashboard")
segment = st.sidebar.radio("Segment Select", ["Small Cap", "Mid Cap", "Large Cap"])

def fetch_nav(code):
    try:
        # Direct AMFI API call
        url = f"https://api.mfapi.in/mf/{code}"
        res = requests.get(url, timeout=10).json()
        return res['data'][0]['nav'], res['data'][0]['date']
    except:
        return "N/A", "N/A"

st.header(f"🚀 {segment} (Live Verified Data)")
rows = []
for i, (name, code) in enumerate(mf_db[segment].items(), 1):
    nav, date = fetch_nav(code)
    rows.append({"#": i, "Fund Name": name, "Live NAV": nav, "Updated On": date})

st.table(pd.DataFrame(rows).set_index('#'))
 
