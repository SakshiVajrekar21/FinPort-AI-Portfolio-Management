
from decimal import Decimal, ROUND_HALF_UP

CENT = Decimal("0.01")

ASSETS = ["Stocks", "Debt", "Gold", "Cash"]

ALLOCATIONS = {
    "conservative": {
        "Stocks": 20, "Debt": 50, "Gold": 15, "Cash": 15
    },
    "moderate": {
        "Stocks": 50, "Debt": 30, "Gold": 10, "Cash": 10
    },
    "aggressive": {
        "Stocks": 70, "Debt": 15, "Gold": 10, "Cash": 5
    }
}

RISK_WEIGHTS = {
    "Stocks": 9,
    "Debt": 2,
    "Gold": 4,
    "Cash": 0
}


def money(value):
    return Decimal(str(value)).quantize(
        CENT, rounding=ROUND_HALF_UP
    )


def calculate_portfolio(capital, risk_profile, current_holdings=None):

    try:
        capital = Decimal(str(capital))
    except Exception:
        raise ValueError("Invalid numeric input.")

    if not capital.is_finite():
        raise ValueError("Invalid numeric input.")

    if capital < 0:
        raise ValueError(
            "Capital must be greater than or equal to zero."
        )

    profile = str(risk_profile).strip().lower()

    if profile not in ALLOCATIONS:
        raise ValueError(
            f"Invalid risk profile '{risk_profile}'. "
            "Allowed: Conservative, Moderate, Aggressive."
        )

    current_holdings = current_holdings or {}

    holdings = {}

    for asset in ASSETS:
        try:
            amount = Decimal(str(current_holdings.get(asset, 0)))
        except Exception:
            raise ValueError("Invalid numeric input.")

        if not amount.is_finite() or amount < 0:
            raise ValueError(
                f"Invalid current holding for {asset}."
            )

        holdings[asset] = amount

    total_holdings = sum(holdings.values(), Decimal("0"))

    if total_holdings > capital:
        raise ValueError(
            f"Sum of current holdings ({money(total_holdings)}) "
            f"exceeds total capital ({money(capital)})."
        )

    if capital == 0:
        return {
            "capital": 0.0,
            "risk_profile": profile.title(),
            "target_allocations": {a: 0.0 for a in ASSETS},
            "target_amounts": {a: 0.0 for a in ASSETS},
            "current_amounts": {a: 0.0 for a in ASSETS},
            "current_percentages": {a: 0.0 for a in ASSETS},
            "variance_percentages": {a: 0.0 for a in ASSETS},
            "rebalance_orders": {
                a: {"action": "HOLD", "amount": 0.0}
                for a in ASSETS
            },
            "target_risk_score": 0.0,
            "current_risk_score": 0.0,
            "status": "BALANCED",
            "unallocated_amount": 0.0
        }

    allocation = ALLOCATIONS[profile]

    target_amounts = {
        a: capital * Decimal(str(allocation[a])) / Decimal("100")
        for a in ASSETS
    }

    current_percentages = {
        a: holdings[a] / capital * Decimal("100")
        for a in ASSETS
    }

    variance = {
        a: current_percentages[a] - Decimal(str(allocation[a]))
        for a in ASSETS
    }

    if not current_holdings:
        unbalanced = False
    else:
        unbalanced = any(
            abs(variance[a]) > Decimal("5")
            for a in ASSETS
        )

    orders = {}

    for asset in ASSETS:
        difference = target_amounts[asset] - holdings[asset]

        if not unbalanced or difference == 0:
            action, amount = "HOLD", Decimal("0")
        elif difference > 0:
            action, amount = "BUY", difference
        else:
            action, amount = "SELL", abs(difference)

        orders[asset] = {
            "action": action,
            "amount": float(money(amount))
        }

    target_risk = sum(
        Decimal(str(allocation[a])) *
        Decimal(str(RISK_WEIGHTS[a]))
        for a in ASSETS
    ) / Decimal("100")

    current_risk = sum(
        current_percentages[a] *
        Decimal(str(RISK_WEIGHTS[a]))
        for a in ASSETS
    ) / Decimal("100")

    return {
        "capital": float(money(capital)),
        "risk_profile": profile.title(),

        "target_allocations": {
            a: float(Decimal(str(allocation[a])))
            for a in ASSETS
        },

        "target_amounts": {
            a: float(money(target_amounts[a]))
            for a in ASSETS
        },

        "current_amounts": {
            a: float(money(holdings[a]))
            for a in ASSETS
        },

        "current_percentages": {
            a: float(money(current_percentages[a]))
            for a in ASSETS
        },

        "variance_percentages": {
            a: float(money(variance[a]))
            for a in ASSETS
        },

        "rebalance_orders": orders,

        "target_risk_score": float(money(target_risk)),
        "current_risk_score": float(money(current_risk)),

        "status": "UNBALANCED" if unbalanced else "BALANCED",

        "unallocated_amount": float(
            money(capital - total_holdings)
        )
    }
