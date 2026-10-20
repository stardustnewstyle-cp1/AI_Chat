# intent_detector.py
import os
import json
import re

class IntentDetector:

    def __init__(self):
        # intent_terms.json は intent_layer/config/ に置く
        self.intent_terms = self.load_json("intent_terms.json")

    # ============================================================
    # Pipeline から呼ぶ統合インターフェース
    # ============================================================
    def run(self, text: str):
        """
        Pipeline が使う統合インターフェース。
        domain / intent / axes / score の4要素を返す。
        """

        domain = self.detect_domain(text)
        hits = self.count_keyword_hits(text)
        intent, score = self.classify_intent_from_hits(hits)
        axes = self.compute_axes(text)

        return {
            "domain": domain,
            "intent": intent,
            "axes": axes,
            "score": score
        }

    # ============================================================
    # domain 判定（最重要）
    # ============================================================
    def detect_domain(self, user_input: str) -> str:
        text = user_input.lower()

        if "違い" in text or "比較" in text or "vs" in text:
            return "compare"
        elif "設計" in text or "architecture" in text or "デザイン" in text:
            return "design"
        elif "手順" in text or "やり方" in text or "方法" in text:
            return "steps"
        elif "注意" in text or "気をつける" in text:
            return "caution"
        elif "改善" in text or "リファクタ" in text:
            return "improvement"
        elif "要約" in text or "まとめ" in text:
            return "summary"
        elif "例" in text or "サンプル" in text:
            return "example"
        elif "仕様" in text or "ルール" in text:
            return "specification"
        elif "体系" in text or "分類" in text:
            return "systematize"
        else:
            return "explain"

    # ============================================================
    # semantic axes（軽量版）
    # ============================================================
    def compute_axes(self, text):
        """
        semantic axes の軽量版。
        必要なら後で semantic_axes.json を使って強化できる。
        """

        text_lower = text.lower()

        axes = {
            "technical": 0.0,
            "logical": 0.0,
            "factual": 0.0,
            "causal": 0.0
        }

        # --- technical axis ---
        technical_keywords = [
            "code", "class", "function", "api", "アルゴリズム", "構造",
            "設計", "optimize", "改善", "比較", "debug", "refactor"
        ]
        if any(k in text_lower for k in technical_keywords):
            axes["technical"] += 1.0

        # --- logical axis ---
        logical_keywords = [
            "how", "どうやって", "手順", "方法", "流れ", "プロセス"
        ]
        if any(k in text_lower for k in logical_keywords):
            axes["logical"] += 1.0

        # --- factual axis ---
        factual_keywords = [
            "what", "定義", "仕様", "説明", "とは", "意味"
        ]
        if any(k in text_lower for k in factual_keywords):
            axes["factual"] += 1.0

        # --- causal axis ---
        causal_keywords = [
            "why", "原因", "理由", "なぜ", "問題", "トラブル"
        ]
        if any(k in text_lower for k in causal_keywords):
            axes["causal"] += 1.0

        return axes

    # ============================================================
    # JSON ロード
    # ============================================================
    def load_json(self, file_name):
        json_path = os.path.join(
            os.path.dirname(__file__),
            "config",
            file_name
        )
        with open(json_path, "r", encoding="utf-8") as f:
            return json.load(f)

    # ============================================================
    # intent_terms.json に基づくキーワードヒット数
    # ============================================================
    def count_keyword_hits(self, text):
        text_lower = text.lower()
        tokens = re.findall(r'\b\w+\b', text_lower)
        hits = {}

        for intent, keywords in self.intent_terms.items():
            count = 0
            for kw in keywords:
                if kw.lower() in tokens:
                    count += 1
            hits[intent] = count

        return hits

    # ============================================================
    # intent 決定（再計算しない）
    # ============================================================
    def classify_intent_from_hits(self, hits):
        if not hits:
            return None, 0

        max_intent = max(hits, key=hits.get)
        max_count = hits[max_intent]

        return max_intent, max_count
