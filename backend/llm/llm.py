# backend/llm/llm.py

class LLM:
    """
    DummyModelClient / 任意の簡易モデル用の軽量 LLM ラッパー。
    pipeline から呼ばれ、単純に model_client.generate() の結果を返す。
    """

    def __init__(self, model_client=None):
        self.model = model_client

    def generate(self, text: str, domain: str = "explain", external_context=None) -> str:
        """
        DummyModelClient は文字列を返すため、
        LLM.generate() も文字列をそのまま返す。
        """
        source = external_context.get("text") if external_context else text

        if self.model is None:
            return f"（fallback）{source}"

        try:
            return self.model.generate(source)
        except Exception as e:
            return f"モデル呼び出しでエラーが発生しました: {e}"
