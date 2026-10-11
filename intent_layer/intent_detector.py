# intent_detector.py
class IntentDetector:

    def __init__(self):
        self.intent_terms = self.load_json("intent_terms.json")

    # ----------------------------------------
    # Pipeline から呼ぶ統一インターフェース
    # ----------------------------------------
    def run(self, text):
        hits = self.count_keyword_hits(text)
        intent, score = self.classify_intent_from_hits(hits)
        return {
            "count": hits,
            "intent": intent,
            "score": score
        }

    # ----------------------------------------
    # JSONロード
    # ----------------------------------------
    def load_json(self, file_path):
        import json
        import os

        json_path = os.path.join(os.path.dirname(__file__), file_path)
        with open(json_path, "r") as f:
            return json.load(f)

    # ----------------------------------------
    # キーワードヒット数を数える
    # ----------------------------------------
    def count_keyword_hits(self, text):
        import re

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

    # ----------------------------------------
    # ヒット数から intent を決定する（再計算しない）
    # ----------------------------------------
    def classify_intent_from_hits(self, hits):
        if not hits:
            return None, 0

        max_intent = max(hits, key=hits.get)
        max_count = hits[max_intent]

        return max_intent, max_count
