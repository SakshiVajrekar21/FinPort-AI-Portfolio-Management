
from typing import TypedDict, Optional

from langgraph.graph import StateGraph, START, END

from src.ml_predictor import predict_market_volatility
from src.portfolio_engine import calculate_portfolio
from src.advisory_engine import generate_advisory


class PortfolioState(TypedDict, total=False):

    capital: float
    risk_profile: str
    current_holdings: dict

    market_prediction: dict
    portfolio_result: dict
    advisory_result: dict
    final_report: dict

    error: Optional[str]


# ==========================================
# NODE 1: VALIDATE USER INPUT
# ==========================================

def validate_input(state: PortfolioState):

    try:
        import math

        capital = float(state["capital"])

        if not math.isfinite(capital):
            raise ValueError("Invalid numeric input.")

        if capital < 0:
            raise ValueError(
                "Capital must be greater than or equal to zero."
            )

        profile = str(state["risk_profile"]).strip().lower()

        if profile not in [
            "conservative",
            "moderate",
            "aggressive"
        ]:
            raise ValueError(
                f"Invalid risk profile '{state['risk_profile']}'. "
                "Allowed: Conservative, Moderate, Aggressive."
            )

        holdings = state.get("current_holdings") or {}

        if not isinstance(holdings, dict):
            raise ValueError("Invalid current holdings.")

        total = 0.0

        for asset in ["Stocks", "Debt", "Gold", "Cash"]:

            try:
                amount = float(holdings.get(asset, 0))
            except (ValueError, TypeError):
                raise ValueError("Invalid numeric input.")

            if not math.isfinite(amount):
                raise ValueError("Invalid numeric input.")

            if amount < 0:
                raise ValueError(
                    f"Invalid current holding for {asset}."
                )

            total += amount

        if total > capital:
            raise ValueError(
                f"Sum of current holdings ({total:.2f}) "
                f"exceeds total capital ({capital:.2f})."
            )

        return {"error": None}

    except (KeyError, TypeError, ValueError) as exc:

        return {"error": str(exc)}


# ==========================================
# NODE 2: ML MARKET PREDICTION
# ==========================================

def predict_market(state: PortfolioState):

    try:

        prediction = predict_market_volatility()

        return {
            "market_prediction": prediction,
            "error": None
        }

    except Exception as exc:

        return {
            "error": f"Market prediction failed: {exc}"
        }


# ==========================================
# NODE 3: PORTFOLIO CALCULATION
# ==========================================

def calculate_portfolio_node(state: PortfolioState):

    try:

        result = calculate_portfolio(
            capital=state["capital"],
            risk_profile=state["risk_profile"],
            current_holdings=state.get(
                "current_holdings", {}
            )
        )

        return {
            "portfolio_result": result,
            "error": None
        }

    except Exception as exc:

        return {
            "error": f"Portfolio calculation failed: {exc}"
        }


# ==========================================
# NODE 4: AI ADVISORY ENGINE
# ==========================================

def advisory_node(state: PortfolioState):

    try:

        advisory = generate_advisory(
            market_prediction=state["market_prediction"],
            portfolio_result=state["portfolio_result"]
        )

        return {
            "advisory_result": advisory,
            "error": None
        }

    except Exception as exc:

        return {
            "error": f"Advisory generation failed: {exc}"
        }


# ==========================================
# NODE 5: FINAL REPORT
# ==========================================

def generate_final_report(state: PortfolioState):

    report = {
        "market": state["market_prediction"],
        "portfolio": state["portfolio_result"],
        "advisory": state["advisory_result"],

        "message": (
            "Integrated AI portfolio analysis "
            "completed successfully."
        )
    }

    return {"final_report": report}


# ==========================================
# ROUTING FUNCTIONS
# ==========================================

def route_after_validation(state: PortfolioState):

    if state.get("error"):
        return "error"

    return "predict"


def route_after_prediction(state: PortfolioState):

    if state.get("error"):
        return "error"

    return "calculate"


def route_after_calculation(state: PortfolioState):

    if state.get("error"):
        return "error"

    return "advisory"


def route_after_advisory(state: PortfolioState):

    if state.get("error"):
        return "error"

    return "report"


# ==========================================
# BUILD LANGGRAPH WORKFLOW
# ==========================================

def build_portfolio_graph():

    workflow = StateGraph(PortfolioState)

    workflow.add_node("validate", validate_input)
    workflow.add_node("predict", predict_market)
    workflow.add_node("calculate", calculate_portfolio_node)
    workflow.add_node("advisory", advisory_node)
    workflow.add_node("report", generate_final_report)

    workflow.add_edge(START, "validate")

    workflow.add_conditional_edges(
        "validate",
        route_after_validation,
        {
            "error": END,
            "predict": "predict"
        }
    )

    workflow.add_conditional_edges(
        "predict",
        route_after_prediction,
        {
            "error": END,
            "calculate": "calculate"
        }
    )

    workflow.add_conditional_edges(
        "calculate",
        route_after_calculation,
        {
            "error": END,
            "advisory": "advisory"
        }
    )

    workflow.add_conditional_edges(
        "advisory",
        route_after_advisory,
        {
            "error": END,
            "report": "report"
        }
    )

    workflow.add_edge("report", END)

    return workflow.compile()


# Compile application
portfolio_app = build_portfolio_graph()


# ==========================================
# PUBLIC FUNCTION
# ==========================================

def run_portfolio_analysis(
    capital,
    risk_profile,
    current_holdings=None
):

    initial_state = {
        "capital": capital,
        "risk_profile": risk_profile,
        "current_holdings": current_holdings or {},
        "error": None
    }

    return portfolio_app.invoke(initial_state)
