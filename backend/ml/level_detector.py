# ml/level_detector.py
class LevelDetector:
    """
    特徴量生成の本体（ルールベース）
    ML導入後は判定ではなく特徴量生成専用になる
    """

    def calc_depth(self, text: str) -> float:
        return len(text.split()) / 100

    def calc_branch(self, text: str) -> float:
        return text.count("、") / 10

    def calc_flow(self, text: str) -> float:
        return 0.5  

    def calc_redundancy(self, text: str) -> float:
        return 0.1  

    def calc_complexity(self, text: str) -> float:
        return len([w for w in text.split() if len(w) > 6]) / 20

    def calc_term_density(self, text: str) -> float:
        terms = ["AI", "モデル", "学習", "推論", "GPU", "Transformer"]
        return sum(t in text for t in terms) / 10

    def calc_prereq_score(self, text: str) -> float:
        return self.calc_term_density(text) * 5

    def calc_cost(self, text: str) -> float:
        return self.calc_depth(text) * 0.3
