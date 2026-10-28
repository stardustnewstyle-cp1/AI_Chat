# backend/pipeline.py
from backend.intent_layer.intent_detector import IntentDetector
from backend.reasoning_layer.reasoning_layer import ReasoningLayer
from backend.teacher_layer.teacher_layer import TeacherLayer
from backend.ml.feature_extractor import FeatureExtractor
from backend.ml.level_detector import LevelDetector
from backend.llm.llm import LLM


class Pipeline:
    """
    技術質問専用パイプライン
    Intent → Reasoning → Feature/Level → LLM → TeacherLayer → UI
    """

    def __init__(self, llm: LLM, external_api_key: str = ""):
        self.llm = llm
        self.external_api_key = external_api_key
        self.intent_detector = IntentDetector()
        self.reasoning_layer = ReasoningLayer()
        self.teacher_layer = TeacherLayer()
        self.extractor = FeatureExtractor()
        self.level_detector = LevelDetector()

    def _is_technical_question(self, text: str) -> bool:
        lower = text.lower()
        keywords = [
            "python", "class", "クラス", "function", "関数",
            "error", "エラー", "設計", "architecture",
            "コード", "実装", "api", "backend", "frontend",
        ]
        return any(k in lower for k in keywords)

    def _normalize_domain(self, domain: str, intent: str) -> str:
        mapping = {"procedural": "steps", "procedure": "steps"}
        base = mapping.get(domain, domain)
        if base in ("", None):
            return {
                "steps": "steps",
                "compare": "compare",
                "summary": "summary",
                "improvement": "improvement",
                "design": "design",
            }.get(intent, "summary")
        return base

    def _build_response_vector(self, text, domain, intent, reasoning_type, level, axes, score):
        text_clean = text.strip()

        if domain == "steps":
            purpose = "手順を理解し実装できるようになる"
            architecture = "準備 → 実装 → 動作確認"
            flow = ["前提知識を確認", "コードを書く", "実行して確認"]
            cautions = ["コードの意味を理解する", "エラー内容を確認する"]

        elif domain == "design":
            purpose = "設計意図を理解し、構造を整理する"
            architecture = "責務分離 → 拡張性 → 保守性"
            flow = ["目的整理", "構造化", "改善点の抽出"]
            cautions = ["過剰設計を避ける", "依存関係に注意"]

        else:
            purpose = "質問の意図を把握して要点を整理する"
            architecture = "背景 → 要点 → 注意点"
            flow = ["本質把握", "背景整理", "簡潔に説明"]
            cautions = ["前提違いによる誤解", "専門用語の多用"]

        return {
            "domain": domain,
            "intent": intent,
            "reasoning_type": reasoning_type,
            "level": level,
            "axes": axes,
            "score": score,
            "title": "回答",
            "purpose": f"{purpose}（質問: {text_clean}）",
            "architecture": architecture,
            "flow": flow,
            "cautions": cautions,
        }

    async def run(self, text: str) -> dict:
        text = text.strip()

        if not text:
            return {
                "title": "入力がありません",
                "sections": [
                    {"header": "入力してください", "content": "質問を入力してください。"}
                ],
            }

        if not self._is_technical_question(text):
            return {
                "title": "非技術質問",
                "sections": [
                    {"header": "このAIは技術専用です", "content": "技術に関係ない質問には回答できません。"}
                ],
            }

        intent_result = self.intent_detector.detect(text)
        intent = intent_result.get("intent", "explain")
        raw_domain = intent_result.get("domain", "summary")
        axes = intent_result.get("axes", {})
        score = intent_result.get("score", 0.0)

        domain = self._normalize_domain(raw_domain, intent)

        reasoning_vector_rl = self.reasoning_layer.run(
            intent_result,
            {"api": {"name": "dummy", "params": []}},
            {"user_input": text},
        )
        reasoning_type = reasoning_vector_rl.get("reasoning_type", "conceptual")

        features = self.extractor.extract(text)

        # ★★★ 最重要修正：LevelDetector に domain を渡す ★★★
        features["domain"] = domain

        level = self.level_detector.detect(features)

        reasoning_vector = reasoning_vector_rl.copy()
        reasoning_vector.update(
            self._build_response_vector(
                text=text,
                domain=domain,
                intent=intent,
                reasoning_type=reasoning_type,
                level=level,
                axes=axes,
                score=score,
            )
        )

        llm_text = self.llm.generate(text, intent=intent, level=level)

        # ---------------------------------------------------------
        # ★ LLM応答を TeacherLayer が期待する形式へ変換
        # ---------------------------------------------------------

        if domain == "compare":
            pass

        elif domain == "steps":
            reasoning_vector.update({
                "summary": llm_text,
                "example": "",
                "notes": "",
            })

        elif domain == "design":
            reasoning_vector.update({
                "summary": llm_text,
                "purpose": reasoning_vector.get("purpose", ""),
                "architecture": reasoning_vector.get("architecture", ""),
                "flow": reasoning_vector.get("flow", []),
                "cautions": reasoning_vector.get("cautions", []),
                "anti_patterns": reasoning_vector.get("anti_patterns", []),
                "example": "",
                "notes": "",
            })

        elif domain == "improvement":
            reasoning_vector.update({
                "summary": llm_text,
                "issues": [llm_text],
                "solutions": [llm_text],
                "effect_check": [llm_text],
                "design_change": llm_text,
                "example": "",
                "notes": "",
            })

        elif domain == "summary":
            reasoning_vector.update({
                "summary": llm_text,
                "conclusion": llm_text,
                "example": "",
                "notes": "",
            })

        else:
            reasoning_vector.update({
                "summary": llm_text,
                "example": "",
                "notes": "",
            })

        # ★★★ TeacherLayer に渡す直前の中身を全部出す（デバッグ）★★★
        print("\n[DEBUG] reasoning_vector passed to TeacherLayer:")
        for k, v in reasoning_vector.items():
            print(f"  {k}: {repr(v)}")

        teacher_output = self.teacher_layer.run(
            reasoning_vector,
            external_context=None,
        )

        return {
            "intent": intent,
            "reasoning": reasoning_type,
            "level": level,
            "axes": axes,
            "score": score,
            "title": teacher_output.get("title", "回答"),
            "sections": teacher_output.get("sections", []),
        }
