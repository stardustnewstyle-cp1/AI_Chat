class IntentDetector:
    """
    技術質問の意図判定（domain / intent / axes）
    """

    def __init__(self):

        self.tech_keywords = [
            "python", "javascript", "typescript", "java", "go", "rust",
            "class", "クラス", "api", "設計", "implementation", "実装",
            "code", "コード", "function", "関数", "error", "エラー",
            "bug", "バグ", "fix", "修正", "refactor", "リファクタ",
            "architecture", "アーキテクチャ",
            "改善", "最適化", "高速化", "効率化",
            "backend", "frontend", "database", "db", "sql",
            "docker", "kubernetes",
            "system design", "プロジェクト",
            "非同期", "同期", "処理", "実行", "ログ",
            "cache", "redis", "mysql", "postgres",
            "flask", "fastapi", "django",
            "react", "vue", "node", "next",
            "http", "https",
            "gpt", "llama", "gemini", "claude",
            "diffusion", "stable diffusion", "sdxl",
            "transformer", "attention",
            "aiモデル", "モデル", "推論", "inference",
            "gpu", "cuda", "nvidia", "amd",
            "latency", "throughput"
        ]

        self.compare_keywords = [
            "違い", "比較", "どっち", "vs", "比べる",
            "openai", "meta", "google", "anthropic"
        ]

    def is_compare(self, text: str) -> bool:
        lower = text.lower()
        return any(k in lower for k in self.compare_keywords)

    def is_technical(self, text: str) -> bool:
        lower = text.lower()
        return any(k in lower for k in self.tech_keywords)

    def detect(self, text: str) -> dict:
        lower = text.lower()

        # compare
        if self.is_compare(lower):
            return {
                "domain": "compare",
                "intent": "compare",
                "axes": {"type": "model"},
                "score": 0.95
            }

        # 非技術
        if not self.is_technical(lower):
            return {
                "domain": "non_technical",
                "intent": "non_technical",
                "axes": {},
                "score": 0.1
            }

        # steps
        if "手順" in lower or "やり方" in lower or "方法" in lower:
            return {"domain": "steps", "intent": "steps", "axes": {}, "score": 0.7}

        # caution
        if "注意" in lower or "危険" in lower or "リスク" in lower:
            return {"domain": "caution", "intent": "caution", "axes": {}, "score": 0.7}

        # improvement
        if "改善" in lower or "最適化" in lower:
            return {"domain": "improvement", "intent": "improve", "axes": {}, "score": 0.8}

        # ★ Python クラスは explain
        if "python" in lower and ("class" in lower or "クラス" in lower):
            return {
                "domain": "explain",
                "intent": "explain",
                "axes": {},
                "score": 0.8
            }

        # ★ 「仕組み」「とは」「概要」は explain
        if "仕組み" in lower or "とは" in lower or "概要" in lower:
            return {
                "domain": "explain",
                "intent": "explain",
                "axes": {},
                "score": 0.75
            }

        # ★ 設計系
        if "設計" in lower or "architecture" in lower or "アーキテクチャ" in lower:
            return {
                "domain": "design",
                "intent": "design",
                "axes": {},
                "score": 0.8
            }

        
        return {
            "domain": "structural",
            "intent": "structural",
            "axes": {},
            "score": 0.6
        }
