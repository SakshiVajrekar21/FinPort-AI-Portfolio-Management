
import sys
from pathlib import Path

import streamlit as st
import plotly.express as px
import pandas as pd

# Add project root to Python's import path
PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from src.graph_workflow import run_portfolio_analysis


st.set_page_config(
    page_title="AI Portfolio Manager",
    page_icon="📈",
    layout="wide"
)

st.title("FinPort")
st.caption(
    "Machine Learning | Financial Analytics | LangGraph"
)

st.markdown(
    "Analyse market volatility, calculate portfolio allocations "
    "and generate rebalancing recommendations."
)

st.divider()

# ---------------- USER INPUTS ----------------

st.subheader("1. Portfolio Configuration")

col1, col2 = st.columns(2)

with col1:
    capital = st.number_input(
        "Total Investment Capital",
        min_value=0.0,
        value=10000.0,
        step=500.0
    )

with col2:
    risk_profile = st.selectbox(
        "Select Risk Profile",
        ["Conservative", "Moderate", "Aggressive"]
    )

st.subheader("2. Current Portfolio Holdings")

st.caption(
    "Enter the current amount invested in each asset. "
    "Leave an asset at zero if you do not hold it."
)

col1, col2, col3, col4 = st.columns(4)

with col1:
    stocks = st.number_input(
        "Stocks", min_value=0.0, value=0.0
    )

with col2:
    debt = st.number_input(
        "Debt", min_value=0.0, value=0.0
    )

with col3:
    gold = st.number_input(
        "Gold", min_value=0.0, value=0.0
    )

with col4:
    cash = st.number_input(
        "Cash", min_value=0.0, value=0.0
    )

holdings = {
    "Stocks": stocks,
    "Debt": debt,
    "Gold": gold,
    "Cash": cash
}

if sum(holdings.values()) > capital:
    st.error("Your current holdings exceed your total capital.")

analyse = st.button(
    "Analyse My Portfolio",
    type="primary",
    use_container_width=True
)

# ---------------- ANALYSIS ----------------

