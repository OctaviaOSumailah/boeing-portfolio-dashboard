import yfinance as yf
import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
from datetime import datetime, timedelta

# ======================================================
# PAGE CONFIG
# ======================================================

st.set_page_config(
    page_title="Boeing Portfolio Dashboard",
    layout="wide"
)

st.title("Boeing Investment Portfolio Dashboard")
st.markdown("### Boeing (BA) Analytics + Volatility Monitor")

# ======================================================
# PORTFOLIO CONFIGURATION
# ======================================================

TICKER = "BA"

SHARES = 3043
AVG_PURCHASE_PRICE = 230

INITIAL_BA_INVESTMENT = 700000
CASH_BUFFER = 300000

TOTAL_INITIAL_PORTFOLIO = (
    INITIAL_BA_INVESTMENT + CASH_BUFFER
)

# ======================================================
# DATE RANGE
# ======================================================

END_DATE = datetime.today()
START_DATE = END_DATE - timedelta(weeks=6)

# ======================================================
# LOAD DATA
# ======================================================

@st.cache_data
def load_data():

    data = yf.download(
        TICKER,
        start=START_DATE.strftime("%Y-%m-%d"),
        end=(END_DATE + timedelta(days=1)).strftime("%Y-%m-%d"),
        auto_adjust=True,
        progress=False
    )

    return data

ba = load_data()

# ======================================================
# ERROR HANDLING
# ======================================================

if ba.empty:
    st.error("No market data available.")
    st.stop()

# ======================================================
# FIX MULTIINDEX COLUMNS
# ======================================================

if isinstance(ba.columns, pd.MultiIndex):
    ba.columns = [col[0] for col in ba.columns]

# ======================================================
# PORTFOLIO CALCULATIONS
# ======================================================

ba["BA_Position_Value"] = (
    ba["Close"] * SHARES
)

ba["Cash_Buffer"] = CASH_BUFFER

ba["Total_Portfolio_Value"] = (
    ba["BA_Position_Value"] + ba["Cash_Buffer"]
)

# Daily returns
ba["Daily_Return"] = ba["Close"].pct_change()

# Portfolio returns
ba["Portfolio_Return"] = (
    ba["Total_Portfolio_Value"].pct_change()
)

# Gain / Loss
ba["Gain_Loss_Dollar"] = (
    ba["Total_Portfolio_Value"]
    - TOTAL_INITIAL_PORTFOLIO
)

# Cumulative Return %
ba["Cumulative_Return"] = (
    (
        ba["Total_Portfolio_Value"]
        / TOTAL_INITIAL_PORTFOLIO
    ) - 1
) * 100

# ======================================================
# VOLATILITY ANALYSIS
# ======================================================

ba["Rolling_Volatility"] = (
    ba["Daily_Return"]
    .rolling(window=10)
    .std()
    * np.sqrt(252)
) * 100

# Remove NaNs
ba["Rolling_Volatility"] = (
    ba["Rolling_Volatility"].fillna(0)
)

# ======================================================
# PORTFOLIO SNAPSHOT
# ======================================================

latest_price = ba["Close"].iloc[-1]

current_ba_value = (
    latest_price * SHARES
)

current_portfolio_value = (
    current_ba_value + CASH_BUFFER
)

gain_loss = (
    current_portfolio_value
    - TOTAL_INITIAL_PORTFOLIO
)

percent_return = (
    gain_loss / TOTAL_INITIAL_PORTFOLIO
) * 100

current_volatility = (
    ba["Rolling_Volatility"].iloc[-1]
)

# ======================================================
# TOP METRICS
# ======================================================

st.divider()

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "BA Share Price",
    f"${latest_price:,.2f}"
)

col2.metric(
    "Portfolio Value",
    f"${current_portfolio_value:,.2f}"
)

col3.metric(
    "Gain / Loss",
    f"${gain_loss:,.2f}"
)

col4.metric(
    "Portfolio Return",
    f"{percent_return:.2f}%"
)

st.divider()

# ======================================================
# PORTFOLIO VALUE CHART
# ======================================================

