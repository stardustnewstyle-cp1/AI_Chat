#dummy_model_client.py
class DummyModelClient:
    """
    llama-cpp や LM Studio が動かない環境向けの簡易ローカル LLM。
    TeacherLayer が構造化した内容をそのまま返すだけ。
    """

    def __init__(self):
        pass

    def generate(self, prompt: str) -> str:
        return f"（ローカルAIによる簡易回答）\n{prompt}"
