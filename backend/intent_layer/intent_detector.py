# intent_layer/intent_detector.py

import os
import json
import re

class IntentDetector:
    def __init__(self):
        path = os.path.join(os.path.dirname(__file__), "..", "models/categories/", "technical_terms.json")
        with open(path, "r", encoding="utf-8") as f:
            self.tech_terms = set(json.load(f))

    def detect(self, user_input: str) -> dict:
        text = user_input.lower()

        # 技術語彙チェック
        is_technical = any(term in text for term in self.tech_terms)

        # domain 判定
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

        # intent（簡易）
        intent = domain

        # axes（簡易）
        axes = {"technical": 1.0 if is_technical else 0.0}

        # score（簡易）
        score = 1 if is_technical else 0

        return {
            "domain": domain,
            "intent": intent,
            "axes": axes,
            "score": score
        }
