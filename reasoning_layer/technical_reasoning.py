# technical_reasoning.py

from typing import Dict, Any
from intent_layer.intent_keywords import ALL_KEYWORDS


class TechnicalReasoner:
    """
    技術特化AI用の推論エンジン。
    semantic axes / features を入力に、
    compare / debug / improve / optimize / design の5種類の推論を行う。
    """

    def __init__(self):
        pass

    # ============================
    # 内側の層（脳の本体）
    # ============================
    def extract_features(self, text: str, source_bias: int = 0) -> Dict[str, Any]:
        keyword_strength = 0
        for kw in ALL_KEYWORDS:
            if kw in text:
                keyword_strength += 1

        context_strength = 0
        question_patterns = ["なぜ", "どうやって", "原因", "理由", "問題", "比較", "改善"]
        for q in question_patterns:
            if q in text:
                context_strength += 1

        structure_strength = 0
        structure_patterns = ["class", "def", "import", "return", "if", "for", "while"]
        for s in structure_patterns:
            if s in text:
                structure_strength += 1

        source_strength = source_bias

        return {
            "keyword_strength": keyword_strength,
            "context_strength": context_strength,
            "structure_strength": structure_strength,
            "source_strength": source_strength,
            "raw_text": text,
        }

    def classify_reasoning_type(self, features: Dict[str, Any]) -> str:
        ks = features.get("keyword_strength", 0)
        cs = features.get("context_strength", 0)
        ss = features.get("structure_strength", 0)

        weights = {
            "compare":  {"ks": 1.2, "cs": 0.8, "ss": 0.6},
            "debug":    {"ks": 1.0, "cs": 1.5, "ss": 0.7},
            "improve":  {"ks": 1.3, "cs": 1.0, "ss": 0.6},
            "optimize": {"ks": 1.1, "cs": 0.7, "ss": 1.2},
            "design":   {"ks": 1.4, "cs": 0.5, "ss": 1.5},
        }

        scores = {}
        for rtype, w in weights.items():
            score = ks * w["ks"] + cs * w["cs"] + ss * w["ss"]
            scores[rtype] = score

        best_type = max(scores, key=scores.get)
        return best_type

    def evaluate(self, features: Dict[str, Any], reasoning_type: str) -> Dict[str, Any]:
        ks = features["keyword_strength"]
        cs = features["context_strength"]
        ss = features["structure_strength"]
        src = features["source_strength"]

        weights = {
            "compare":  {"ks": 1.2, "cs": 0.8, "ss": 0.6},
            "debug":    {"ks": 1.0, "cs": 1.5, "ss": 0.7},
            "improve":  {"ks": 1.3, "cs": 1.0, "ss": 0.6},
            "optimize": {"ks": 1.1, "cs": 0.7, "ss": 1.2},
            "design":   {"ks": 1.4, "cs": 0.5, "ss": 1.5},
        }

        w = weights[reasoning_type]
        score = ks * w["ks"] + cs * w["cs"] + ss * w["ss"] + src * 0.5
        confidence = min(1.0, score / 10.0)

        weak_points = []
        if ks < 2:
            weak_points.append("keyword不足")
        if cs < 1:
            weak_points.append("context不足")
        if ss < 1:
            weak_points.append("structure不足")

        return {
            "confidence": confidence,
            "weak_points": weak_points,
        }

    def detect_weak_points(self, features: Dict[str, Any], reasoning_type: str) -> list:
        ks = features["keyword_strength"]
        cs = features["context_strength"]
        ss = features["structure_strength"]

        weak = []
        if ks < 2:
            weak.append("keyword不足")
        if cs < 1:
            weak.append("context不足")
        if ss < 1:
            weak.append("structure不足")

        if reasoning_type == "compare":
            if ss < 2:
                weak.append("比較軸が不足")
            if ks < 3:
                weak.append("比較キーワード不足")
        elif reasoning_type == "debug":
            if cs < 2:
                weak.append("再現条件の文脈不足")
            if ks < 2:
                weak.append("原因候補のキーワード不足")
        elif reasoning_type == "improve":
            if ss < 2:
                weak.append("改善ポイントの構造不足")
            if ks < 3:
                weak.append("改善キーワード不足")
        elif reasoning_type == "optimize":
            if ss < 2:
                weak.append("ボトルネック構造不足")
            if ks < 3:
                weak.append("最適化キーワード不足")
        elif reasoning_type == "design":
            if ss < 3:
                weak.append("設計構造の手がかり不足")
            if ks < 2:
                weak.append("設計キーワード不足")

        return weak

    def improve(self, features: Dict[str, Any], weak_points: list, reasoning_type: str) -> Dict[str, Any]:
        improved = features.copy()

        if "keyword不足" in weak_points:
            improved["keyword_strength"] += 1
        if "context不足" in weak_points:
            improved["context_strength"] += 1
        if "structure不足" in weak_points:
            improved["structure_strength"] += 1

        if reasoning_type == "compare":
            if "比較軸が不足" in weak_points:
                improved["structure_strength"] += 1
            if "比較キーワード不足" in weak_points:
                improved["keyword_strength"] += 1
        elif reasoning_type == "debug":
            if "再現条件の文脈不足" in weak_points:
                improved["context_strength"] += 1
            if "原因候補のキーワード不足" in weak_points:
                improved["keyword_strength"] += 1
        elif reasoning_type == "improve":
            if "改善ポイントの構造不足" in weak_points:
                improved["structure_strength"] += 1
            if "改善キーワード不足" in weak_points:
                improved["keyword_strength"] += 1
        elif reasoning_type == "optimize":
            if "ボトルネック構造不足" in weak_points:
                improved["structure_strength"] += 1
            if "最適化キーワード不足" in weak_points:
                improved["keyword_strength"] += 1
        elif reasoning_type == "design":
            if "設計構造の手がかり不足" in weak_points:
                improved["structure_strength"] += 1
            if "設計キーワード不足" in weak_points:
                improved["keyword_strength"] += 1
        # source_strength の改善も追加
        if "source不足" in weak_points:
            improved["source_strength"] += 1

        return improved

    def depth_loop(self, raw_text: str, max_depth: int = 3, threshold: float = 0.8) -> Dict[str, Any]:
        depth = 0
        last_result = None

        while depth < max_depth:
            features = self.extract_features(raw_text)
            reasoning_type = self.classify_reasoning_type(features)
            weak_points = self.detect_weak_points(features, reasoning_type)
            improved_features = self.improve(features, weak_points, reasoning_type)
            evaluation = self.evaluate(improved_features, reasoning_type)
            confidence = evaluation["confidence"]
            depth += 1

            last_result = {
                "reasoning_type": reasoning_type,
                "features": improved_features,
                "confidence": confidence,
                "weak_points": weak_points,
                "depth": depth,
            }

            if confidence >= threshold or len(weak_points) == 0:
                break

        return last_result

    # ============================
    # 外側の層（推論タイプごとの処理）
    # ============================

    def run(self, raw_text: str) -> Dict[str, Any]:
        loop_result = self.depth_loop(raw_text)

        reasoning_type = loop_result["reasoning_type"]
        features = loop_result["features"]
        confidence = loop_result["confidence"]
        weak_points = loop_result["weak_points"]
        depth = loop_result["depth"]

        context = {
            "raw_text": raw_text,
            "features": features,
            "axes": {},
        }

        if reasoning_type == "compare":
            outer = self._reason_compare(context)
        elif reasoning_type == "debug":
            outer = self._reason_debug(context)
        elif reasoning_type == "improve":
            outer = self._reason_improve(context)
        elif reasoning_type == "optimize":
            outer = self._reason_optimize(context)
        elif reasoning_type == "design":
            outer = self._reason_design(context)
        else:
            outer = {
                "reasoning_type": reasoning_type,
                "steps": [],
                "analysis": [],
                "conclusion": "未対応の推論タイプです。",
                "confidence": 0.0,
            }

        outer["confidence"] = confidence
        outer["weak_points"] = weak_points
        outer["depth"] = depth

        return {
            "reasoning_type": reasoning_type,
            "features": features,
            "confidence": confidence,
            "weak_points": weak_points,
            "depth": depth,
            "outer": outer
        }

    def _reason_compare(self, context: Dict[str, Any]) -> Dict[str, Any]:
        raw = context["raw_text"]
        features = context["features"]
        points = self._extract_comparison_points(raw, features)

        steps = [
            "比較対象の抽出",
            "比較軸の洗い出し",
            "各軸ごとの評価",
            "総合的な結論の提示",
        ]

        analysis = [
            f"比較軸: {points}",
            "各軸ごとにメリット・デメリットを整理する。",
        ]

        # -------------------------
        # ★ 入力依存の追加ロジック
        # -------------------------

        # raw_text に応じた追加
        if "速度" in raw or "高速" in raw:
            analysis.append("速度に関する記述があるため、性能軸を重視する。")

        if "コスト" in raw or "料金" in raw:
            analysis.append("コストに関する記述があるため、費用面の比較が重要。")

        if "Python" in raw and "Go" in raw:
            analysis.append("Python と Go の比較が求められている。")

        # features に応じた追加
        if features["keyword_strength"] >= 3:
            analysis.append("キーワード密度が高いため、技術的な深い比較が必要。")

        if features["context_strength"] >= 2:
            analysis.append("文脈が複雑なため、用途に応じた比較が求められる。")

        if features["structure_strength"] >= 2:
            analysis.append("構造的な観点からの比較も重要になる。")

        conclusion = "比較軸に基づいて、用途に応じた最適な選択肢を提示する。"

        return {
            "reasoning_type": "compare",
            "steps": steps,
            "analysis": analysis,
            "conclusion": conclusion
        }


    def _extract_comparison_points(self, raw_text: str, features: Dict[str, Any], weak_points: List[str]):
        points = []

        # raw_text から比較軸候補を抽出
        if any(k in raw_text for k in ["速度", "高速", "パフォーマンス", "レスポンス"]):
            points.append("性能")

        if any(k in raw_text for k in ["コスト", "料金", "値段", "費用"]):
            points.append("コスト")

        if any(k in raw_text for k in ["保守", "メンテ", "運用", "サポート"]):
            points.append("保守性")

        if any(k in raw_text for k in ["拡張", "スケール", "スケーラビリティ", "将来性"]):
            points.append("拡張性")

        # features に応じた追加
        if features.get("structure_strength", 0) >= 2:
            points.append("構造性")

        if features.get("keyword_strength", 0) >= 3:
            points.append("技術的深さ")

        if features.get("context_strength", 0) >= 2:
            points.append("文脈の複雑性")

        # weak_points に応じた追加
        if "比較軸不足" in weak_points:
            points.extend(["性能", "コスト", "保守性", "拡張性"])

        # デフォルト
        if not points:
            points = ["性能", "コスト", "保守性", "拡張性"]

        return list(set(points))


    def _reason_debug(self, context: Dict[str, Any]) -> Dict[str, Any]:
        raw = context["raw_text"]
        features = context["features"]
        weak_points = context.get("weak_points", [])

        steps = [
            "現象の整理",
            "再現条件の特定",
            "典型的な原因パターンとの照合",
            "原因候補のランキング",
        ]

        analysis = [
            "エラーメッセージや挙動から、よくある原因パターンを照合する。",
            "設定ミス・依存関係・バージョン差異などを候補に挙げる。",
            "ログ解析やスタックトレースのパターン認識も活用。",
        ]

        # raw_text に応じた追加
        if "落ちる" in raw or "クラッシュ" in raw:
            analysis.append("クラッシュが発生しているため、メモリリークや例外処理の不足が疑われる。")

        if "遅い" in raw or "重い" in raw:
            analysis.append("動作が重いため、パフォーマンス劣化や無限ループの可能性がある。")

        # features に応じた追加
        if features["keyword_strength"] >= 3:
            analysis.append("キーワード密度が高いため、原因候補の特定が容易。")

        if features["structure_strength"] >= 2:
            analysis.append("構造的な情報が多いため、依存関係の問題を疑うべき。")

        # weak_points に応じた追加
        if "情報不足" in weak_points:
            analysis.append("情報が不足しているため、ログの追加取得が必要。")

        conclusion = "最も可能性の高い原因候補を提示し、次に確認すべきポイントを示す。"

        return {
            "reasoning_type": "debug",
            "steps": steps,
            "analysis": analysis,
            "conclusion": conclusion
        }


    def _reason_improve(self, context: Dict[str, Any]) -> Dict[str, Any]:
        raw = context["raw_text"]
        features = context["features"]
        weak_points = context.get("weak_points", [])

        steps = [
            "現状の問題点の抽出",
            "改善余地のある箇所の特定",
            "改善案の列挙",
            "影響範囲とリスクの整理",
        ]

        analysis = [
            "構造・可読性・パフォーマンス・保守性の観点から改善ポイントを洗い出す。",
            "コードレビュー結果やテストカバレッジも参考にする。",
        ]

        # -------------------------
        # ★ raw_text に応じた追加
        # -------------------------
        if any(k in raw for k in ["遅い", "重い", "速度", "パフォーマンス"]):
            analysis.append("速度に関する問題が示唆されているため、パフォーマンス改善が必要。")

        if any(k in raw for k in ["読みにくい", "可読性", "複雑", "スパゲッティ"]):
            analysis.append("可読性や構造の問題があるため、リファクタリングや責務分割が有効。")

        if any(k in raw for k in ["冗長", "無駄", "最適化"]):
            analysis.append("冗長な処理が存在する可能性があり、ロジックの簡素化が改善につながる。")

        # -------------------------
        # ★ features に応じた追加
        # -------------------------
        if features.get("structure_strength", 0) >= 2:
            analysis.append("構造的な情報が多いため、設計改善の余地が大きい。")

        if features.get("keyword_strength", 0) >= 3:
            analysis.append("改善に関するキーワードが多く、具体的な改善案を提示しやすい。")

        if features.get("context_strength", 0) >= 2:
            analysis.append("文脈が十分にあるため、改善ポイントの特定が容易。")

        # -------------------------
        # ★ weak_points に応じた追加
        # -------------------------
        if "改善ポイントの構造不足" in weak_points:
            analysis.append("構造的な情報が不足しているため、改善ポイントの特定が難しい。")

        if "改善キーワード不足" in weak_points:
            analysis.append("改善に関するキーワードが不足しているため、改善案の精度が低下する可能性がある。")

        if "情報不足" in weak_points:
            analysis.append("情報が不足しているため、追加の仕様確認やログ取得が必要。")

        conclusion = "具体的な改善案を複数提示し、優先度の高いものから実施する方針を示す。"

        return {
            "reasoning_type": "improve",
            "steps": steps,
            "analysis": analysis,
            "conclusion": conclusion
        }


    def _reason_design(self, context: Dict[str, Any]) -> Dict[str, Any]:
        raw = context["raw_text"]
        features = context["features"]
        weak_points = context.get("weak_points", [])

        steps = [
            "構成要素の洗い出し",
            "依存関係の整理",
            "責務分割の評価",
            "設計原則との照合",
        ]

        analysis = [
            "構造性辞書（STRUCTURE_FEATURES）を使って、コンポーネント・関係性・レイアウトを評価する。",
            "SOLID原則やデザインパターンとの整合性も確認する。",
        ]

        # -------------------------
        # ★ raw_text に応じた追加
        # -------------------------
        if any(k in raw for k in ["複雑", "スパゲッティ", "読みにくい"]):
            analysis.append("構造が複雑化しているため、責務分割や階層化が必要。")

        if any(k in raw for k in ["依存", "結合", "密結合"]):
            analysis.append("依存関係が強すぎる可能性があり、疎結合化が設計改善につながる。")

        if any(k in raw for k in ["拡張", "変更", "将来性"]):
            analysis.append("将来の変更を考慮した拡張性のある設計が求められる。")

        # -------------------------
        # ★ features に応じた追加
        # -------------------------
        if features.get("structure_strength", 0) >= 2:
            analysis.append("構造的な情報が多いため、設計改善の余地が大きい。")

        if features.get("keyword_strength", 0) >= 3:
            analysis.append("設計に関するキーワードが多く、具体的な改善案を提示しやすい。")

        if features.get("context_strength", 0) >= 2:
            analysis.append("文脈が十分にあるため、設計の問題点を正確に把握できる。")

        # -------------------------
        # ★ weak_points に応じた追加
        # -------------------------
        if "構造情報不足" in weak_points:
            analysis.append("構造的な情報が不足しているため、コンポーネントの関係性を再確認する必要がある。")

        if "責務不明確" in weak_points:
            analysis.append("責務分割が不明確であるため、各コンポーネントの役割を明確化する必要がある。")

        if "依存関係不明確" in weak_points:
            analysis.append("依存関係が不明確なため、モジュール間の結合度を再評価する必要がある。")

        conclusion = "設計の良し悪しを評価し、改善すべき構造とその理由を提示する。"

        return {
            "reasoning_type": "design",
            "steps": steps,
            "analysis": analysis,
            "conclusion": conclusion
        }

    def _reason_optimize(self, context: Dict[str, Any]) -> Dict[str, Any]:


        structure_strength = self.extract_features(context["strength"], source_bias=0)
        complexity_score = self
