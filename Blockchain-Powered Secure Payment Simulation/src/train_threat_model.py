import json
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
import joblib
from pathlib import Path

# Sets the path to the folder where we’ll store and load data
DATA_DIR = Path(__file__).resolve().parents[1] / "data"
# Creates the folder if it doesn’t already exist
DATA_DIR.mkdir(exist_ok=True)

# Opens and loads the dataset from a JSON file
with open(DATA_DIR / "ml_dataset.json", "r") as f:
    data = json.load(f)

# It turns the JSON data into a pandas DataFrame (as it's easier to work with)
df = pd.DataFrame(data)

# Splits the data into:
# - X: the input features (everything except 'next_interval')
# - y: the value we’re trying to predict ('next_interval')
X = df.drop("next_interval", axis=1)
y = df["next_interval"]

# It sets the random seed
np.random.seed(42)
# Makes a copy of the features and add a little bit of random noise
X_noisy = X.copy()
for col in X_noisy.columns:
    if X_noisy[col].dtype in [int, float]:
        noise = np.random.normal(0, 0.01 * X_noisy[col].std(), size=X_noisy.shape[0])
        X_noisy[col] += noise

# Creates the Random Forest model
model = RandomForestClassifier(
    n_estimators=50,
    random_state=42,
    class_weight="balanced",
    oob_score=True,
)
# Trains the model using the noisy input data and the target values
model.fit(X_noisy, y)

# It saves the trained model to a file
joblib.dump(model, DATA_DIR / "threat_model.pkl")

# It prints a confirmation message
print(f"Threat model trained and saved at {DATA_DIR / 'threat_model.pkl'}")
print(f"Out-of-bag score: {model.oob_score_:.4f}")

