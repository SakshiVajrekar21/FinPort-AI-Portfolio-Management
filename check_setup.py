import sys
import os
import pandas as pd
import numpy as np
import sklearn
import xgboost
import langgraph
import streamlit
import plotly

print("=" * 45)
print("FINANCIAL PORTFOLIO MANAGEMENT")
print("ENVIRONMENT CHECK")
print("=" * 45)

print("Python Version:", sys.version.split()[0])
print("Pandas:", pd.__version__)
print("NumPy:", np.__version__)
print("Scikit-learn:", sklearn.__version__)
print("XGBoost:", xgboost.__version__)

print("\nChecking Dataset Folder...")

data_path = "dataset/raw"

if os.path.exists(data_path):
    files = os.listdir(data_path)

    print("Dataset folder found!")
    print("Files available:")

    for file in files:
        print(" -", file)
else:
    print("Dataset folder not found!")

print("\nEnvironment verification completed!")