import json
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
import joblib
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parents[1] / "data"
DATA_DIR.mkdir(exist_ok=True)

with open(DATA_DIR / "ml_dataset.json", "r") as f:
    data = json.load(f)

df = pd.DataFrame(data)

X = df.drop("next_interval", axis=1)
y = df["next_interval"]


np.random.seed(42)
X_noisy = X.copy()
for col in X_noisy.columns:
    if X_noisy[col].dtype in [int, float]:
        noise = np.random.normal(0, 0.01 * X_noisy[col].std(), size=X_noisy.shape[0])
        X_noisy[col] += noise


model = RandomForestClassifier(
    n_estimators=50,
    random_state=42,
    class_weight="balanced",
    oob_score=True,
)

model.fit(X_noisy, y)

joblib.dump(model, DATA_DIR / "threat_model.pkl")
print(f"Threat model trained and saved at {DATA_DIR / 'threat_model.pkl'}")
print(f"Out-of-bag score: {model.oob_score_:.4f}")
