# ml/dataset_builder.py
import pandas as pd
import glob
from ml.feature_extractor import FeatureExtractor

class DatasetBuilder:
    def __init__(self):
        self.extractor = FeatureExtractor()

    def build(self):
        rows = []

        # raw/*.xlsx を全部読む
        for path in glob.glob("data/raw/*.xlsx"):
            df = pd.read_excel(path)

            # ファイル名からラベルを決定
            level = path.split("/")[-1].replace("_AI開発.xlsx", "")

            for text in df["text"]:
                features = self.extractor.extract(text)
                features["final_level"] = level
                rows.append(features)

        # processed に保存
        out = pd.DataFrame(rows)
        out.to_excel("data/processed/training_data.xlsx", index=False)

        print("training_data.xlsx を生成しました")
