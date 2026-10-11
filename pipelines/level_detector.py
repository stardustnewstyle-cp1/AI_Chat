# level_detector.py
import json
import os

class LevelDetectorUnified:
    def __init__(self):
        # 一次判定（専門度）で使う辞書
        self.technical_terms = self.load_json("technical_terms.json")

    # -----------------------------
    # JSON ロード
    # -----------------------------
    def load_json(self, file_path):
        json_path = os.path.join(os.path.dirname(__file__), file_path)
        with open(json_path, "r") as f:
            return json.load(f)

    # -----------------------------
    # 一次判定：専門用語密度
    # -----------------------------
    def calculate_term_density(self, text):
        term_density = 0.0
        term_count = 0
        total_words = len(text.split())

        for terms in self.technical_terms.values():
            for term in terms:
                term_count += text.count(term)

        if total_words > 0:
            term_density = term_count / total_words
        return term_density

    # -----------------------------
    # 一次判定：前提知識スコア
    # -----------------------------
    def calculate_prereq_score(self, text):
        # TODO: 必要なら後で拡張
        prereq_score = 0
        return prereq_score

    # -----------------------------
    # 一次レベル判定（初級・中級・上級）
    # -----------------------------
    def initial_level(self, term_density, prereq_score):
        if term_density < 0.05 and prereq_score < 2:
            return "beginner"
        elif term_density < 0.15 and prereq_score < 4:
            return "intermediate"
        else:
            return "advanced"

    # -----------------------------
    # 二次判定：構造的特徴量（depth / branch / flow / redundancy / cost）
    # -----------------------------
    def calc_depth(self, text):
        return min(len(text) / 500, 1.0)

    def calc_branch(self, text):
        keywords = ["if", "else", "elif", "switch", "case", "when"]
        count = sum(text.count(k) for k in keywords)
        return min(count / 10, 1.0)

    def calc_flow(self, text):
        flow_words = ["because", "therefore", "so", "thus", "hence"]
        count = sum(text.count(w) for w in flow_words)
        return min(count / 10, 1.0)

    def calc_redundancy(self, text):
        words = text.split()
        unique = len(set(words))
        if len(words) == 0:
            return 0
        return 1 - (unique / len(words))

    def calc_cost(self, text):
        return min(len(text) / 1000, 1.0)

    # -----------------------------
    # 二次レベル判定（初級〜研究）
    # -----------------------------
    def secondary_level(self, depth, branch, flow, redundancy, cost):
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

    # -----------------------------
    # 統合判定（一次＋二次）
    # -----------------------------
    def detect(self, text):
        # 一次判定
        term_density = self.calculate_term_density(text)
        prereq_score = self.calculate_prereq_score(text)
        initial_level = self.initial_level(term_density, prereq_score)

        # 二次判定
        depth = self.calc_depth(text)
        branch = self.calc_branch(text)
        flow = self.calc_flow(text)
        redundancy = self.calc_redundancy(text)
        cost = self.calc_cost(text)
        secondary = self.secondary_level(depth, branch, flow, redundancy, cost)

        # 統合レベル（今は二次判定を優先）
        final_level = secondary

        return {
            "term_density": term_density,
            "prereq_score": prereq_score,
            "initial_level": initial_level,
            "depth": depth,
            "branch": branch,
            "flow": flow,
            "redundancy": redundancy,
            "cost": cost,
            "final_level": final_level
        }
