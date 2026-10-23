# ml/level_detector.py

class LevelDetector:
    """
    特徴量生成（calc_xxx）＋ルールベースのレベル判定（detect）
    ML版は level_detector_ml.py に分離してあるのでここは軽量版でOK
    """

    # -------------------------
    # 特徴量生成（既存）
    # -------------------------
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

    # -------------------------
    # ★追加：レベル判定（Pipeline が使う）
    # -------------------------
    def detect(self, features: dict) -> str:
        """
        ルールベースの簡易レベル判定
        ML版は level_detector_ml.py の predict() を使う
        """

        score = (
            features.get("tech_terms", 0) +
            features.get("connectives", 0) +
            features.get("causal_links", 0)
        )

        if score < 3:
            return "初級"
        elif score < 7:
            return "中級"
        else:
            return "上級"
