# ★★★ IntentDetector 完全修正版 ★★★

class IntentDetector:
    """
    技術質問の意図判定（domain / intent / axes）
    """

    def __init__(self):

        self.tech_keywords = [
            "python", "fastapi", "flask", "django",
            "class", "クラス", "api", "設計", "implementation", "実装",
            "code", "コード", "function", "関数", "error", "エラー",
            "backend", "frontend", "database", "sql",
            "docker", "kubernetes",
            "非同期", "同期",
            "認証", "ログイン", "jwt", "oauth",
        ]

        self.compare_keywords = [
            "違い", "比較", "どっち", "vs", "比べる", "差分",
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

        # ★★★ steps 判定を強化（ここが最重要）★★★
        if any(k in lower for k in [
            "手順", "やり方", "方法", "追加する", "導入する", "設定する",
            "インストール", "構築", "作る", "実装する"
        ]):
            return {
                "domain": "steps",
                "intent": "steps",
                "axes": {},
                "score": 0.9
            }

        # caution
        if "注意" in lower or "危険" in lower or "リスク" in lower:
            return {"domain": "caution", "intent": "caution", "axes": {}, "score": 0.7}

        # improvement
        if "改善" in lower or "最適化" in lower:
            return {"domain": "improvement", "intent": "improve", "axes": {}, "score": 0.8}

        # 設計系
        if "設計" in lower or "architecture" in lower or "アーキテクチャ" in lower:
            return {
                "domain": "design",
                "intent": "design",
                "axes": {},
                "score": 0.8
            }

        # fallback → design
        return {
            "domain": "design",
            "intent": "design",
            "axes": {},
            "score": 0.6
        }
