# Multi-Asset Tail Risk Modeling
 
A staged risk-modeling study for a 7-asset, multi-class portfolio. We start
from six single-series VaR/ES estimators, backtest them, diagnose where they
break, and incrementally escalate the model — first by introducing a copula
for cross-asset dependence, then by layering EVT on top for the marginal
tails — and re-backtest at each step.
 
## Portfolio
 
| Ticker | Asset class | Weight |
|---|---|---|
| **SPY** | US large-cap equity (S&P 500) | 25% |
| **QQQ** | US growth equity (Nasdaq-100) | 15% |
| **IEF** | US Treasuries (7–10Y) | 20% |
| **TLT** | US Treasuries (20Y+) | 10% |
| **LQD** | US investment-grade corporate bonds | 10% |
| **GLD** | Gold | 10% |
| **VNQ** | US REITs | 10% |
 
Daily adjusted prices pulled from **Yahoo Finance** for **2005–2025**, giving
exposure to Global Financial Crisis (2008), COVID (2020),
and 2022 rates-driven drawdowns within the validation window.

## Methodology

The methodology can be broken down into three stages:
**Stage 1** : We estimate the VaR/ES by treating the portfolio return as a single series, assuming the dependence structure between assets in the portfolio is fixed over time.

**Stage 2** : We examine cross-asset dependence over time and model the dependence with copulas to see if it improves the model.

**Stage 3** : Testing whether modeling the tails using EVT further improves the result.

## Results

### Kupiec / Christoffersen Independence Test Results (Pass Rate)
| Method | Kupiec 95% | Kupiec 99% | Christoffersen 95% |
|---|---|---|---|
| GARCH + HS | _50.28%_ | _55.45%_ | 83.37% |
| GARCH + PG | _49.49%_ | _45.93%_ | 79.21% |
| GARCH + PST | _48.52%_ | _57.95%_ | 81% |
| GARCH + FHS | _95.16%_ | _92.86%_ | 84.25% |
| GARCH + FPST | _76.74%_ | _86.17%_ | 80% |
| GARCH + t-Copula + MC | _92.71%_ | _95.34%_ | 85.73% |
| GARCH + EVT + t-Copula + MC | _88.93%_ | _94.05%_ | 85.49% |

### Basel Traffic Light Results
![images](outputs/basel_traffic_res.png)

## Notebook Walkthrough
 
| # | Notebook | Stage | What it does |
|---|---|---|---|
| 00 | `00_data_pipeline.ipynb` | — | Pull 7 tickers from Yahoo Finance (2005–2025), build log-return + log-loss series |
| 01 | `01_volatility_model.ipynb` | — | Fit GARCH models per asset; check standardized-residual normality |
| 02 | `02_var_es_estimation.ipynb` | **1** | Six single-series VaR/ES estimators: Historical Simulation (HS), Parametric Gaussian (PG), Parametric Student-T (PST), and their GARCH-filtered counterparts (FHS, FPG, FPST) |
| 03 | `03_backtesting.ipynb` | **1** | Rolling backtest for the six baselines (Kupiec / Christoffersen / Basel); surface where each one fails |
| 04 | `04_copula_correlation.ipynb` | **2** | Examine cross-asset dependence over time; fit Gaussian and Student-t copulas; ask whether explicit dependence modeling improves the estimates |
| 05 | `05_evt_tail_modeling.ipynb` | **3** | POT threshold selection (shape stability + mean excess), GPD fit per asset, then the full GARCH + EVT + Student-t copula + Monte Carlo pipeline and its backtest (combined in 03_backtesting.ipynb) |
