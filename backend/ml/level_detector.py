# level_detector.py
import os
import json

class LevelDetector:
    """
    FeatureExtractor が生成した特徴量を使って
    一次判定（専門度）＋二次判定（構造的複雑度）を行い、
    最終レベル（初級〜研究）を返す統合レベル判定器。
    """

    def __init__(self):
        # 専門用語辞書（一次判定で使用）
        self.technical_terms = self.load_json("technical_terms.json")

    # ---------------------------------------------------------
    # JSON ロード
    # ---------------------------------------------------------
    def load_json(self, file_path):
        json_path = os.path.join(os.path.dirname(__file__), file_path)
        with open(json_path, "r", encoding="utf-8") as f:
            return json.load(f)

    # ---------------------------------------------------------
    # 一次判定：専門度（term_density / prereq_score）
    # ---------------------------------------------------------
    def initial_level(self, term_density, prereq_score):
        """
        初級・中級・上級の一次判定。
        FeatureExtractor の term_density / prereq_score を使う。
        """
        if term_density < 0.05 and prereq_score < 2:
            return "beginner"
        elif term_density < 0.15 and prereq_score < 4:
            return "intermediate"
        else:
            return "advanced"

    # ---------------------------------------------------------
    # 二次判定：構造的特徴量（depth / branch / flow / redundancy / cost）
    # ---------------------------------------------------------
    def secondary_level(self, depth, branch, flow, redundancy, cost):
        """
        初級〜研究の二次判定。
        FeatureExtractor の構造系特徴量を使う。
        """

        score = (
            0.30 * depth +
            0.25 * branch +
            0.25 * flow +
           -0.10 * redundancy +
            0.10 * cost
        )

        if score < 0.30:
            return "初級"
        elif score < 0.55:
            return "中級"
        elif score < 0.75:
            return "上級"
        elif score < 0.90:
            return "専門"
        else:
            return "研究"

    # ---------------------------------------------------------
    # 統合判定（一次＋二次）
    # ---------------------------------------------------------
    def detect(self, features):
        """
        FeatureExtractor.extract(text) が返す特徴量 dict を受け取り、
        一次判定＋二次判定を統合して final_level を返す。
        """

        # 一次判定（専門度）
        term_density = features["term_density"]
        prereq_score = features["prereq_score"]
        initial = self.initial_level(term_density, prereq_score)

        # 二次判定（構造的複雑度）
        depth = features["depth"]
        branch = features["branch"]
        flow = features["flow"]
        redundancy = features["redundancy"]
        cost = features["cost"]
        secondary = self.secondary_level(depth, branch, flow, redundancy, cost)

        # 今は二次判定を優先（ML 導入後はここを統合ロジックに変更）
        final_level = secondary

        return {
            "initial_level": initial,
            "secondary_level": secondary,
            "final_level": final_level
        }
