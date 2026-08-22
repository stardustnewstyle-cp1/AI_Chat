# dictionary/context_patterns.py

CONTEXT_PATTERNS = {
    "compare": [
        r".+と.+の違い", r"比較", r"vs", r"どっちが"
    ],
    "understand": [
        r"とは", r"仕組み", r"意味", r"概要", r"説明して"
    ],
    "design": [
        r"設計", r"構造", r"アーキテクチャ", r"どう作る"
    ],
    "debug": [
        r"エラー", r"原因", r"動かない", r"traceback", r"例外"
    ],
    "improve": [
        r"改善", r"修正", r"リファクタ", r"もっと良く"
    ],
    "optimize": [
        r"高速化", r"効率化", r"最適化", r"遅い"
    ],
    "summarize": [
        r"要約", r"まとめて", r"短く"
    ],
    "generate": [
        r"作成して", r"生成して", r"書いて"
    ],
    "classify": [
        r"分類", r"カテゴリ", r"タイプ分け"
    ],
    "evaluate": [
        r"評価", r"レビュー", r"良いか悪いか"
    ]
}
