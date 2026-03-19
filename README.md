#  QuantSim — Algorithmic Trading Terminal

> A quantitative trading research platform built in Python and Streamlit. Simulate, optimise, and stress-test algorithmic trading strategies on synthetic market data — all from an interactive dark-mode terminal interface.

![Python](https://img.shields.io/badge/Python-3.10+-00C896?style=flat&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.0+-00C896?style=flat&logo=streamlit&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-00C896?style=flat)

---

## 📸 Overview

QuantSim is a full-stack quantitative finance simulator that lets you:
- Run algorithmic trading strategies on realistic synthetic price data
- Automatically optimise strategy parameters using grid search
- Stress-test strategies across 100 randomised market scenarios with Monte Carlo simulation
- Visualise results through an interactive terminal-style dashboard

---

## 🚀 Features

| Feature | Description |
|---|---|
| 📈 **MA Crossover** | Golden/death cross strategy with optimisable fast/slow windows |
| 📉 **RSI Strategy** | Mean-reversion using Relative Strength Index |
| 🔍 **Strategy Optimiser** | Grid search across parameters, ranked by Sharpe Ratio |
| 🎲 **Monte Carlo Simulation** | 100 randomised market runs to model outcome distribution |
| 🕯️ **Candlestick Chart** | OHLCV price chart with BUY/SELL markers plotted |
| 📊 **Equity Curve** | Live portfolio value over time with starting capital baseline |
| ⚡ **Kelly Criterion** | Mathematically optimal position sizing |
| 🧮 **Risk Metrics** | Sharpe Ratio, Max Drawdown, Total Return |

---

## 🛠 Installation

**1. Clone the repository**
```bash
git clone https://github.com/Yashas0012/QuantSim-Algorithmic-Trading-Simulator.git
cd QuantSim-Algorithmic-Trading-Simulator
```

**2. Install dependencies**
```bash
pip install streamlit numpy pandas plotly
```

**3. Run the app**
```bash
streamlit run UI/App.py
```

---

## 🎮 How to Use

1. Open the app in your browser at `localhost:8501`
2. Set your **starting capital** in the sidebar
3. Choose a **strategy** — MA Crossover or RSI
4. Click **▶ RUN OPTIMISATION** to find the best parameters and see full results
5. Click **◎ RUN MONTE CARLO** to stress-test across 100 different market scenarios

---

## 📁 Project Structure

```
QuantSim/
├── data/
│   └── generator.py          # GBM synthetic OHLCV price data generator
├── Stratergies/
│   ├── ma_crossover.py       # Moving Average Crossover strategy
│   └── RSI.py                # Relative Strength Index strategy
├── Utils/
│   ├── portfolio.py          # Portfolio state, positions, trade history
│   ├── metrics.py            # Sharpe ratio, max drawdown, total return
│   ├── Backtester.py         # Simulation engine with Kelly position sizing
│   ├── optimiser.py          # Grid search parameter optimiser
│   ├── Monte_Carlo.py        # Monte Carlo simulation engine
│   └── Kelly.py              # Kelly Criterion position sizing
├── UI/
│   └── App.py                # Streamlit terminal dashboard
├── .streamlit/
│   └── config.toml           # Dark theme configuration
├── README.md
└── LICENSE
```

---

## 📐 How It Works

### Data Generation
Synthetic OHLCV price data is generated using **Geometric Brownian Motion** — the same mathematical model used in the Black-Scholes options pricing formula. Regime shifts in volatility and drift create realistic trending and ranging market conditions.

### Strategies

**Moving Average Crossover**
Uses two EMAs — a fast and a slow one. Buys when the fast MA crosses above the slow MA (golden cross) and sells on the reverse (death cross).

**RSI (Relative Strength Index)**
Measures momentum over a rolling window. Buys when RSI drops below 30 (oversold) and sells when RSI rises above 70 (overbought).

### Optimisation
Grid search tests every combination of strategy parameters and ranks them by **Sharpe Ratio** — a risk-adjusted return metric. The best parameters are then used for the full backtest.

### Monte Carlo Simulation
Runs the strategy 100 times across randomly generated market scenarios (different seeds). The distribution of outcomes shows the realistic range of risk and reward — not just one lucky or unlucky result.

### Kelly Criterion
Replaces the naive fixed position size with a mathematically optimal fraction of capital, calculated from historical win rate and average win/loss ratio.

---

## 📊 Metrics Explained

| Metric | Formula | What it means |
|---|---|---|
| Total Return | (final - start) / start | Net % gain or loss |
| Sharpe Ratio | mean(returns) / std(returns) × √252 | Risk-adjusted return |
| Max Drawdown | max peak-to-trough decline | Worst losing streak |

---

## 🧠 Concepts Used

- Geometric Brownian Motion
- Moving Average Crossover
- Relative Strength Index (RSI)
- Grid Search Optimisation
- Monte Carlo Simulation
- Kelly Criterion
- Sharpe Ratio
- Maximum Drawdown

---

## 🛠 Built With

- [Python 3.10+](https://python.org)
- [Streamlit](https://streamlit.io)
- [NumPy](https://numpy.org)
- [Pandas](https://pandas.pydata.org)
- [Plotly](https://plotly.com)

---

## 📄 License

MIT — free to use, modify and distribute.

---

## 👤 Author(Yashas Chopra)

Built as a work experience project whilst at IBM exploring quantitative finance and algorithmic trading.
```
