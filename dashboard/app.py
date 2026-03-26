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

# price chart
st.subheader(f"Stock Price — {selected} (Last 14 Days)")
price_res = requests.get(f"{API_BASE}/prices/{selected}").json()
prices = price_res["prices"]

if prices:
    price_df = pd.DataFrame(prices).set_index("date")
    st.line_chart(price_df["close"])
else:
    st.info("No price data available.")

st.divider()

# daily sentiment chart
st.subheader(f"Daily Sentiment Score — {selected}")
daily_res = requests.get(f"{API_BASE}/daily_sentiment/{selected}").json()
daily_sentiment = daily_res["data"]

if daily_sentiment:
    sent_df = pd.DataFrame(daily_sentiment).set_index("date")
    st.line_chart(sent_df["daily_score"])
    st.caption("Score ranges from -1 (bearish) to +1 (bullish)")
else:
    st.info("No sentiment trend data yet. Keep the scheduler running.")

st.divider()

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


st.divider()

# study section
st.subheader(f"Sentiment Study — {selected}")

study_res = requests.get(f"{API_BASE}/study/{selected}").json()
study_data = study_res["data"]

if study_data:
    study_df = pd.DataFrame(study_data)
    
    # sentiment score trend per run
    st.markdown("**Sentiment Score Over Time**")
    chart_df = study_df[["date", "time_of_day", "sentiment_score"]].copy()
    chart_df["datetime"] = chart_df["date"] + " (" + chart_df["time_of_day"] + ")"
    chart_df = chart_df.set_index("datetime")
    st.line_chart(chart_df["sentiment_score"])
    
    # signal distribution
    st.markdown("**Signal Distribution**")
    signal_counts = study_df["signal"].value_counts().reset_index()
    signal_counts.columns = ["signal", "count"]
    st.bar_chart(signal_counts.set_index("signal"))
    
    # raw study table
    st.markdown("**Raw Study Data**")
    st.dataframe(study_df)
else:
    st.info("Study data will appear here as the scheduler collects data over multiple days.")
