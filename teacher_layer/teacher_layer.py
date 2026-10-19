# teacher_layer/teacher_layer.py

import json
import os

class TeacherLayer:

    def __init__(self):
        """
        分野ごとのテンプレートを JSON から読み込む
        domain（compare, design, steps...）をキーにする
        """
        path = os.path.join(os.path.dirname(__file__), "..", "models", "teacher_templates.json")
        with open(path, "r", encoding="utf-8") as f:
            self.templates = json.load(f)

    def build_structure(self, reasoning_vector: dict) -> dict:
        """
        reasoning_vector は LLM が生成した構造化回答
        domain に応じてテンプレートを選択し、構造化 JSON を生成する
        """
        domain = reasoning_vector["domain"]
        sections = self.templates.get(domain, [])

        output = {
            "title": reasoning_vector.get("title", "回答"),
            "sections": []
        }

        for kind in sections:
            block = self._build_section(kind, reasoning_vector)
            if block:
                output["sections"].append(block)

        return output

    def _build_section(self, kind: str, rv: dict) -> dict:
        """
        kind（セクション種別）に応じて構造ブロックを生成する
        """
        # ここは君のコードのままで完全にOK
        ...
        return None

    def run(self, reasoning_vector: dict) -> dict:
        """
        TeacherLayer の最終出力（構造化 JSON）
        """
        return self.build_structure(reasoning_vector)
