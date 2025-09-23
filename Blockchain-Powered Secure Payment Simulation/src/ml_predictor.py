import joblib
import numpy as np

class ThreatPredictor:
    def __init__(self, model_path="../data/threat_model.pkl"):
        self.model = joblib.load(model_path)

    def predict_interval(self, payments_since_last, total_amount, avg_amount, unique_employees, past_attacks):
        X = np.array([[payments_since_last, total_amount, avg_amount, unique_employees, past_attacks]])

        interval = 100
        threat_score = 0.0

        try:
            interval = int(self.model.predict(X)[0])

            if hasattr(self.model, "predict_proba"):
                probs = self.model.predict_proba(X)[0]
                pred_class = interval
                if hasattr(self.model, "classes_"):
                    class_index = list(self.model.classes_).index(pred_class)
                    threat_score = float(probs[class_index])
                else:
                    threat_score = max(probs)
            else:
                threat_score = (interval - 50) / (150 - 50)
                threat_score = min(max(threat_score, 0.0), 1.0)
        except Exception as e:
            print(f"<!> ThreatPredictor error: {e}, using fallback values.")

        return interval, threat_score
