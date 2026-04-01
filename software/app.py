import streamlit as st
import boto3
import pandas as pd
from datetime import timedelta

# --- 1. THE "UNIVERSE" DECORATION (CSS) ---
st.set_page_config(page_title="Sentinel-X: Deep Space", page_icon="🌌", layout="wide")

st.markdown("""
    <style>
    .main {
        background: linear-gradient(to bottom, #000428, #004e92); /* Space Gradient */
        color: white;
    }
    .stButton>button {
        background-color: #4CAF50; /* Green Refresh */
        color: white;
        border-radius: 20px;
        border: 2px solid #fff;
        font-weight: bold;
    }
    .stSelectbox label {
        color: #00d2ff !important;
        font-weight: bold;
    }
    /* Simple glowing border for tables */
    .stTable {
        border: 1px solid #00d2ff;
        border-radius: 10px;
        background-color: rgba(255, 255, 255, 0.05);
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. AWS SETUP ---
ACCESS_KEY = "YOUR_ACCESS_KEY"
SECRET_KEY = "YOUR_SECRET_KEY_HERE"
BUCKET_NAME = "your-sentinel-x-bucket-name"
s3 = boto3.client('s3', aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_KEY)

# --- 3. LOGIC (No Changes) ---
def get_s3_data():
    try:
        response = s3.list_objects_v2(Bucket=BUCKET_NAME)
        if 'Contents' in response:
            data = []
            for obj in response['Contents']:
                ist_time = obj['LastModified'] + timedelta(hours=5, minutes=30)
                data.append({
                    "Incident File": obj['Key'],
                    "Detected At (IST)": ist_time.strftime("%Y-%m-%d %I:%M:%S %p"),
                    "Size": f"{obj['Size']} bytes"
                })
            return pd.DataFrame(data).sort_values(by="Detected At (IST)", ascending=False)
    except: return None
    return None

# --- 4. CHARMING LAYOUT ---
# We use st.columns to put the title and refresh button side-by-side
col1, col2 = st.columns([4, 1])

with col1:
    st.title("🌌 Sentinel-X: Farm Monitor")
    st.caption("Deep Space Edition | Connected to AWS S3 Cloud")

with col2:
    st.write("##") # Add a little space to align with title
    if st.button('🔄 REFRESH'):
        st.rerun()

st.divider()

# --- 5. DATA VIEW ---
df = get_s3_data()

if df is not None:
    st.subheader("🛰️ Live Satellite Logs")
    st.table(df)

    st.markdown("---")
    
    # Selection area with better spacing
    c1, c2 = st.columns([2, 1])
    with c1:
        selected_file = st.selectbox("📂 Select a Transmission to Decode:", df["Incident File"])
    with c2:
        st.write("##")
        view_btn = st.button("🔓 DECODE CONTENT")
    
    if view_btn:
        obj = s3.get_object(Bucket=BUCKET_NAME, Key=selected_file)
        content = obj['Body'].read().decode('utf-8')
        st.success(f"Transmission Decoded: {selected_file}")
        st.code(content, language='text')

else:
    st.warning("Scanning for signals... No data found in S3.")

st.sidebar.markdown("### 🛠️ System Status")
st.sidebar.success("GATEWAY: ONLINE")
st.sidebar.info(f"BUCKET: {BUCKET_NAME}")