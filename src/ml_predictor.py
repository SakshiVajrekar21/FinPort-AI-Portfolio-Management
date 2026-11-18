
from pathlib import Path
import joblib
import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]

MODEL_PATH = PROJECT_ROOT / "models" / "volatility_model.pkl"

DATA_PATH = (
    PROJECT_ROOT
    / "dataset"
    / "processed"
    / "nifty50_latest_features.csv"
)

REGIMES = ["LOW", "MEDIUM", "HIGH"]


def predict_market_volatility():

    # 1. Check required files
    if not MODEL_PATH.exists():
        raise FileNotFoundError(
            f"Trained model not found: {MODEL_PATH}"
        )

    if not DATA_PATH.exists():
        raise FileNotFoundError(
            f"Inference dataset not found: {DATA_PATH}"
        )

    # 2. Load trained model
    artifact = joblib.load(MODEL_PATH)

    model = artifact["model"]
    features = artifact["feature_columns"]

    # 3. Load market dataset
    data = pd.read_csv(DATA_PATH)

    data["Date"] = pd.to_datetime(
        data["Date"], errors="coerce"
    )

    data[features] = data[features].replace(
        [float("inf"), float("-inf")], float("nan")
    )

    data = data.dropna(
        subset=["Date", "Symbol"] + features
    )

    if data.empty:
        raise ValueError("No valid market records found.")

    # 4. Select latest available observation per stock
    latest_data = (
        data.sort_values("Date")
        .groupby("Symbol")
        .tail(1)
        .copy()
    )

    if latest_data.empty:
        raise ValueError("No latest stock observations found.")

    # 5. Generate individual predictions
    X_latest = latest_data[features]

    predictions = model.predict(X_latest)
    probabilities = model.predict_proba(X_latest)

    classes = list(model.classes_)

    stock_predictions = []

    for index, (_, row) in enumerate(latest_data.iterrows()):

        probability_dict = {
            regime: float(
                probabilities[index][classes.index(regime)]
            )
            if regime in classes else 0.0
            for regime in REGIMES
        }

        predicted_regime = str(predictions[index])

        stock_predictions.append({
            "symbol": str(row["Symbol"]),
            "date": row["Date"].strftime("%Y-%m-%d"),
            "predicted_regime": predicted_regime,
            "probabilities": {
                regime: round(probability, 4)
                for regime, probability
                in probability_dict.items()
            },
            "confidence": round(
                max(probability_dict.values()), 4
            )
        })

    # 6. Aggregate probabilities across all stocks
    average_probabilities = {
        regime: sum(
            item["probabilities"][regime]
            for item in stock_predictions
        ) / len(stock_predictions)
        for regime in REGIMES
    }

    market_regime = max(
        average_probabilities,
        key=average_probabilities.get
    )

    # 7. Calculate average prediction confidence
    average_confidence = sum(
        item["confidence"]
        for item in stock_predictions
    ) / len(stock_predictions)

    # 8. Prepare final prediction
    return {
        "market_regime": market_regime,

        "stocks_analysed": len(stock_predictions),

        "latest_market_date": max(
            item["date"] for item in stock_predictions
        ),

        "average_confidence": round(
            average_confidence, 4
        ),

        "regime_distribution": {
            regime: round(
                average_probabilities[regime] * 100, 2
            )
            for regime in REGIMES
        },

        "stock_predictions": stock_predictions
    }
