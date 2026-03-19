import sys
import os
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
from data.generator import generate_ohlcv
from Stratergies.ma_crossover import ma_crossover
from Stratergies.RSI import RSI
from Utils.optimiser import optimise, param_grid_ma, param_grid_RSI
from Utils.Backtester import run_backtests
from Utils.Monte_Carlo import Monte_Carlo

# -------------------------
# PAGE CONFIG
# -------------------------
st.markdown("<br><br>", unsafe_allow_html=True)
st.set_page_config(page_title="QuantSim Terminal", layout="wide", page_icon="⬡")

# -------------------------
# STYLING
# -------------------------
st.markdown("""
<style>
    body { background-color: #0A0C14; }
    .block-container { padding-top: 1.5rem; }

    .terminal-title {
        font-family: monospace;
        font-size: 2.2rem;
        font-weight: 800;
        color: #00C896;
        letter-spacing: 2px;
    }
    .terminal-sub {
        font-family: monospace;
        font-size: 0.85rem;
        color: #465172;
        margin-top: -12px;
        margin-bottom: 20px;
    }
    .divider {
        border: none;
        border-top: 1px solid #1E2640;
        margin: 10px 0 24px 0;
    }
    .section-header {
        font-family: monospace;
        font-size: 1rem;
        color: #00C896;
        text-transform: uppercase;
        letter-spacing: 3px;
        margin-bottom: 12px;
        margin-top: 28px;
    }
    .metric-card {
        background-color: #121420;
        border: 1px solid #1E2640;
        border-radius: 8px;
        padding: 16px 20px;
        text-align: center;
    }
    .metric-label {
        font-family: monospace;
        font-size: 0.7rem;
        color: #465172;
        text-transform: uppercase;
        letter-spacing: 2px;
    }
    .metric-value {
        font-family: monospace;
        font-size: 1.6rem;
        font-weight: 700;
        color: #DCE1F0;
        margin-top: 4px;
    }
    .metric-value.positive { color: #00C896; }
    .metric-value.negative { color: #FF4646; }
    .signal-badge {
        display: inline-block;
        padding: 3px 10px;
        border-radius: 4px;
        font-family: monospace;
        font-size: 0.75rem;
        font-weight: 700;
        margin-right: 8px;
    }
    .buy-badge { background-color: #0D2E22; color: #00C896; border: 1px solid #00C896; }
    .sell-badge { background-color: #2E0D0D; color: #FF4646; border: 1px solid #FF4646; }
    .total-badge { background-color: #1A1E30; color: #8090B8; border: 1px solid #2E3650; }
    div[data-testid="stDataFrame"] { border: 1px solid #1E2640; border-radius: 8px; }
    div[data-testid="stSidebar"] { background-color: #0D0F1A; border-right: 1px solid #1E2640; }
</style>
""", unsafe_allow_html=True)

# -------------------------
# HEADER
# -------------------------
st.markdown('<div class="terminal-title">⬡ QUANTSIM TERMINAL</div>', unsafe_allow_html=True)
st.markdown('<div class="terminal-sub">ALGORITHMIC TRADING RESEARCH PLATFORM</div>', unsafe_allow_html=True)
st.markdown('<hr class="divider">', unsafe_allow_html=True)

# -------------------------
# SIDEBAR
# -------------------------
st.sidebar.markdown("### ⚙️ PARAMETERS")
st.sidebar.markdown("---")

starting_cash = st.sidebar.number_input(
    "Starting Capital ($)",
    min_value=1000,
    max_value=1000000,
    value=10000,
    step=1000
)

strategy_choice = st.sidebar.selectbox(
    "Strategy",
    ["MA Crossover", "RSI"]
)

st.sidebar.markdown("---")
run_button  = st.sidebar.button("▶ RUN OPTIMISATION", use_container_width=True)
mc_button   = st.sidebar.button("◎ RUN MONTE CARLO",  use_container_width=True)
st.sidebar.markdown("---")
st.sidebar.markdown("""
<div style='font-family:monospace; font-size:0.7rem; color:#465172;'>
QUANTSIM v1.0<br>
Built with Python + Streamlit<br>
</div>
""", unsafe_allow_html=True)

# -------------------------
# DATA
# -------------------------
df = generate_ohlcv()
strategy_func = ma_crossover if strategy_choice == "MA Crossover" else RSI

# -------------------------
# HELPER — dark plotly theme
# -------------------------
PLOT_LAYOUT = dict(
    paper_bgcolor="#0A0C14",
    plot_bgcolor="#0A0C14",
    font=dict(family="monospace", color="#8090B8"),
    xaxis=dict(gridcolor="#1E2640", showgrid=True),
    yaxis=dict(gridcolor="#1E2640", showgrid=True),
    margin=dict(l=40, r=20, t=40, b=40),
)

def metric_card(label, value, positive=None):
    cls = ""
    if positive is True:  cls = "positive"
    if positive is False: cls = "negative"
    return f"""
    <div class="metric-card">
        <div class="metric-label">{label}</div>
        <div class="metric-value {cls}">{value}</div>
    </div>
    """

