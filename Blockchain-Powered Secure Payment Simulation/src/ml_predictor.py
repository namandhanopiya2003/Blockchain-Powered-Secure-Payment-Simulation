import joblib
import numpy as np

class ThreatPredictor:
    def __init__(self, model_path="../data/threat_model.pkl"):
        # Loads the pre-trained ML model from the given file path
        self.model = joblib.load(model_path)

    def predict_interval(self, payments_since_last, total_amount, avg_amount, unique_employees, past_attacks):
        # It prepares input features as a 2D numpy array
        X = np.array([[payments_since_last, total_amount, avg_amount, unique_employees, past_attacks]])

        # Default interval and threat score if prediction fails
        interval = 100
        threat_score = 0.0

        try:
            # Predicts the next scan interval using the model
            interval = int(self.model.predict(X)[0])
            # If the model supports probability predictions, it calculates threat confidence
            if hasattr(self.model, "predict_proba"):
                probs = self.model.predict_proba(X)[0]
                pred_class = interval
                # If the model knows its possible classes, it finds the one we predicted
                if hasattr(self.model, "classes_"):
                    class_index = list(self.model.classes_).index(pred_class)
                    threat_score = float(probs[class_index])
                else:
                    threat_score = max(probs)
            else:
                # If the model doesn't support probabilities, it estimates a basic threat level from the interval
                threat_score = (interval - 50) / (150 - 50)
                threat_score = min(max(threat_score, 0.0), 1.0)
        except Exception as e:
            # If anything goes wrong, it prints an error and returns fallback values
            print(f"<!> ThreatPredictor error: {e}, using fallback values.")

        # It returns both the interval prediction and the threat confidence score
        return interval, threat_score

