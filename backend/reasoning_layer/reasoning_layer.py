# reasoning_layer.py
class ReasoningLayer:

    def __init__(self):
        # IntentDetector の domain を reasoning_type に変換するマップ
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
            "explain": "conceptual"
        }

        # reasoning_type → Code Generator intent_type
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

    # ============================================================
    # Pipeline から呼ぶ統合インターフェース
    # ============================================================
    def run(self, intent_info, api_info, features):
        """
        intent_info = IntentDetector.run() の返り値
        {
            "domain": ...,
            "intent": ...,
            "axes": ...,
            "score": ...
        }
        """

        domain = intent_info["domain"]
        reasoning_type = self.map_domain_to_reasoning(domain)
        intent_type = self.select_code_intent(reasoning_type)

        code = self.generate_code(api_info, intent_type)

        return {
            "domain": domain,
            "reasoning_type": reasoning_type,
            "intent_type": intent_type,
            "code": code,
            "features": features
        }

    # ============================================================
    # domain → reasoning_type
    # ============================================================
    def map_domain_to_reasoning(self, domain):
        return self.DOMAIN_TO_REASONING.get(domain, "conceptual")

    # ============================================================
    # reasoning_type → Code Generator intent_type
    # ============================================================
    def select_code_intent(self, reasoning_type):
        return self.INTENT_MAP.get(reasoning_type, "design")

    # ============================================================
    # Code Generator（既存ロジック）
    # ============================================================
    def generate_code(self, api_info, intent_type):

        if intent_type == "design":
            return self.generate_design_code(api_info)
        if intent_type == "debug":
            return self.generate_debug_code(api_info)
        if intent_type == "improve":
            return self.generate_improve_code(api_info)
        if intent_type == "compare":
            return self.generate_compare_code(api_info)
        if intent_type == "optimize":
            return self.generate_optimize_code(api_info)

        return "# intent_type が不明です"

    # -------------------------
    # design: 基本コード生成
    # -------------------------
    def generate_design_code(self, api):
        name = api["api"]["name"]
        params = api["api"]["params"]
        usage = api["usage"]["examples"]
        notes = api["notes"]["important"]

        code = []
        code.append("# 基本的な使い方")
        code.append(f"# API: {name}")

        for u in usage[:2]:
            code.append(f"# {u}")

        for n in notes[:2]:
            code.append(f"# 注意: {n}")

        code.append(f"{name}({', '.join(params)})")
        return "\n".join(code)

    # -------------------------
    # debug: 例外処理付きコード
    # -------------------------
    def generate_debug_code(self, api):
        name = api["api"]["name"]
        params = api["api"]["params"]
        exceptions = api["api"]["exceptions"]

        code = []
        code.append("# 例外処理付きコード")
        code.append("try:")
        code.append(f"    result = {name}({', '.join(params)})")

        for e in exceptions[:2]:
            code.append(f"except {e}:")
            code.append(f"    print('Error occurred: {e}')")

        return "\n".join(code)

    # -------------------------
    # improve: 改善コード
    # -------------------------
    def generate_improve_code(self, api):
        name = api["api"]["name"]
        params = api["api"]["params"]
        perf = api["notes"]["performance"]

        code = []
        code.append("# 改善版コード")

        for p in perf[:2]:
            code.append(f"# 性能改善ポイント: {p}")

        code.append(f"{name}({', '.join(params)})")
        return "\n".join(code)

    # -------------------------
    # compare: 比較コード
    # -------------------------
    def generate_compare_code(self, api):
        name = api["api"]["name"]
        params = api["api"]["params"]
        usage = api["usage"]["examples"]

        code = []
        code.append("# API比較コード")

        for u in usage[:2]:
            code.append(f"# 使用例: {u}")

        code.append(f"# パラメータ: {params}")
        return "\n".join(code)

    # -------------------------
    # optimize: 性能最適化コード
    # -------------------------
    def generate_optimize_code(self, api):
        name = api["api"]["name"]
        params = api["api"]["params"]
        perf = api["notes"]["performance"]

        code = []
        code.append("# 性能最適化コード")

        for p in perf[:2]:
            code.append(f"# 性能注意点: {p}")

        code.append(f"{name}({', '.join(params)})")
        return "\n".join(code)