st.subheader("Portfolio Value Over 6 Weeks")

fig1 = px.line(
    ba,
    x=ba.index,
    y="Total_Portfolio_Value",
    template="plotly_dark",
    labels={
        "value": "Portfolio Value",
        "index": "Date"
    }
)

fig1.update_layout(
    height=500
)

st.plotly_chart(
    fig1,
    use_container_width=True
)

# ======================================================
# BA SHARE PRICE CHART
# ======================================================

st.subheader("Boeing (BA) Share Price")

fig2 = px.line(
    ba,
    x=ba.index,
    y="Close",
    template="plotly_dark",
    labels={
        "Close": "BA Share Price",
        "index": "Date"
    }
)

fig2.add_hline(
    y=AVG_PURCHASE_PRICE,
    line_dash="dash",
    annotation_text="Average Purchase Price"
)

fig2.update_layout(
    height=500
)

st.plotly_chart(
    fig2,
    use_container_width=True
)

# ======================================================
# VOLATILITY CHART
# ======================================================

st.subheader("Rolling Volatility (10-Day Annualized)")

fig3 = px.line(
    ba,
    x=ba.index,
    y="Rolling_Volatility",
    template="plotly_dark",
    labels={
        "Rolling_Volatility": "Volatility %",
        "index": "Date"
    }
)

fig3.add_hline(
    y=35,
    line_dash="dash",
    annotation_text="Hedge Trigger"
)

fig3.update_layout(
    height=500
)

st.plotly_chart(
    fig3,
    use_container_width=True
)

# ======================================================
# GAIN / LOSS CHART
# ======================================================

st.subheader("Portfolio Gain / Loss")

fig4 = px.line(
    ba,
    x=ba.index,
    y="Gain_Loss_Dollar",
    template="plotly_dark",
    labels={
        "Gain_Loss_Dollar": "Gain / Loss ($)",
        "index": "Date"
    }
)

fig4.add_hline(
    y=0,
    line_dash="dash"
)

fig4.update_layout(
    height=500
)

st.plotly_chart(
    fig4,
    use_container_width=True
)

# ======================================================
# HEDGE MONITOR
# ======================================================

st.subheader("Volatility Hedge Monitor")

if current_volatility > 35:

    st.warning(
        f'''
        Volatility spike detected.

        Current Volatility: {current_volatility:.2f}%

        Suggested hedge:
        - Protective puts
        - Strike price 5–10% below market
        - 30–60 day expiration
        '''
    )

else:

    st.success(
        f'''
        Volatility within acceptable range.

        Current Volatility:
        {current_volatility:.2f}%
        '''
    )

# ======================================================
# POSITION SUMMARY TABLE
# ======================================================

st.subheader("Position Summary")

summary = pd.DataFrame({

    "Metric": [
        "Ticker",
        "Shares Held",
        "Average Purchase Price",
        "Current BA Price",
        "Current Boeing Value",
        "Cash Buffer",
        "Total Portfolio Value",
        "Portfolio Return"
    ],

    "Value": [
        TICKER,
        f"{SHARES:,}",
        f"${AVG_PURCHASE_PRICE:,.2f}",
        f"${latest_price:,.2f}",
        f"${current_ba_value:,.2f}",
        f"${CASH_BUFFER:,.2f}",
        f"${current_portfolio_value:,.2f}",
        f"{percent_return:.2f}%"
    ]
})

st.dataframe(
    summary,
    use_container_width=True
)

# ======================================================
# RAW DATA VIEW
# ======================================================

with st.expander("View Raw Portfolio Data"):

    st.dataframe(
        ba,
        use_container_width=True
    )

# ======================================================
# CSV EXPORT
# ======================================================

csv = ba.to_csv().encode("utf-8")

st.download_button(
    label="Download Portfolio Analytics CSV",
    data=csv,
    file_name="boeing_portfolio_analytics.csv",
    mime="text/csv"
)

# ======================================================
# FOOTER
# ======================================================

st.caption(
    "Boeing Portfolio Dashboard | Streamlit + yFinance + Plotly"
)