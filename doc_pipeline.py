#doc_pipeline.py
import requests
from bs4 import BeautifulSoup

class DocPipeline:
    def __init__(self, router, normalizer):
        self.router = router
        self.normalizer = normalizer

    def run(self, intent_result, mode="text"):
        """
        mode = "text" → 従来の要約モード
        mode = "code" → 構造化抽出モード（コード再構築用）
        """

        # 1. 公式ドキュメントURLを決定
        url = self.router.select_doc_source(intent_result)

        # 2. ドキュメント取得
        raw_text = self.fetch(url)

        # -------------------------
        # ★ 新モード：コード再構築モード
        # -------------------------
        if mode == "code":
            structured = self.extract_api_structure(raw_text)
            return structured

        # -------------------------
        # ★ 従来モード：テキスト抽出モード
        # -------------------------
        section = self.extract_section(raw_text, intent_result)
        jp_text = self.normalizer.to_japanese(section)
        summary = self.summarize(jp_text)
        validated = self.evaluate(summary)
        return validated

    # ---------------------------------------------------------
    # 1. fetch: 公式ドキュメント取得
    # ---------------------------------------------------------
    def fetch(self, url):
        try:
            response = requests.get(url, timeout=5)
            response.raise_for_status()
        except Exception:
            fallback_url = self.router.fallback_source(url)
            response = requests.get(fallback_url, timeout=5)

        soup = BeautifulSoup(response.text, "html.parser")
        text = soup.get_text(separator="\n")
        return text

    # ---------------------------------------------------------
    # 2. extract_section: 従来の意味軸ベース抽出
    # ---------------------------------------------------------
    def extract_section(self, raw_text, intent_result):
        intent = intent_result["intent"]

        patterns = {
            "design": ["design", "architecture", "structure", "component"],
            "debug": ["error", "exception", "troubleshoot", "fix"],
            "improve": ["best practice", "optimize", "performance"],
            "compare": ["difference", "compare", "vs", "contrast"],
            "optimize": ["optimize", "performance", "speed", "efficiency"]
        }

        keywords = patterns.get(intent, [])
        lines = raw_text.split("\n")
        extracted = []

        for line in lines:
            lower = line.lower()
            if any(k in lower for k in keywords):
                extracted.append(line)

        if len(extracted) < 5:
            extracted = [line for line in lines if line.strip().startswith("#") or line.strip().startswith("##")]

        return "\n".join(extracted)

    # ---------------------------------------------------------
    # ★ 構造化抽出ロジック（コード再構築モード）
    # ---------------------------------------------------------
    def extract_api_structure(self, raw_text):
        lines = raw_text.split("\n")

        api_name = None
        signature = None
        params = []
        param_types = []
        returns = None
        exceptions = []
        constraints = []
        usage_examples = []
        notes_important = []
        notes_caution = []
        notes_performance = []

        for line in lines:
            lower = line.lower()

            # 関数名・クラス名・メソッド名
            if line.strip().startswith("def ") or "function" in lower or "class " in lower:
                api_name = line.strip()

            # シグネチャ
            if "signature" in lower:
                signature = line.strip()

            # 引数
            if any(k in lower for k in ["param", "argument", "args"]):
                params.append(line.strip())

            # 戻り値
            if "return" in lower:
                returns = line.strip()

            # 例外
            if any(k in lower for k in ["error", "exception", "raises"]):
                exceptions.append(line.strip())

            # 制約
            if any(k in lower for k in ["must", "required", "constraint", "should not", "cannot"]):
                constraints.append(line.strip())

            # 使用例
            if any(k in lower for k in ["example", "usage", "how to use"]):
                usage_examples.append(line.strip())

            # 注意点
            if "important" in lower or "note" in lower:
                notes_important.append(line.strip())

            if "caution" in lower or "warning" in lower:
                notes_caution.append(line.strip())

            if "performance" in lower:
                notes_performance.append(line.strip())

        return {
            "api": {
                "name": api_name,
                "signature": signature,
                "params": params,
                "param_types": param_types,
                "returns": returns,
                "exceptions": exceptions,
                "constraints": constraints,
            },
            "usage": {
                "examples": usage_examples,
            },
            "notes": {
                "important": notes_important,
                "caution": notes_caution,
                "performance": notes_performance,
            }
        }

    # ---------------------------------------------------------
    # 3. summarize: 従来の要約
    # ---------------------------------------------------------
    def summarize(self, text):
        lines = text.split("\n")
        cleaned = [l.strip() for l in lines if len(l.strip()) > 0]

        important = []
        for line in cleaned:
            if any(word in line.lower() for word in ["use", "should", "important", "note", "recommended"]):
                important.append(line)

        if len(important) == 0:
            important = cleaned[:10]

        summary = "\n".join(f"- {line}" for line in important[:12])
        return summary

    # ---------------------------------------------------------
    # 4. evaluate: 技術的正確性チェック
    # ---------------------------------------------------------
    def evaluate(self, text):
        return text
