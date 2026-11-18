
from src.portfolio_engine import calculate_portfolio

# Test 1: Moderate, no existing holdings
test1 = calculate_portfolio(
    10000,
    "Moderate",
    {}
)

assert test1["target_amounts"] == {
    "Stocks": 5000.0,
    "Debt": 3000.0,
    "Gold": 1000.0,
    "Cash": 1000.0
}

assert test1["target_risk_score"] == 5.5
assert test1["status"] == "BALANCED"


# Test 2: Aggressive, unbalanced portfolio
test2 = calculate_portfolio(
    10000,
    "Aggressive",
    {
        "Stocks": 8000,
        "Debt": 1000,
        "Gold": 500,
        "Cash": 500
    }
)

assert test2["status"] == "UNBALANCED"
assert test2["target_risk_score"] == 7.0
assert test2["current_risk_score"] == 7.6

assert test2["rebalance_orders"]["Stocks"] == {
    "action": "SELL",
    "amount": 1000.0
}

assert test2["rebalance_orders"]["Debt"] == {
    "action": "BUY",
    "amount": 500.0
}


# Test 3: Conservative, balanced portfolio
test3 = calculate_portfolio(
    20000,
    "Conservative",
    {
        "Stocks": 4400,
        "Debt": 9600,
        "Gold": 3000,
        "Cash": 3000
    }
)

assert test3["status"] == "BALANCED"

print("All portfolio engine tests passed!")
