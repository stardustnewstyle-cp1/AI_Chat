# backend/llm/llm.py

class LLM:
    """
    DummyModelClient / 任意の簡易モデル用の軽量 LLM ラッパー。
    pipeline から intent / level を受け取り、model_client に渡す。
    """

    def __init__(self, model_client=None):
        self.model = model_client

    def generate(self, text: str, intent: str = "explain", level: str = "初級", external_context=None) -> str:
        """
        DummyModelClient は文字列を返すため、
        LLM.generate() も文字列をそのまま返す。
        """

        # 外部検索があればそちらを優先
        source = external_context.get("text") if external_context else text

        if self.model is None:
            return f"（fallback）{source}"

        try:
            # ★ intent / level を DummyModelClient に渡す
            return self.model.generate(source, intent=intent, level=level)
        except Exception as e:
            return f"モデル呼び出しでエラーが発生しました: {e}"
