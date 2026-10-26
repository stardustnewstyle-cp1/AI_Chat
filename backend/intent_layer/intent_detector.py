# intent_layer/intent_detector.py

import os
import json

class IntentDetector:
    DEFAULT_TECH_TERMS = [
        "python", "javascript", "typescript", "java", "go", "rust",
        "rest", "graphql", "api", "http", "https", "json", "yaml",
        "sql", "database", "db", "mysql", "postgres", "redis", "mongo",
        "docker", "kubernetes", "aws", "gcp", "linux", "react", "vue",
        "node", "next", "fastapi", "flask", "django", "spring",
        "class", "function", "design", "architecture", "implementation",
        "code", "error", "bug", "fix", "refactor", "algorithm", "model",
        "ai", "ml", "llm", "security", "performance", "cache", "query",
        "schema", "browser", "server", "network"
    ]

    def __init__(self):
        path = os.path.join(os.path.dirname(__file__), "..", "models", "categories", "technical_terms.json")

        self.tech_terms = set(self.DEFAULT_TECH_TERMS)

        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)

            if isinstance(data, dict):
                terms = []
                for value in data.values():
                    if isinstance(value, list):
                        terms.extend(value)
                self.tech_terms |= {str(t).lower() for t in terms if str(t).strip()}

            elif isinstance(data, list):
                self.tech_terms |= {str(t).lower() for t in data if str(t).strip()}

        except Exception:
            # JSON が空でも壊れていても安全に fallback
            self.tech_terms = set(self.DEFAULT_TECH_TERMS)

    def detect(self, user_input: str) -> dict:
        text = user_input.lower()

        is_technical = any(term in text for term in self.tech_terms)

        if "違い" in text or "比較" in text or "vs" in text:
            domain = "compare"
        elif "設計" in text or "architecture" in text or "デザイン" in text:
            domain = "design"
        elif "手順" in text or "やり方" in text or "方法" in text:
            domain = "steps"
        elif "注意" in text or "気をつける" in text:
            domain = "caution"
        elif "改善" in text or "リファクタ" in text:
            domain = "improvement"
        elif "要約" in text or "まとめ" in text:
            domain = "summary"
        elif "例" in text or "サンプル" in text:
            domain = "example"
        elif "仕様" in text or "ルール" in text:
            domain = "specification"
        elif "体系" in text or "分類" in text:
            domain = "systematize"
        else:
            domain = "explain" if is_technical else "non_technical"

        intent = domain
        axes = {"technical": 1.0 if is_technical else 0.0}
        score = 1 if is_technical else 0

        return {
            "domain": domain,
            "intent": intent,
            "axes": axes,
            "score": score
        }