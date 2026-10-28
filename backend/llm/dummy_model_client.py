class DummyModelClient:
    """
    Intent / Level に応じてローカルで技術回答を生成する簡易モデル。
    TeacherLayer が構造化する前提のため、本文のみを返す。
    """

    def __init__(self):
        pass

    def generate(self, prompt: str, intent: str = "explain", level: str = "初級") -> str:

        if intent == "explain":
            return (
                f"{prompt} をわかりやすく説明します。"
                "基本的な仕組みと目的を中心に解説します。"
            )

        if intent == "compare":
            return (
                f"{prompt} の違いを整理します。"
                "構造・用途・動作の観点から比較します。"
            )

        if intent == "design":
            return (
                f"{prompt} の設計方針をまとめます。"
                "責務分離と拡張性を中心に説明します。"
            )

        if intent == "steps":
            return (
                f"{prompt} を行う手順を整理します。"
                "必要な準備と実行ステップを説明します。"
            )

        if intent == "improvement":
            return (
                f"{prompt} の改善ポイントを説明します。"
                "冗長処理の削減や命名改善を含みます。"
            )

        if intent == "summary":
            return (
                f"{prompt} の要点を簡潔にまとめます。"
                "重要なポイントを中心に整理します。"
            )

        if intent == "debug":
            return (
                f"{prompt} の原因を特定するための観点を整理します。"
                "再現手順や依存関係を中心に確認します。"
            )

        if intent == "optimization":
            return (
                f"{prompt} のパフォーマンス改善ポイントを説明します。"
                "アルゴリズムやデータ構造の見直しを含みます。"
            )

        if intent == "structuring":
            return (
                f"{prompt} を体系的に整理します。"
                "概念の分類や関係性を中心に説明します。"
            )

        return (
            f"{prompt} を説明します。"
            "基本的な仕組みと目的を中心に解説します。"
        )
