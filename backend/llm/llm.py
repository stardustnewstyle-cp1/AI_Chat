# backend/llm/llm.py

class LLM:

    def generate(self, text: str, domain: str = "explain") -> dict:
        """
        仮の回答生成器
        """

        lower = text.lower()

        # -------------------------
        # ★ 改善系（最小追加）
        # -------------------------
        if domain == "improvement":
            return {
                "issues": [
                    "ループで加算しているため計算量が O(a) と大きい",
                    "calc という関数名が抽象的で役割が分かりにくい",
                    "変数 c が何を表しているか不明確"
                ],
                "solutions": [
                    "乗算 a * b を使うことで O(1) にできる",
                    "関数名を multiply に変更するなど意味を明確化する",
                    "変数名を result に変更して役割を明確化する"
                ],
                "design_change": "ループを廃止し、純粋な算術演算に置き換えることで高速化と可読性向上を図る",
                "effect_check": [
                    "a が大きい場合に高速化されているかベンチマークで確認する",
                    "変数名変更によりコードレビュー時の理解が向上しているか確認する"
                ],
                "cautions": [
                    "a と b の型チェックを追加して予期せぬ動作を防ぐ",
                    "負の値やゼロのケースを考慮する"
                ]
            }

        # -------------------------
        # 既存の explain 系（そのまま）
        # -------------------------

        # Python クラス
        if "python" in lower and "クラス" in text:
            return {
                "summary":
                    "Pythonのクラスはデータと処理をひとつにまとめるためのオブジェクト指向機能です。",
                "example":
"""class User:
    def __init__(self, name):
        self.name = name

user = User("Taro")
print(user.name)
""",
                "cautions": [
                    "クラスとインスタンスを混同しない",
                    "__init__ の役割を理解する",
                ]
            }

        # REST vs GraphQL
        if "graphql" in lower or "rest" in lower:
            return {
                "summary":
                    "RESTはURL単位でリソースを取得し、GraphQLは必要なデータだけを取得できます。",
                "example":
"""REST:
GET /users/1

GraphQL:
{
  user(id:1){
    id
    name
  }
}
""",
                "cautions": [
                    "GraphQLは柔軟だが設計が複雑になりやすい",
                    "RESTはシンプルだが過剰取得が起きやすい",
                ]
            }

        # 非同期
        if "非同期" in text:
            return {
                "summary":
                    "非同期処理では待機時間を有効活用できますが、状態管理や競合状態に注意が必要です。",
                "example":
"""async def main():
    result = await fetch_data()
    print(result)
""",
                "cautions": [
                    "共有状態への同時アクセス",
                    "例外処理の見落とし",
                    "デッドロック",
                ]
            }

        # fallback（そのまま）
        return {
            "summary": f"「{text}」についての技術的な説明です。",
            "example": "",
            "cautions": ["前提条件を確認してください"]
        }
