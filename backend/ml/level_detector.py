#level_detector.py
class LevelDetector:
    """
    軽量ルールベースのレベル判定。
    FeatureExtractor → LevelDetector → Pipeline の流れと完全整合。
    compare / design / steps / caution / improvement の各 domain に対応。
    """

    # -------------------------
    # 文章特徴量（AIモデル語彙を含む）
    # -------------------------
    def calc_term_density(self, text: str) -> float:
        # AIモデル系語彙を追加（IntentDetector と整合）
        terms = [
            "AI", "モデル", "学習", "推論", "GPU", "Transformer",
            "GPT", "Llama", "Diffusion", "Stable Diffusion", "SDXL",
            "CUDA", "NVIDIA", "AMD", "Attention"
        ]
        return sum(t.lower() in text.lower() for t in terms) / 10

    def calc_depth(self, text: str) -> float:
        return len(text.split()) / 100

    def calc_complexity(self, text: str) -> float:
        return len([w for w in text.split() if len(w) > 6]) / 20

    def calc_prereq_score(self, text: str) -> float:
        return self.calc_term_density(text) * 5

    # -------------------------
    # レベル判定（Pipeline が使う）
    # -------------------------
    def detect(self, features: dict) -> str:
        """
        FeatureExtractor の出力と ReasoningLayer の domain を使って
        初級 / 中級 / 上級 を判定する。
        """

        # --- コード特徴量（既存） ---
        loop_count = features.get("loop_count", 0)
        nest_depth = features.get("nest_depth", 0)
        function_count = features.get("function_count", 0)
        class_count = features.get("class_count", 0)
        async_used = features.get("async_used", 0)
        try_except = features.get("try_except", 0)

        # --- 文章特徴量（FeatureExtractor と整合） ---
        score = (
            features.get("tech_terms", 0) +
            features.get("connectives", 0) +
            features.get("causal_links", 0)
        )

        # --- domain に応じた補正（ReasoningLayer と整合） ---
        domain = features.get("domain")

        # compare は文章の深さが高くなるので補正
        if domain == "compare":
            score += 2

        # design は構造化された説明が多いので補正
        if domain == "design":
            score += 1

        # caution は専門語彙が増えるので補正
        if domain == "caution":
            score += 1

        # -------------------------
        # レベル判定ロジック
        # -------------------------

        # 上級（構造化されたコード or 高い文章スコア）
        if class_count >= 2 or nest_depth >= 3 or score >= 8:
            return "上級"

        # 中級（少し複雑）
        if (
            nest_depth >= 2 or
            async_used == 1 or
            try_except == 1 or
            function_count >= 2 or
            score >= 4
        ):
            return "中級"

        # 初級（簡単）
        return "初級"
