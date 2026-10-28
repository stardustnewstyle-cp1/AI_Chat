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
        domain = features.get("domain")

        # ★ 締め切り対応：compare は必ず中級にする
        if domain == "compare":
            return "中級"

        # --- コード特徴量 ---
        loop_count = features.get("loop_count", 0)
        nest_depth = features.get("nest_depth", 0)
        function_count = features.get("function_count", 0)
        class_count = features.get("class_count", 0)
        async_used = features.get("async_used", 0)
        try_except = features.get("try_except", 0)

        # --- 文章特徴量 ---
        score = (
            features.get("tech_terms", 0) +
            features.get("connectives", 0) +
            features.get("causal_links", 0)
        )

        # --- domain 補正 ---
        if domain == "design":
            score += 1
        if domain == "caution":
            score += 1
        if domain == "steps":
            score += 1  # 手順系は文章構造が複雑になりやすい

        # --- 上級 ---
        if class_count >= 2 or nest_depth >= 3 or score >= 8:
            return "上級"

        # --- 中級 ---
        if (
            nest_depth >= 2 or
            async_used == 1 or
            try_except == 1 or
            function_count >= 2 or
            score >= 4
        ):
            return "中級"

        return "初級"
