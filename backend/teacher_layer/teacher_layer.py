import json
import os


class TeacherLayer:
    def __init__(self):
        path = os.path.join(os.path.dirname(__file__), "..", "models/templates", "teacher_templates.json")
        with open(path, "r", encoding="utf-8") as f:
            self.templates = json.load(f)

    def _format_external(self, external_context):
        if not external_context:
            return None

        return [
            f"{item.get('title', '')} — {item.get('summary', '')}（{item.get('url', '')}）"
            for item in external_context
        ]

    def build_structure(self, reasoning_vector: dict, external_context=None) -> dict:
        domain = reasoning_vector.get("domain", "design")
        sections = self.templates.get(domain, ["purpose", "architecture", "flow", "caution"])

        output = {
            "title": reasoning_vector.get("title", "回答"),
            "sections": []
        }

        formatted_external = self._format_external(external_context)

        for kind in sections:
            block = self._build_section(kind, reasoning_vector, formatted_external)
            if block is not None:
                output["sections"].append(block)

        if formatted_external:
            output["sections"].append({
                "header": "外部情報（補助）",
                "list": formatted_external
            })

        return output

    def _build_section(self, kind: str, rv: dict, external_list=None):

        # --- 共通系 ---
        if kind == "summary":
            return {"header": "概要", "content": rv.get("summary", "")}

        if kind == "steps":
            return {"header": "手順", "steps": rv.get("steps", [])}

        if kind == "differences":
            return {"header": "違い", "list": rv.get("differences", [])}

        if kind == "pros_cons":
            return {
                "header": "メリット・デメリット",
                "pros": rv.get("pros", []),
                "cons": rv.get("cons", [])
            }

        if kind == "architecture":
            return {"header": "構造", "content": rv.get("architecture", "")}

        if kind == "use_cases":
            return {"header": "使いどころ", "list": rv.get("use_cases", [])}

        if kind == "example":
            return {"header": "例", "code": rv.get("example", "")}

        if kind == "caution":
            return {"header": "注意点", "list": rv.get("cautions", [])}

        if kind == "purpose":
            return {"header": "目的", "content": rv.get("purpose", "")}

        if kind == "flow":
            return {"header": "流れ", "steps": rv.get("flow", [])}

        if kind == "conclusion":
            return {"header": "結論", "content": rv.get("conclusion", "")}

        if kind == "notes":
            notes = rv.get("notes", "")
            if external_list:
                return {
                    "header": "補足",
                    "content": notes,
                    "list": external_list
                }
            return {"header": "補足", "content": notes}

        if kind == "anti_patterns":
            return {"header": "アンチパターン", "list": rv.get("anti_patterns", [])}

        if kind == "requirements":
            return {"header": "要件", "list": rv.get("requirements", [])}

        # --- 改善系（今回の追加） ---
        if kind == "issues":
            return {
                "header": "課題",
                "list": rv.get("issues", [])
            }

        if kind == "solutions":
            return {
                "header": "改善方針",
                "list": rv.get("solutions", [])
            }

        if kind == "design_change":
            return {
                "header": "設計変更",
                "content": rv.get("design_change", "")
            }

        if kind == "effect_check":
            return {
                "header": "効果検証",
                "list": rv.get("effect_check", [])
            }

        # --- 未実装セクション ---
        return {
            "header": kind,
            "content": f"[未実装セクション: {kind}]"
        }

    def run(self, reasoning_vector: dict, external_context=None) -> dict:
        return self.build_structure(reasoning_vector, external_context)
