
# FinPort: AI-Based Financial Portfolio Management System

FinPort is an AI-powered financial portfolio management application developed using Python, Machine Learning, LangGraph, and Streamlit.

## Features

- Portfolio allocation based on risk profiles.
- Conservative, Moderate, and Aggressive investment strategies.
- Portfolio risk score calculation.
- Asset allocation and rebalancing recommendations.
- Machine Learning-based historical market volatility analysis.
- Individual stock volatility predictions.
- AI-generated portfolio insights and recommendations.
- Interactive Streamlit dashboard.

## Technology Stack

- Python
- Streamlit
- Pandas and NumPy
- Scikit-learn
- XGBoost
- Joblib
- LangGraph
- Plotly

## Project Structure

```text
Financial_Portfolio_Management/
├── app/
│   └── dashboard.py
├── dataset/
│   └── processed/
├── models/
│   └── volatility_model.pkl
├── notebooks/
├── src/
├── test_advisory.py
├── test_graph.py
├── test_ml.py
├── test_portfolio.py
├── requirements.txt
├── .gitignore
└── README.md
```

## Run Locally

### 1. Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd Financial_Portfolio_Management
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

### 3. Install dependencies

```bash
.venv\Scripts\activate
pip install -r requirements.txt
```

### 4. Run the application

```bash
python -m streamlit run app/dashboard.py
```

The dashboard will open in your browser at the local Streamlit address.

## Historical Data Disclaimer

The Machine Learning model uses historical NIFTY 50 data ending on 30 April 2021. Its volatility analysis is based on historical data and does not represent current market conditions or guaranteed future performance.

## Disclaimer

FinPort is an academic and educational project. Its outputs are for informational purposes only and should not be considered professional financial or investment advice.
