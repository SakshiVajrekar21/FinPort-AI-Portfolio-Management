
def generate_advisory(
    market_prediction,
    portfolio_result
):
    """
    Generate personalised portfolio recommendations
    using ML market predictions and portfolio analytics.
    """

    regime = market_prediction["market_regime"].upper()
    confidence = market_prediction["average_confidence"]

    profile = portfolio_result["risk_profile"].lower()
    status = portfolio_result["status"]

    allocations = portfolio_result["target_allocations"]
    variances = portfolio_result["variance_percentages"]
    orders = portfolio_result["rebalance_orders"]

    recommendations = []
    warnings = []
    insights = []

    # ------------------------------------------------
    # 1. MARKET REGIME ANALYSIS
    # ------------------------------------------------

    if regime == "LOW":
        insights.append(
            "The ML model identifies relatively low "
            "market volatility in the latest observations."
        )

    elif regime == "MEDIUM":
        insights.append(
            "The ML model identifies moderate market "
            "volatility. Monitor changes in market conditions."
        )

    elif regime == "HIGH":
        insights.append(
            "The ML model identifies elevated market "
            "volatility. Portfolio risk deserves additional attention."
        )

    # ------------------------------------------------
    # 2. RISK PROFILE BASED ADVISORY
    # ------------------------------------------------

    if profile == "conservative":

        if regime == "HIGH":
            recommendations.append(
                "Your conservative strategy prioritises capital "
                "preservation. Review your equity exposure carefully."
            )

            warnings.append(
                "Elevated market volatility may create greater "
                "short-term fluctuations in your stock holdings."
            )

        elif regime == "MEDIUM":
            recommendations.append(
                "Continue monitoring equity exposure while "
                "maintaining your conservative allocation strategy."
            )

        else:
            recommendations.append(
                "Current volatility conditions are relatively calm. "
                "Continue following your conservative allocation."
            )

    elif profile == "moderate":

        if regime == "HIGH":
            recommendations.append(
                "Consider reviewing your 50% stock allocation "
                "against your investment horizon and risk tolerance."
            )

            warnings.append(
                "Elevated volatility increases uncertainty "
                "around short-term portfolio movements."
            )

        elif regime == "MEDIUM":
            recommendations.append(
                "Maintain diversification across stocks, debt, "
                "gold and cash while monitoring market volatility."
            )

        else:
            recommendations.append(
                "Current volatility conditions are relatively calm. "
                "Continue monitoring your diversified allocation."
            )

    elif profile == "aggressive":

        if regime == "HIGH":
            recommendations.append(
                "Your aggressive strategy has higher equity exposure. "
                "Monitor volatility and ensure you can tolerate "
                "larger portfolio fluctuations."
            )

            warnings.append(
                "High market volatility can amplify short-term "
                "portfolio losses as well as gains."
            )

        elif regime == "MEDIUM":
            recommendations.append(
                "Continue monitoring your equity-heavy strategy "
                "and maintain your intended diversification."
            )

        else:
            recommendations.append(
                "Market volatility is relatively low. Continue "
                "evaluating your aggressive strategy against "
                "your long-term investment objectives."
            )

    # ------------------------------------------------
    # 3. PORTFOLIO BALANCE ANALYSIS
    # ------------------------------------------------

    if status == "UNBALANCED":

        recommendations.append(
            "Your current portfolio exceeds the permitted "
            "allocation deviation. Review the generated "
            "rebalancing orders."
        )

        for asset, variance in variances.items():

            if abs(variance) > 5:

                direction = (
                    "overweight" if variance > 0
                    else "underweight"
                )

                insights.append(
                    f"{asset} is {direction} by "
                    f"{abs(variance):.2f} percentage points."
                )

    else:
        recommendations.append(
            "Your portfolio is within the specified "
            "5 percentage-point allocation tolerance."
        )

    # ------------------------------------------------
    # 4. ASSET-SPECIFIC ANALYSIS
    # ------------------------------------------------

    for asset, details in orders.items():

        action = details["action"]
        amount = details["amount"]

        if action in ["BUY", "SELL"]:

            recommendations.append(
                f"{action} {asset}: "
                f"{amount:,.2f} to restore the target allocation."
            )

    # ------------------------------------------------
    # 5. MODEL CONFIDENCE
    # ------------------------------------------------

    if confidence < 0.50:
        warnings.append(
            "The model's average prediction confidence is low. "
            "Interpret the market regime cautiously."
        )

    elif confidence < 0.70:
        insights.append(
            "The model has moderate average prediction confidence."
        )

    else:
        insights.append(
            "The model has relatively high average prediction "
            "confidence. This does not guarantee prediction accuracy."
        )

    # ------------------------------------------------
    # 6. FINAL ADVISORY OUTPUT
    # ------------------------------------------------

    return {
        "market_regime": regime,
        "risk_profile": profile.title(),
        "portfolio_status": status,

        "recommendations": recommendations,
        "warnings": warnings,
        "insights": insights,

        "model_confidence": confidence,

        "advisory_summary": (
            f"For a {profile.title()} investor, "
            f"the predicted market regime is {regime} "
            f"and the portfolio status is {status}."
        )
    }
