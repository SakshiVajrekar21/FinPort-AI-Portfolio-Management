
from src.advisory_engine import generate_advisory


mock_portfolio = {
    "risk_profile": "Conservative",
    "status": "BALANCED",

    "target_allocations": {
        "Stocks": 20,
        "Debt": 50,
        "Gold": 15,
        "Cash": 15
    },

    "variance_percentages": {
        "Stocks": 0,
        "Debt": 0,
        "Gold": 0,
        "Cash": 0
    },

    "rebalance_orders": {
        "Stocks": {"action": "HOLD", "amount": 0},
        "Debt": {"action": "HOLD", "amount": 0},
        "Gold": {"action": "HOLD", "amount": 0},
        "Cash": {"action": "HOLD", "amount": 0}
    }
}


market = {
    "market_regime": "HIGH",
    "average_confidence": 0.85
}


result = generate_advisory(
    market,
    mock_portfolio
)

print("ADVISORY ENGINE TEST")
print("====================")

print(result["advisory_summary"])

print("\nRecommendations:")
for item in result["recommendations"]:
    print("-", item)

print("\nWarnings:")
for item in result["warnings"]:
    print("-", item)

print("\nInsights:")
for item in result["insights"]:
    print("-", item)
