# Import tools needed
import json
import pandas as pd
from pathlib import Path

# Sets the path to the folder and the JSON file that has data
DATA_DIR = Path(__file__).resolve().parents[1] / "data"
DATA_FILE = DATA_DIR / "ml_dataset.json"

# Opens the file and read the data from it
with open(DATA_FILE, "r") as f:
    data = json.load(f)

# Puts the data into a table (DataFrame)
df = pd.DataFrame(data)

# Shows some basic info about the data
print("\n===== Dataset Overview =====")
print(f"Total samples: {len(df)}")
print(f"Columns: {df.columns.tolist()}")
print("\nSample data:")
print(df.head())

# Checks if any values are missing
print("\n===== Missing Values =====")
print(df.isnull().sum())

# Shows numbers like average, min, and max for each column
print("\n===== Feature Statistics =====")
print(df.describe())

# This is the column we want to predict
target_col = "next_interval"
if target_col in df.columns:
    print(f"\n===== Target '{target_col}' Distribution =====")
    print(df[target_col].value_counts())
    print(df[target_col].value_counts(normalize=True)) 

# Shows how each column is related to the target column
print("\n===== Correlation with Target =====")
print(df.corr()[target_col].sort_values(ascending=False))

# Shows how many different values each column has
print("\n===== Feature Unique Values =====")
for col in df.columns:
    print(f"{col}: {df[col].nunique()} unique values")

