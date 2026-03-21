import sys
sys.path.insert(0, "D:/project_imp")

import streamlit as st
import requests
import pandas as pd

API_BASE = "http://127.0.0.1:8000"

st.set_page_config(page_title="Market Sentiment Dashboard", layout="wide")
st.title("📈 Real-Time Market Sentiment Dashboard")

# fetch tickers
tickers_res = requests.get(f"{API_BASE}/tickers").json()
tickers = tickers_res["tickers"]

# ticker selector
selected = st.selectbox("Select Stock", tickers)

# signal box
signal_res = requests.get(f"{API_BASE}/signal/{selected}").json()
signal = signal_res["signal"]
score = signal["aggregate_score"]
count = signal["count"]

col1, col2, col3 = st.columns(3)
col1.metric("Signal", signal["signal"])
col2.metric("Aggregate Score", round(score, 4))
col3.metric("Data Points", count)

# sentiment data
sentiment_res = requests.get(f"{API_BASE}/sentiment/{selected}").json()
data = sentiment_res["data"]

if data:
    df = pd.DataFrame(data)
    df["fetched_at"] = pd.to_datetime(df["fetched_at"])

    st.subheader(f"Sentiment Breakdown for {selected}")
    label_counts = df["label"].value_counts().reset_index()
    label_counts.columns = ["label", "count"]
    st.bar_chart(label_counts.set_index("label"))

    st.subheader("Recent Items")
    st.dataframe(df[["fetched_at", "source", "label", "score", "text"]].head(20))
else:
    st.warning("No data found for this ticker.")