# -------------------------
# MONTE CARLO
# -------------------------
if mc_button:
    with st.spinner("Running Monte Carlo simulations..."):
        mc_results   = Monte_Carlo(100, strategy_func)
        final_values = [r[0] for r in mc_results]

    st.markdown('<div class="section-header">◎ Monte Carlo Analysis</div>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(metric_card("BEST CASE",  f"${max(final_values):,.2f}",  True),  unsafe_allow_html=True)
    with col2:
        st.markdown(metric_card("WORST CASE", f"${min(final_values):,.2f}",  False), unsafe_allow_html=True)
    with col3:
        avg = sum(final_values) / len(final_values)
        st.markdown(metric_card("AVERAGE",    f"${avg:,.2f}", avg >= starting_cash),  unsafe_allow_html=True)

    fig = px.histogram(
        x=final_values,
        nbins=25,
        title="Distribution of Final Portfolio Values — 100 Simulations",
        labels={"x": "Final Portfolio Value ($)", "y": "Frequency"},
        color_discrete_sequence=["#00C896"],
    )
    fig.update_layout(**PLOT_LAYOUT, title_font_color="#00C896")
    fig.update_traces(marker_line_color="#0A0C14", marker_line_width=1)
    st.plotly_chart(fig, use_container_width=True)

# -------------------------
# OPTIMISATION
# -------------------------
if run_button:
    with st.spinner("Optimising strategy parameters..."):
        param_grid  = param_grid_ma if strategy_choice == "MA Crossover" else param_grid_RSI
        best_params, best_score, results = optimise(strategy_func, df, param_grid)
        best_signals = strategy_func(df, **best_params)
        final_value, equity_curve, total_return, max_dd, sharpe_ratio = run_backtests(
            df, best_signals, starting_cash
        )

    # ── Metrics ──
    st.markdown('<div class="section-header">▶ Optimisation Results</div>', unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(metric_card("FINAL VALUE",    f"${final_value:,.2f}",        final_value >= starting_cash), unsafe_allow_html=True)
    with col2:
        st.markdown(metric_card("TOTAL RETURN",   f"{total_return*100:+.2f}%",   total_return >= 0),            unsafe_allow_html=True)
    with col3:
        st.markdown(metric_card("MAX DRAWDOWN",   f"{max_dd*100:.2f}%",          False),                        unsafe_allow_html=True)
    with col4:
        st.markdown(metric_card("SHARPE RATIO",   f"{sharpe_ratio:.3f}",         sharpe_ratio >= 1),            unsafe_allow_html=True)

    # ── Best params ──
    st.markdown('<div class="section-header">🏆 Best Parameters</div>', unsafe_allow_html=True)
    st.json(best_params)

    # ── Signal counts ──
    n_buy   = len([s for s in best_signals if s == "Buy"])
    n_sell  = len([s for s in best_signals if s == "Sell"])
    n_total = n_buy + n_sell
    st.markdown(f"""
    <span class="signal-badge buy-badge">▲ BUY {n_buy}</span>
    <span class="signal-badge sell-badge">▼ SELL {n_sell}</span>
    <span class="signal-badge total-badge">● TOTAL {n_total}</span>
    """, unsafe_allow_html=True)

    # ── Equity curve ──
    st.markdown('<div class="section-header">📈 Equity Curve</div>', unsafe_allow_html=True)
    fig_eq = go.Figure()
    fig_eq.add_trace(go.Scatter(
        y=equity_curve,
        mode="lines",
        line=dict(color="#00C896", width=2),
        fill="tozeroy",
        fillcolor="rgba(0,200,150,0.05)",
        name="Portfolio Value"
    ))
    fig_eq.add_hline(y=starting_cash, line_dash="dash", line_color="#465172", annotation_text="Starting Capital")
    fig_eq.update_layout(**PLOT_LAYOUT, title="Portfolio Value Over Time")
    st.plotly_chart(fig_eq, use_container_width=True)

    # ── Candlestick ──
    st.markdown('<div class="section-header">🕯️ Price Chart</div>', unsafe_allow_html=True)
    fig_c = go.Figure()
    fig_c.add_trace(go.Candlestick(
        x=df["Date"],
        open=df["Open"], high=df["High"],
        low=df["Low"],   close=df["Close"],
        increasing_line_color="#00C896",
        decreasing_line_color="#FF4646",
        name="Price"
    ))

    # Plot buy/sell markers on chart
    buy_dates  = [df["Date"].iloc[i] for i, s in enumerate(best_signals) if s == "Buy"]
    buy_prices = [df["Low"].iloc[i]  for i, s in enumerate(best_signals) if s == "Buy"]
    sell_dates  = [df["Date"].iloc[i]  for i, s in enumerate(best_signals) if s == "Sell"]
    sell_prices = [df["High"].iloc[i]  for i, s in enumerate(best_signals) if s == "Sell"]

    fig_c.add_trace(go.Scatter(
        x=buy_dates, y=buy_prices,
        mode="markers",
        marker=dict(symbol="triangle-up", size=10, color="#00C896"),
        name="BUY"
    ))
    fig_c.add_trace(go.Scatter(
        x=sell_dates, y=sell_prices,
        mode="markers",
        marker=dict(symbol="triangle-down", size=10, color="#FF4646"),
        name="SELL"
    ))
    fig_c.update_layout(**PLOT_LAYOUT, title="OHLCV Candlestick Chart with Signals")
    fig_c.update_xaxes(rangeslider_visible=False)
    st.plotly_chart(fig_c, use_container_width=True)

    # ── Top results table ──
    st.markdown('<div class="section-header">📊 Parameter Search Results</div>', unsafe_allow_html=True)
    results_sorted = sorted(results, key=lambda x: x["score"], reverse=True)
    results_df = pd.DataFrame([
        {**r["params"], "Sharpe Score": round(r["score"], 4), "Final Value ($)": round(r["final_value"], 2)}
        for r in results_sorted[:5]
    ])
    st.dataframe(results_df, use_container_width=True)