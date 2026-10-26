# backend/utils/search_query_builder.py
from typing import Dict, List, Tuple

# --- 推論テンプレート ---
reasoning_templates = {
    "structure": ["{topic} 仕組み", "{topic} 構造", "{topic} 全体像", "{topic} 関係性"],
    "procedure": ["{topic} 手順", "{topic} やり方", "{topic} ステップ", "{topic} 実装方法"],
    "concept": ["{topic} とは", "{topic} 定義", "{topic} 基本概念"],
    "causality": ["{topic} 原因", "{topic} なぜ", "{topic} 理由"],
    "contrast": ["{topic} 比較", "{topic} 違い", "{topic} メリット デメリット"],
    "improvement": ["{topic} 改善案", "{topic} 最適化", "{topic} 効率化"],
    "organization": ["{topic} まとめ", "{topic} 要点", "{topic} 整理"],
    "selection": ["{topic} 選び方", "{topic} おすすめ", "{topic} 比較ポイント"],
    "action": ["{topic} 操作方法", "{topic} 使い方"],
    "abstraction": ["{topic} 抽象化", "{topic} 本質", "{topic} 概要"]
}

# --- ソーステンプレート ---
source_templates = {
    "qiita": ["{topic} 実装", "{topic} 手順", "{topic} トラブルシューティング"],
    "zenn": ["{topic} 解説", "{topic} 実装方法"],
    "stackoverflow": ["{topic} エラー", "{topic} 原因", "{topic} 解決策"],
    "github_docs": ["{topic} ドキュメント", "{topic} API", "{topic} 設計"],
    "wikipedia": ["{topic} とは", "{topic} 概要", "{topic} 歴史"],
    "review": ["{topic} 評価", "{topic} 比較", "{topic} 選び方"],
    "compare_article": ["{topic} 比較", "{topic} 違い"],
    "research_abstract": ["{topic} 論文", "{topic} 研究"]
}


def build_query(topic: str, final_vector: Dict[str, float], source: str) -> List[Tuple[str, float]]:
    """
    推論方向ベクトル × ソース種類 × 推論テンプレート
    を使って検索クエリ候補を生成する。
    """
    queries = []

    # 推論テンプレート
    for axis, weight in final_vector.items():
        if axis in reasoning_templates:
            for template in reasoning_templates[axis]:
                queries.append((template.format(topic=topic), weight))

    # ソーステンプレート
    if source in source_templates:
        for template in source_templates[source]:
            queries.append((template.format(topic=topic), 0.7))

    # 重み順に並べる
    queries.sort(key=lambda x: x[1], reverse=True)
    return queries


def build_top_queries(topic: str, final_vector: Dict[str, float], source: str, limit: int = 5) -> List[str]:
    """
    上位の検索クエリだけ返す（Knowledge Layerで使う）
    """
    queries = build_query(topic, final_vector, source)
    return [q for q, _ in queries[:limit]]


class SearchQueryBuilder:
    """
    クエリ生成器（検索実行はしない）
    pipeline.py が検索実行エンジンと組み合わせて使う。
    """
    def build(self, topic: str, axes: Dict[str, float], source: str = "qiita") -> List[str]:
        return build_top_queries(topic, axes, source)
