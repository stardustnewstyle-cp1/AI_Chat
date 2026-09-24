# ============================================
# improver.py
# Intent Layer Pipeline（semantic_axes 統合版）
# ============================================

from .source_filter import SourceFilter
from .feature_extractors import extract_features
from .semantic_axes import load_axes_dict, classify_axes


class ImproverPipeline:

    def __init__(self, axes_dict_path):
        # 安全フィルタ
        self.filter = SourceFilter()

        # semantic_axes.json を読み込む
        self.axes_dict = load_axes_dict(axes_dict_path)

    # -----------------------------------------
    # 情報源メタデータの評価
    # -----------------------------------------
    def evaluate_source(self, meta):
        return self.filter.filter_source(meta)

    # -----------------------------------------
    # 辞書抽出フェーズ（強弱語・曖昧語など）
    # -----------------------------------------
    def extract(self, text, dict_paths):
        return extract_features(text, dict_paths)

    # -----------------------------------------
    # 意味軸フェーズ（semantic axes）
    # -----------------------------------------
    def apply_semantic_axes(self, text):
        return classify_axes(text, self.axes_dict)

    # -----------------------------------------
    # 推論フェーズ（reasoning engine）
    # -----------------------------------------
    def reasoning(self, features, axes):
        # 後で reasoning_engine を統合する
        return {
            "intent": "unknown",
            "confidence": 0.0,
            "features": features,
            "axes": axes
        }

    # -----------------------------------------
    # 改善フェーズ（最終出力の整形）
    # -----------------------------------------
    def improve_output(self, reasoning_result):
        return {
            "final_intent": reasoning_result["intent"],
            "confidence": reasoning_result["confidence"],
            "explanation": "Intent Layer output (placeholder)"
        }

    # -----------------------------------------
    # パイプライン全体
    # -----------------------------------------
    def run(self, meta, text, dict_paths):
        # 1. 安全フィルタ
        source_eval = self.evaluate_source(meta)
        if not source_eval["allowed"]:
            return {
                "status": "blocked",
                "reason": source_eval["reason"],
                "score": source_eval["score"]
            }

        # 2. 辞書抽出（意図抽出）
        features = self.extract(text, dict_paths)

        # 3. 意味軸分類
        axes = self.apply_semantic_axes(text)

        # 4. 推論フェーズ
        reasoning_result = self.reasoning(features, axes)

        # 5. 改善フェーズ
        final_output = self.improve_output(reasoning_result)

        return {
            "status": "ok",
            "source_score": source_eval["score"],
            "result": final_output
        }
