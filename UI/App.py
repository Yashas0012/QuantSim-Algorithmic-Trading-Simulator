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
st.set_page_config(page_title="Quant Trading Simulator", layout="wide")

st.title("📊 Quant Trading Simulator")

# -------------------------
# SIDEBAR SETTINGS
# -------------------------
st.sidebar.header("⚙️ Settings")


starting_cash = st.sidebar.number_input(
    "Starting Cash",
    min_value=1000,
    max_value=1000000,
    value=10000,
    step=1000
)

strategy_choice = st.sidebar.selectbox(
    "Choose Strategy",
    ["MA", "RSI"]
)

run_button = st.sidebar.button("🚀 Run Optimisation")
mc_button = st.sidebar.button("🎲 Run Monte Carlo")

# -------------------------
# DATA
# -------------------------
df = generate_ohlcv()
strategy_func = ma_crossover if strategy_choice == "MA" else RSI

# -------------------------
# MAIN LOGIC
# -------------------------
if mc_button:
    mc_results = Monte_Carlo(100,strategy_func)
    final_values = [r[0] for r in mc_results]
    fig = px.histogram(
        x=final_values,
        nbins=20,
        title="Monte Carlo Distribution of Final Portfolio Values",
        labels={"x": "Final Value ($)"}
    )
    st.plotly_chart(fig)
    col1, col2, col3 = st.columns(3)
    col1.metric(" Best Case", f"${max(final_values):,.2f}")
    col2.metric(" Worst Case", f"${min(final_values):,.2f}")
    col3.metric(" Average", f"${sum(final_values)/len(final_values):,.2f}")


if run_button:

    st.subheader("🔍 Optimisation Results")

    # Select strategy + grid
    if strategy_choice == "MA":
        strategy_func = ma_crossover
        param_grid = param_grid_ma
    else:
        strategy_func = RSI
        param_grid = param_grid_RSI

    # Run optimiser
    best_params, best_score, results = optimise(strategy_func, df, param_grid)

    # Run best strategy again to get equity curve
    best_signals = strategy_func(df, **best_params)
    final_value, equity_curve, total_return, max_dd, sharpe_ratio = run_backtests(
        df, best_signals, starting_cash
    )


    col1, col2, col3, col4 = st.columns(4)

    col1.metric("💰 Final Value", f"${final_value:,.2f}")
    col2.metric("📈 Total Return", f"{total_return*100:.2f}%")
    col3.metric("📉 Max Drawdown", f"{max_dd*100:.2f}%")
    col4.metric("⚡ Sharpe Ratio", f"{sharpe_ratio:.2f}")


    st.subheader("🏆 Best Parameters")
    st.json(best_params)


    st.subheader("📈 Equity Curve")
    st.line_chart(equity_curve)


    st.subheader("📊 Top Results (Preview)")


    results_sorted = sorted(results, key=lambda x: x["score"], reverse=True)
    results_df = pd.DataFrame([
        {**r["params"], "score": r["score"], "final_value": r["final_value"]}
        for r in results_sorted[:5]
    ])
    st.dataframe(results_df)
    st.write("Total signals:", len([s for s in best_signals if s is not None]))
    st.write("Buy signals:", len([s for s in best_signals if s == "Buy"]))
    st.write("Sell signals:", len([s for s in best_signals if s == "Sell"]))
    fig = go.Figure()

    fig.add_trace(go.Candlestick(
        x = df["Date"],
        open = df["Open"],
        high = df["High"],
        low = df["Low"],
        close = df["Close"]
    ))

    st.plotly_chart(fig)

