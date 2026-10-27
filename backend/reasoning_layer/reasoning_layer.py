# reasoning_layer.py

import re

class ReasoningLayer:
    def __init__(self):
        self.DOMAIN_TO_REASONING = {
            "compare": "comparative",
            "design": "structural",
            "steps": "procedural",
            "caution": "causal",
            "improvement": "improvement",
            "summary": "conceptual",
            "example": "example",
            "specification": "factual",
            "systematize": "organizational",
            "explain": "conceptual",
            "non_technical": "conceptual"
        }

        self.INTENT_MAP = {
            "structural": "design",
            "procedural": "design",
            "conceptual": "design",
            "organizational": "design",
            "comparative": "compare",
            "improvement": "improve",
            "causal": "debug",
            "selective": "optimize",
            "example": "design",
            "factual": "design",
            "compare": "compare",
            "debug": "debug",
            "improve": "improve",
            "optimize": "optimize",
            "design": "design"
        }

        self.COMPARE_KEYWORDS = [
            "openai", "meta", "google", "anthropic",
            "gpt", "llama", "gemini", "claude",
            "diffusion", "stable diffusion", "sdxl",
            "transformer",
            "gpu", "cpu", "cuda", "nvidia", "amd"
        ]

    def run(self, intent_info, api_info, features):
        domain = intent_info["domain"]
        reasoning_type = self.map_domain_to_reasoning(domain)
        intent_type = self.select_code_intent(reasoning_type)

        code = self.generate_code(api_info, intent_type)
        user_text = features.get("user_input", "")

        rv = {
            "domain": domain,
            "reasoning_type": reasoning_type,
            "intent_type": intent_type,
            "code": code,
            "features": features
        }

        # compare は特別処理
        if domain == "compare":
            targets = self.extract_targets(user_text.lower())
            axes = self.extract_axes(targets)

            rv["summary"] = self.build_summary(targets, axes)
            rv["differences"] = self.build_differences(targets, axes)
            rv["pros"] = self.build_pros(targets, axes)
            rv["cons"] = self.build_cons(targets, axes)
            rv["use_cases"] = self.build_use_cases(targets, axes)
            rv["cautions"] = self.build_cautions(targets, axes)
            return rv

        # 汎用素材生成
        base = user_text.strip() or "情報が不足しています。"

        if domain == "explain":
            rv["summary"] = base
            rv["example"] = base     
            rv["cautions"] = ["前提条件やバージョン差異に注意してください。"]

        elif domain == "design":
            rv["purpose"] = base
            rv["requirements"] = [base]
            rv["architecture"] = base
            rv["flow"] = [base]
            rv["cautions"] = ["設計変更の影響範囲に注意してください。"]

        elif domain == "steps":
            rv["steps"] = [base]
            rv["notes"] = base
            rv["cautions"] = ["前提条件を確認してください。"]

        elif domain == "improvement":
            rv["issues"] = [base]
            rv["solutions"] = [base]
            rv["design_change"] = base
            rv["effect_check"] = [base]
            rv["cautions"] = ["仕様変更の影響範囲を確認してください。"]

        elif domain == "summary":
            rv["summary"] = base
            rv["conclusion"] = base

        elif domain == "example":
            rv["example"] = base
            rv["notes"] = base

        elif domain == "specification":
            rv["requirements"] = [base]
            rv["constraints"] = [base]
            rv["rules"] = [base]

        elif domain == "systematize":
            rv["summary"] = base
            rv["use_cases"] = [base]
            rv["cautions"] = ["適用範囲を確認してください。"]

        return rv

    # compare 専用ロジック
    def extract_targets(self, text):
        found = [kw for kw in self.COMPARE_KEYWORDS if kw in text]
        return found[:2] if len(found) >= 2 else found

    def extract_axes(self, targets):
        axes = []
        if any(t in targets for t in ["gpu", "cpu", "cuda", "nvidia", "amd"]):
            axes += ["速度", "最適化", "メモリ効率", "安定性"]
        if any(t in targets for t in ["diffusion", "stable diffusion", "sdxl"]):
            axes += ["画像生成品質", "計算コスト", "モデル構造"]
        if any(t in targets for t in ["transformer", "gpt", "llama", "claude"]):
            axes += ["言語処理性能", "推論速度", "モデル構造"]
        if "openai" in targets or "meta" in targets:
            axes += ["最適化方針", "GPU効率", "環境依存性"]
        return list(set(axes))

    def build_summary(self, targets, axes):
        if len(targets) < 2:
            return "比較対象が十分に抽出できませんでした。"
        return f"{targets[0]} と {targets[1]} の比較概要です（軸: {', '.join(axes)}）。"

    def build_differences(self, targets, axes):
        if len(targets) < 2:
            return []
        t1, t2 = targets[0], targets[1]
        return [f"{t1} と {t2} は {axis} の設計方針が異なる" for axis in axes]

    def build_pros(self, targets, axes):
        if len(targets) < 2:
            return []
        t1 = targets[0]
        return [f"{t1} は {axis} に強みがある可能性がある" for axis in axes]

    def build_cons(self, targets, axes):
        if len(targets) < 2:
            return []
        t2 = targets[1]
        return [f"{t2} は {axis} に課題が残る可能性がある" for axis in axes]

    def build_use_cases(self, targets, axes):
        if len(targets) < 2:
            return []
        t1, t2 = targets[0], targets[1]
        return [
            msg
            for axis in axes
            for msg in (
                f"{axis} を重視するなら {t1}",
                f"{axis} の最適化を優先するなら {t2}"
            )
        ]

    def build_cautions(self, targets, axes):
        return [
            f"{axis} は環境差によって結果が変動する可能性がある"
            for axis in axes
        ]

    def map_domain_to_reasoning(self, domain):
        return self.DOMAIN_TO_REASONING.get(domain, "conceptual")

    def select_code_intent(self, reasoning_type):
        return self.INTENT_MAP.get(reasoning_type, "design")

    def generate_code(self, api_info, intent_type):
        return "# code generation placeholder"