if analyse:
    if sum(holdings.values()) > capital:
        st.error("Please correct your holdings before continuing.")

    else:
        with st.spinner(
            "Running machine learning and portfolio analysis..."
        ):
            try:
                result = run_portfolio_analysis(
                    capital=capital,
                    risk_profile=risk_profile,
                    current_holdings=holdings
                )

                if result.get("error"):
                    st.error(result["error"])

                else:
                    report = result["final_report"]
                    market = report["market"]
                    portfolio = report["portfolio"]
                    advisory = report["advisory"]

                    st.success(report["message"])
                    # AI ADVISORY
                    st.divider()
                    st.subheader("AI-Powered Portfolio Advisory")

                    st.info(advisory["advisory_summary"])

                    col1, col2 = st.columns(2)

                    col1.metric(
                        "Model Confidence",
                        f'{advisory["model_confidence"] * 100:.2f}%'
                    )

                    col2.metric(
                        "Portfolio Status",
                        advisory["portfolio_status"]
                    )

                    st.markdown("#### Recommendations")

                    for recommendation in advisory["recommendations"]:
                        st.write("•", recommendation)

                    st.markdown("#### Insights")

                    for insight in advisory["insights"]:
                        st.write("•", insight)

                    if advisory["warnings"]:
                        st.markdown("#### Warnings")

                        for warning in advisory["warnings"]:
                            st.warning(warning)

                    # MARKET PREDICTION
                    st.divider()
                    st.subheader("3. Historical ML Market Volatility Analysis")
                    st.warning(
                        "The model uses historical NIFTY 50 data ending on "
                        "30 April 2021. Predictions represent historical data "
                        "analysis, not current market conditions."
                    )

                    col1, col2, col3 = st.columns(3)

                    col1.metric(
                        "Predicted Market Regime",
                        market["market_regime"]
                    )

                    col2.metric(
                        "Stocks Analysed",
                        market["stocks_analysed"]
                    )

                    col3.metric(
                        "Latest Dataset Date",
                        market["latest_market_date"]
                    )

                    st.write("Predicted regime distribution")

                    regime_data = pd.DataFrame({
                        "Regime": list(
                            market["regime_distribution"].keys()
                        ),
                        "Proportion": list(
                            market["regime_distribution"].values()
                        )
                    })

                    fig = px.bar(
                        regime_data,
                        x="Regime",
                        y="Proportion",
                        title="Predicted Volatility Distribution",
                        text_auto=".1%"
                    )

                    st.plotly_chart(fig, use_container_width=True)
                    # INDIVIDUAL STOCK PREDICTIONS
                    st.markdown("#### Individual Stock Volatility Predictions")

                    stock_predictions = market.get("stock_predictions", [])

                    if stock_predictions:
                        stock_df = pd.DataFrame(stock_predictions)

                        stock_df["confidence"] = (
                            stock_df["confidence"] * 100
                        ).round(2)

                        stock_df = stock_df.rename(columns={
                            "symbol": "Stock Symbol",
                            "date": "Prediction Date",
                            "predicted_regime": "Predicted Volatility",
                            "confidence": "Confidence (%)"
                        })

                        st.dataframe(
                            stock_df[
                                [
                                    "Stock Symbol",
                                    "Prediction Date",
                                    "Predicted Volatility",
                                    "Confidence (%)"
                                ]
                            ],
                            hide_index=True,
                            use_container_width=True
                        )

                    else:
                        st.info("No individual stock predictions available.")

                    # PORTFOLIO ALLOCATION
                    st.divider()
                    st.subheader("4. Target Portfolio Allocation")

                    allocation_data = pd.DataFrame({
                        "Asset": list(
                            portfolio["target_allocations"].keys()
                        ),
                        "Allocation (%)": list(
                            portfolio["target_allocations"].values()
                        )
                    })

                    fig = px.pie(
                        allocation_data,
                        names="Asset",
                        values="Allocation (%)",
                        title="Recommended Asset Allocation",
                        hole=0.4
                    )

                    st.plotly_chart(fig, use_container_width=True)

                    st.dataframe(
                        pd.DataFrame({
                            "Asset": list(
                                portfolio["target_amounts"].keys()
                            ),
                            "Target Amount": list(
                                portfolio["target_amounts"].values()
                            ),
                            "Current Amount": list(
                                portfolio["current_amounts"].values()
                            ),
                            "Variance (%)": list(
                                portfolio["variance_percentages"].values()
                            )
                        }),
                        hide_index=True,
                        use_container_width=True
                    )

                    # RISK
                    st.divider()
                    st.subheader("5. Portfolio Risk Analysis")

                    col1, col2 = st.columns(2)

                    col1.metric(
                        "Target Portfolio Risk",
                        f'{portfolio["target_risk_score"]:.2f} / 10'
                    )

                    col2.metric(
                        "Current Portfolio Risk",
                        f'{portfolio["current_risk_score"]:.2f} / 10'
                    )

                    # REBALANCING
                    st.divider()
                    st.subheader("6. Rebalancing Recommendations")

                    status = portfolio["status"]

                    if status == "UNBALANCED":
                        st.warning("Portfolio status: UNBALANCED")
                    else:
                        st.success("Portfolio status: BALANCED")

                    orders = portfolio["rebalance_orders"]

                    order_data = pd.DataFrame([
                        {
                            "Asset": asset,
                            "Action": details["action"],
                            "Amount": details["amount"]
                        }
                        for asset, details in orders.items()
                    ])

                    st.dataframe(
                        order_data,
                        hide_index=True,
                        use_container_width=True
                    )

                    st.info(
                        "Unallocated capital: "
                        f'{portfolio["unallocated_amount"]:.2f}'
                    )

                    st.caption(
                        "This application provides educational portfolio "
                        "analysis, not personalised investment advice."
                    )

            except Exception as exc:
                st.error(f"Analysis failed: {exc}")
