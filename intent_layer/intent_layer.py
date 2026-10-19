class IntentDetector:

    def detect(self, user_input: str) -> dict:
        text = user_input.lower()

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
            domain = "explain"

        return {"domain": domain}
