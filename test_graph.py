
from src.graph_workflow import run_portfolio_analysis


result = run_portfolio_analysis(
    capital=10000,
    risk_profile="Conservative",
    current_holdings={
        "Stocks": 2000,
        "Debt": 5000,
        "Gold": 1500,
        "Cash": 1500
    }
)


if result.get("error"):
    print("ERROR:", result["error"])

else:

    report = result["final_report"]

    print("\n========== MARKET PREDICTION ==========")

    print(
        "Market Regime:",
        report["market"]["market_regime"]
    )

    print(
        "Confidence:",
        report["market"]["average_confidence"]
    )

    print("\n========== PORTFOLIO ANALYSIS ==========")

    print(
        "Risk Profile:",
        report["portfolio"]["risk_profile"]
    )

    print(
        "Portfolio Status:",
        report["portfolio"]["status"]
    )

    print(
        "Target Risk:",
        report["portfolio"]["target_risk_score"]
    )

    print("\n========== AI ADVISORY ==========")

    advisory = report["advisory"]

    print(advisory["advisory_summary"])

    print("\nRecommendations:")

    for item in advisory["recommendations"]:
        print("-", item)

    print("\nWarnings:")

    for item in advisory["warnings"]:
        print("-", item)

    print("\nInsights:")

    for item in advisory["insights"]:
        print("-", item)
