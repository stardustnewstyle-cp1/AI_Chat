# ml/level_detector_ml.py
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import joblib

class LevelDetectorML:
    def __init__(self):
        self.model = None

    def train(self):
        df = pd.read_excel("data/processed/training_data.xlsx")
        x = df.drop("final_level", axis=1)
        y = df["final_level"]

        x_train, x_test, y_train, y_test = train_test_split(
            x, y, test_size=0.2, random_state=42
        )

        model = RandomForestClassifier()
        model.fit(x_train, y_train)

        pred = model.predict(x_test)
        print("accuracy:", accuracy_score(y_test, pred))

        self.model = model
        joblib.dump(model, "data/models/level_detector.pkl")

    def load(self):
        self.model = joblib.load("data/models/level_detector.pkl")

    def predict(self, features: dict):
        df = pd.DataFrame([features])
        return self.model.predict(df)[0]
