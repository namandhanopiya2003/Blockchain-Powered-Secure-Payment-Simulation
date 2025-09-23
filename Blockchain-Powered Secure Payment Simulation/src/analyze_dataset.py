import json
import pandas as pd
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parents[1] / "data"
DATA_FILE = DATA_DIR / "ml_dataset.json"

with open(DATA_FILE, "r") as f:
    data = json.load(f)

df = pd.DataFrame(data)

print("\n===== Dataset Overview =====")
print(f"Total samples: {len(df)}")
print(f"Columns: {df.columns.tolist()}")
print("\nSample data:")
print(df.head())

print("\n===== Missing Values =====")
print(df.isnull().sum())

print("\n===== Feature Statistics =====")
print(df.describe())

target_col = "next_interval"
if target_col in df.columns:
    print(f"\n===== Target '{target_col}' Distribution =====")
    print(df[target_col].value_counts())
    print(df[target_col].value_counts(normalize=True)) 

print("\n===== Correlation with Target =====")
print(df.corr()[target_col].sort_values(ascending=False))

print("\n===== Feature Unique Values =====")
for col in df.columns:
    print(f"{col}: {df[col].nunique()} unique values")
