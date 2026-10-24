# teacher_layer/teacher_layer.py

import json
import os


class TeacherLayer:
    def __init__(self):
        """
        分野ごとのテンプレートを JSON から読み込む
        domain（compare, design, steps...）をキーにする
        """
        path = os.path.join(os.path.dirname(__file__), "..", "models/templates", "teacher_templates.json")
        with open(path, "r", encoding="utf-8") as f:
            self.templates = json.load(f)

    def build_structure(self, reasoning_vector: dict) -> dict:
        """
        reasoning_vector は LLM が生成した構造化回答
        domain に応じてテンプレートを選択し、構造化 JSON を生成する
        """
        domain = reasoning_vector.get("domain", "design")
        sections = self.templates.get(domain, ["purpose", "architecture", "flow", "caution"])

        output = {
            "title": reasoning_vector.get("title", "回答"),
            "sections": []
        }

        for kind in sections:
            block = self._build_section(kind, reasoning_vector)
            if block is not None:
                output["sections"].append(block)

        return output

    def _build_section(self, kind: str, rv: dict):
        """
        kind（セクション種別）に応じて構造ブロックを生成する
        """

        # --- Summary ---
        if kind == "summary":
            return {"header": "概要", "content": rv.get("summary", "")}

        # --- Steps ---
        if kind == "steps":
            return {"header": "手順", "steps": rv.get("steps", [])}

        # --- Differences ---
        if kind == "differences":
            return {"header": "違い", "list": rv.get("differences", [])}

        # --- Pros & Cons ---
        if kind == "pros_cons":
            return {"header": "メリット・デメリット", "pros": rv.get("pros", []), "cons": rv.get("cons", [])}

        # --- Architecture ---
        if kind == "architecture":
            return {"header": "構造", "content": rv.get("architecture", "")}

        # --- Use Cases ---
        if kind == "use_cases":
            return {"header": "使いどころ", "list": rv.get("use_cases", [])}

        # --- Example ---
        if kind == "example":
            return {"header": "例", "code": rv.get("example", "")}

        # --- Caution ---
        if kind == "caution":
            return {"header": "注意点", "list": rv.get("cautions", [])}

        # --- Purpose ---
        if kind == "purpose":
            return {"header": "目的", "content": rv.get("purpose", "")}

        # --- Flow ---
        if kind == "flow":
            return {"header": "流れ", "steps": rv.get("flow", [])}

        # --- Conclusion ---
        if kind == "conclusion":
            return {"header": "結論", "content": rv.get("conclusion", "")}

        # --- Notes ---
        if kind == "notes":
            return {"header": "補足", "content": rv.get("notes", "")}

        # --- Anti-patterns ---
        if kind == "anti_patterns":
            return {"header": "アンチパターン", "list": rv.get("anti_patterns", [])}

        # --- Requirements ---
        if kind == "requirements":
            return {"header": "要件", "list": rv.get("requirements", [])}

        # --- Default ---
        return {
            "header": kind,
            "content": f"[未実装セクション: {kind}]"
        }

    def run(self, reasoning_vector: dict) -> dict:
        """
        TeacherLayer の最終出力（構造化 JSON）
        """
        return self.build_structure(reasoning_vector)