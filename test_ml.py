
from src.ml_predictor import predict_market_volatility

result = predict_market_volatility()

print("\nMARKET PREDICTION")
print("========================")

print("Market Regime:", result["market_regime"])
print("Stocks Analysed:", result["stocks_analysed"])
print("Latest Date:", result["latest_market_date"])

print(
    "Average Confidence:",
    result["average_confidence"]
)

print("\nREGIME DISTRIBUTION")

for regime, percentage in result["regime_distribution"].items():
    print(f"{regime}: {percentage}%")

print("\nINDIVIDUAL STOCK PREDICTIONS")

for stock in result["stock_predictions"][:10]:
    print(
        stock["symbol"],
        "|",
        stock["predicted_regime"],
        "| Confidence:",
        stock["confidence"]
    )
