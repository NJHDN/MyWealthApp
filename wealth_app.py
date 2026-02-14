import streamlit as st
import pandas as pd
import requests

# Page Config
st.set_page_config(page_title="WealthMax 30 Super App", layout="wide")

# --- 1. TOTAL 30 FUNDS DATABASE (Correct Codes) ---
mf_db = {
    # SMALL CAP (Top 10)
    "Quant Small Cap (D)": "120849", "Nippon Small Cap (D)": "118778", 
    "Bandhan Small Cap (D)": "128947", "Tata Small Cap (D)": "144181", 
    "HDFC Small Cap (D)": "119063", "Axis Small Cap (D)": "125354", 
    "Kotak Small Cap (D)": "114389", "HSBC Small Cap (D)": "130635", 
    "Franklin Small Cap (D)": "118741", "Invesco Small Cap (D)": "143248",
    
    # MID CAP (Top 10)
    "Motilal Midcap (D)": "127042", "HDFC Mid-Cap (D)": "119036", 
    "Edelweiss Mid Cap (D)": "121406", "Quant Mid Cap (D)": "120841", 
    "Kotak Emerging (D)": "114392", "Nippon Growth (D)": "118788", 
    "SBI Magnum Midcap (D)": "119551", "Mirae Midcap (D)": "146882", 
    "Axis Midcap (D)": "114400", "DSP Midcap (D)": "118544",
    
    # LARGE CAP (Top 10)
    "HDFC Nifty 50 (D)": "119060", "UTI Nifty 50 (D)": "120716", 
    "Nippon Large Cap (D)": "118784", "ICICI Bluechip (D)": "118972", 
    "Canara Bluechip (D)": "118671", "SBI Bluechip (D)": "119598", 
    "Kotak Bluechip (D)": "114385", "Mirae Large Cap (D)": "118834", 
    "Axis Bluechip (D)": "118471", "Tata Large Cap (D)": "119230"
}

# --- 2. SIDEBAR LOGIC (Fixes NameError) ---
st.sidebar.title("WealthMax Filters")
category = st.sidebar.selectbox("Choose Category", ["Small Cap", "Mid Cap", "Large Cap"])

# Segment filtering logic
if category == "Small Cap":
    active_funds = dict(list(mf_db.items())[0:10])
elif category == "Mid Cap":
    active_funds = dict(list(mf_db.items())[10:20])
else:
    active_funds = dict(list(mf_db.items())[20:30])

# --- 3. DASHBOARD DISPLAY ---
st.title(f"🚀 {category} Live Performance")
st.info(f"Showing Top 10 funds for {category}. NAV as of latest market close.")

watchlist = []
with st.spinner('Updating NAV from AMFI...'):
    for name, code in active_funds.items():
        try:
            url = f"https://api.mfapi.in/mf/{code}"
            data = requests.get(url, timeout=10).json()
            watchlist.append({
                "Fund Name": name,
                "Live NAV (₹)": float(data['data'][0]['nav']),
                "Update Date": data['data'][0]['date']
            })
        except Exception as e:
            continue

if watchlist:
    df = pd.DataFrame(watchlist)
    st.table(df)
else:
    st.error("Server se connect nahi ho pa raha. Please wait.")

# --- 4. QUICK CALCULATOR ---
st.divider()
st.subheader("🧮 Quick Profit Calculator")
col1, col2 = st.columns(2)
with col1:
    invested = st.number_input("Amount Invested (₹)", value=100000)
with col2:
    selected_mf = st.selectbox("Select Fund for Return Check", list(active_funds.keys()))

st.success("Tip: Check sidebar to switch between Small, Mid, and Large caps.")
