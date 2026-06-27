# Imports
import streamlit as st
import pandas as pd
import plotly.express as px

# Page Configuration
st.set_page_config(
    page_title="Bitcoin Sentiment Dashboard",
    layout="wide"
)
st.title("📈 Bitcoin Trading Sentiment Dashboard")

# Load dataset
@st.cache_data
def load_data():

    sentiment = pd.read_csv("fear_greed_index.csv")
    trades = pd.read_csv("historical_data_sample.csv")

    return sentiment, trades
sentiment, trades = load_data()

# Data Preprocessing

sentiment['date'] = pd.to_datetime(
    sentiment['date']
)

trades['time'] = pd.to_datetime(
    trades['Timestamp'],
    unit='ms'
)

trades['date'] = trades['time'].dt.date

trades['date'] = pd.to_datetime(
    trades['date']
)

# Merge Trading Data with Sentiment Data

df = trades.merge(
    sentiment,
    on="date",
    how="left"
)

# Create Win/Loss Column
df['win'] = df['Closed PnL'] > 0


# Dashboard Metrics

col1, col2, col3, col4 = st.columns(4)


col1.metric(
    "Total Trades",
    len(df)
)


col2.metric(
    "Average PnL",
    round(df["Closed PnL"].mean(), 2)
)


col3.metric(
    "Win Rate",
    str(round(df["win"].mean()*100, 2)) + "%"
)


col4.metric(
    "Avg Trade Size",
    round(df["Size USD"].mean(), 2)
)

# Average PnL by Market Sentiment
pnl_by_sentiment = (
    df.groupby("classification")["Closed PnL"]
    .mean()
    .reset_index()
)


fig = px.bar(
    pnl_by_sentiment,
    x="classification",
    y="Closed PnL",
    title="Average PnL by Market Sentiment",
    color="classification"
)
st.plotly_chart(fig, use_container_width=True)

