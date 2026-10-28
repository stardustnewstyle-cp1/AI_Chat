import json
import os


class TeacherLayer:
    def __init__(self):
        path = os.path.join(
            os.path.dirname(__file__),
            "..",
            "models/templates",
            "teacher_templates.json",
        )

        with open(path, "r", encoding="utf-8") as f:
            self.templates = json.load(f)

    def _format_external(self, external_context):
        if not external_context:
            return None

        return [
            f"{item.get('title', '')} — "
            f"{item.get('summary', '')}"
            f"（{item.get('url', '')}）"
            for item in external_context
        ]

    def _default_sections_for_domain(self, domain: str):

        if domain == "compare":
            return [
                "summary",
                "differences",
                "pros_cons",
                "use_cases",
                "caution",
            ]

        if domain == "design":
            return [
                "purpose",
                "architecture",
                "flow",
                "caution",
                "anti_patterns",
            ]

        if domain in ("steps", "procedural"):
            return [
                "summary",
                "example",
                "caution",
            ]

        if domain == "caution":
            return [
                "summary",
                "caution",
                "anti_patterns",
            ]

        if domain == "improvement":
            return [
                "summary",
                "issues",
                "solutions",
                "effect_check",
            ]

        if domain == "summary":
            return [
                "summary",
                "conclusion",
                "notes",
            ]

        if domain == "example":
            return [
                "summary",
                "example",
                "notes",
            ]

        if domain == "specification":
            return [
                "summary",
                "requirements",
                "caution",
            ]

        if domain == "systematize":
            return [
                "summary",
                "requirements",
                "notes",
            ]

        return [
            "summary",
            "purpose",
            "notes",
        ]

    def build_structure(
        self,
        reasoning_vector: dict,
        external_context=None,
    ) -> dict:

        # ★★★ デバッグ追加（ここが最重要）★★★
        domain = reasoning_vector.get("domain", "design")
        sections = self.templates.get(domain)
        print(f"\n[DEBUG] TeacherLayer.build_structure domain = {domain}")
        print(f"[DEBUG] TeacherLayer template sections = {sections}")

        if not sections:
            sections = self._default_sections_for_domain(domain)

        output = {
            "title": reasoning_vector.get("title", "回答"),
            "sections": [],
        }

        formatted_external = self._format_external(external_context)

        for kind in sections:

            block = self._build_section(
                kind,
                reasoning_vector,
                formatted_external,
            )

            if block is None:
                continue

            has_content = any(
                key in block and block[key]
                for key in (
                    "content",
                    "list",
                    "steps",
                    "code",
                    "pros",
                    "cons",
                )
            )

            if has_content:
                output["sections"].append(block)

        if formatted_external:
            output["sections"].append(
                {
                    "header": "外部情報（補助）",
                    "list": formatted_external,
                }
            )

        return output

    def _build_section(
        self,
        kind: str,
        rv: dict,
        external_list=None,
    ):

        # ---------------------------------
        # 共通セクション
        # ---------------------------------

        if kind == "summary":
            summary = rv.get("summary", "")
            if not summary:
                return None
            return {
                "header": "概要",
                "content": summary,
            }

        if kind == "steps":
            steps = rv.get("steps", [])
            if steps:
                return {
                    "header": "手順",
                    "steps": steps,
                }
            return None

        if kind == "differences":
            diffs = rv.get("differences", [])
            if not diffs:
                return None
            return {
                "header": "違い",
                "list": diffs,
            }

        if kind == "pros_cons":
            pros = rv.get("pros", [])
            cons = rv.get("cons", [])
            if not pros and not cons:
                return None
            return {
                "header": "メリット・デメリット",
                "pros": pros,
                "cons": cons,
            }

        if kind == "architecture":
            arch = rv.get("architecture", "")
            if not arch:
                return None
            return {
                "header": "構造",
                "content": arch,
            }

        if kind == "use_cases":
            uc = rv.get("use_cases", [])
            if not uc:
                return None
            return {
                "header": "使いどころ",
                "list": uc,
            }

        if kind == "example":
            example = rv.get("example", "")
            if not example:
                return None
            return {
                "header": "例",
                "code": example,
            }

        if kind == "caution":
            cautions = rv.get("cautions", [])
            if not cautions:
                return None
            return {
                "header": "注意点",
                "list": cautions,
            }

        if kind == "purpose":
            purpose = rv.get("purpose", "")
            if not purpose:
                return None
            return {
                "header": "目的",
                "content": purpose,
            }

        if kind == "flow":
            flow = rv.get("flow", [])
            if not flow:
                return None
            return {
                "header": "流れ",
                "steps": flow,
            }

        if kind == "conclusion":
            conc = rv.get("conclusion", "")
            if not conc:
                return None
            return {
                "header": "結論",
                "content": conc,
            }

        if kind == "notes":
            notes = rv.get("notes", "")
            if not notes and not external_list:
                return None
            return {
                "header": "補足",
                "content": notes,
                "list": external_list,
            }

        if kind == "anti_patterns":
            ap = rv.get("anti_patterns", [])
            if not ap:
                return None
            return {
                "header": "アンチパターン",
                "list": ap,
            }

        if kind == "requirements":
            req = rv.get("requirements", [])
            if not req:
                return None
            return {
                "header": "要件",
                "list": req,
            }

        # ---------------------------------
        # 改善系
        # ---------------------------------

        if kind == "issues":
            issues = rv.get("issues", [])
            if not issues:
                return None
            return {
                "header": "課題",
                "list": issues,
            }

        if kind == "solutions":
            sol = rv.get("solutions", [])
            if not sol:
                return None
            return {
                "header": "改善方針",
                "list": sol,
            }

        if kind == "design_change":
            dc = rv.get("design_change", "")
            if not dc:
                return None
            return {
                "header": "設計変更",
                "content": dc,
            }

        if kind == "effect_check":
            ec = rv.get("effect_check", [])
            if not ec:
                return None
            return {
                "header": "効果検証",
                "list": ec,
            }

        return None

    def run(
        self,
        reasoning_vector: dict,
        external_context=None,
    ) -> dict:

        output = self.build_structure(
            reasoning_vector,
            external_context,
        )

        print(
            f"[TeacherLayer] sections_count = "
            f"{len(output.get('sections', []))}"
        )

        return output
