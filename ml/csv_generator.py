# ml/csv_generator.py
import csv
import os

class CSVGenerator:
    """
    新構造用：FeatureExtractor（新）と LevelDetector（新）の
    特徴量を CSV に保存する学習専用ユーティリティ。
    """

    def __init__(self, output_path="training_data.csv"):
        self.output_path = output_path

        # 新構造の特徴量（FeatureExtractor）
        self.headers = [
            "text",
            "depth",
            "branch",
            "flow",
            "redundancy",
            "complexity",
            "term_density",
            "prereq_score",
            "cost",
            "level"   # LevelDetector の最終レベル
        ]

    # ---------------------------------------------------------
    # CSV 初期化（ヘッダー書き込み）
    # ---------------------------------------------------------
    def init_csv(self):
        with open(self.output_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(self.headers)

    # ---------------------------------------------------------
    # 1行追加（特徴量＋レベル）
    # ---------------------------------------------------------
    def append_row(self, text, features, level):
        """
        text: 元の文章
        features: FeatureExtractor.extract(text) の dict
        level: LevelDetector.detect(features) の結果（単一ラベル）
        """

        row = [
            text,
            features["depth"],
            features["branch"],
            features["flow"],
            features["redundancy"],
            features["complexity"],
            features["term_density"],
            features["prereq_score"],
            features["cost"],
            level
        ]

        with open(self.output_path, "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(row)

    # ---------------------------------------------------------
    # 一括生成（文章リスト → CSV）
    # ---------------------------------------------------------
    def generate(self, texts, extractor, detector):
        """
        texts: 学習用文章のリスト
        extractor: FeatureExtractor（新）
        detector: LevelDetector（新）
        """

        self.init_csv()

        for text in texts:
            features = extractor.extract(text)
            level = detector.detect(features)
            self.append_row(text, features, level)

        print(f"CSV 生成完了: {self.output_path}")
