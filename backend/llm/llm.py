# llm/llm.py

class LLM:

    def format(self, structured_json: dict) -> str:
        """
        JSON を自然な文章に整形する
        """
        lines = []
        lines.append(f"# {structured_json['title']}")

        for sec in structured_json["sections"]:
            lines.append(f"\n## {sec['header']}")

            if "content" in sec:
                for c in sec["content"]:
                    lines.append(f"- {c}")

            if "list" in sec:
                for item in sec["list"]:
                    lines.append(f"- {item}")

            if "steps" in sec:
                for step in sec["steps"]:
                    lines.append(f"1. {step}")

            if "code" in sec:
                lines.append("```python")
                lines.append(sec["code"])
                lines.append("```")

            if "table" in sec:
                lines.append("（表）")
                for row in sec["table"]:
                    lines.append(str(row))

        return "\n".join(lines)
