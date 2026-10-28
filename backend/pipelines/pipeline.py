#pipeline.py
from backend.intent_layer.intent_detector import IntentDetector
from backend.reasoning_layer.reasoning_layer import ReasoningLayer
from backend.teacher_layer.teacher_layer import TeacherLayer
from backend.ml.feature_extractor import FeatureExtractor
from backend.ml.level_detector import LevelDetector
from backend.llm.llm import LLM


class Pipeline:
    """
    技術質問専用パイプライン

    IntentDetector
        ↓
    ReasoningLayer
        ↓
    FeatureExtractor / LevelDetector
        ↓
    LLM
        ↓
    TeacherLayer
        ↓
    UI
    """

    def __init__(self, llm: LLM, external_api_key: str = ""):
        self.llm = llm

        self.intent_detector = IntentDetector()
        self.reasoning_layer = ReasoningLayer()
        self.teacher_layer = TeacherLayer()

        self.extractor = FeatureExtractor()
        self.level_detector = LevelDetector()

    def _is_technical_question(self, text: str) -> bool:

        lower = text.lower()

        technical_keywords = [
            "python", "javascript", "typescript", "java", "go", "rust",
            "class", "クラス", "api", "設計", "implementation", "実装",
            "code", "コード", "function", "関数", "error", "エラー",
            "bug", "バグ", "fix", "修正", "refactor", "リファクタ",
            "architecture", "アーキテクチャ", "改善", "最適化", "高速化",
            "効率化", "backend", "frontend", "database", "db", "sql",
            "docker", "kubernetes", "system design", "プロジェクト",
            "this code", "this file", "this repository", "this function",
            "this api", "非同期", "同期", "処理", "実行", "ログ",
            "cache", "redis", "mysql", "postgres", "flask", "fastapi",
            "django", "react", "vue", "node", "next", "http", "https",
            "gpt", "llama", "gemini", "claude", "transformer", "attention",
            "aiモデル", "モデル", "推論", "inference", "gpu", "cuda",
            "nvidia", "amd", "latency", "throughput",
        ]

        return any(keyword in lower for keyword in technical_keywords)

    def _normalize_domain(self, domain: str) -> str:

        mapping = {
            "procedural": "steps",
            "procedure": "steps",
        }

        return mapping.get(domain, domain)

    def _build_response_vector(
        self,
        text: str,
        domain: str,
        intent: str,
        reasoning_type: str,
        level: str,
        axes: dict,
        score: float,
    ) -> dict:

        text_clean = text.strip()

        if domain == "structural":

            purpose = "技術や言語仕様の内部構造や挙動の違いを理解する"
            architecture = "構造差分 → コンパイラ/ランタイム → 実行時挙動"
            flow = ["構造の違いを把握", "内部処理を確認", "実行時影響を整理"]
            cautions = ["古い仕様との差異に注意", "実装依存の挙動に注意"]

        elif intent == "steps":

            purpose = "手順を理解し実装できるようになる"
            architecture = "準備 → 実装 → 動作確認"
            flow = ["前提知識を確認", "コードを書く", "実行して確認"]
            cautions = ["コードの意味を理解する", "エラー内容を確認する"]

        else:

            purpose = "質問の意図を把握して要点を整理する"
            architecture = "背景 → 要点 → 注意点"
            flow = ["本質把握", "背景整理", "簡潔に説明"]
            cautions = ["前提違いによる誤解", "専門用語の多用"]

        purpose = f"{purpose}（質問: {text_clean}）"

        return {
            "domain": domain,
            "intent": intent,
            "reasoning_type": reasoning_type,
            "level": level,
            "axes": axes,
            "score": score,
            "title": "回答",
            "purpose": purpose,
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

        domain = self._normalize_domain(intent_result.get("domain", "explain"))
        intent = intent_result.get("intent", "explain")
        axes = intent_result.get("axes", {})
        score = intent_result.get("score", 0.0)

        reasoning_vector_rl = self.reasoning_layer.run(
            intent_result,
            {"api": {"name": "dummy", "params": []}},
            {"user_input": text},
        )

        reasoning_type = reasoning_vector_rl.get("reasoning_type", "conceptual")

        features = self.extractor.extract(text)
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

        external_context = None

        llm_text = self.llm.generate(text, intent=intent, level=level)

        # ---------------------------------------------------------
        # LLM応答を TeacherLayer が期待する形式へ変換
        # ---------------------------------------------------------
        if domain == "improvement":
            reasoning_vector.update({
                "issues": [llm_text],
                "solutions": [llm_text],
                "design_change": llm_text,
                "effect_check": [llm_text],
            })

        elif domain == "design":
            reasoning_vector.update({
                "purpose": llm_text,
                "architecture": llm_text,
                "flow": [llm_text],
            })

        elif domain == "steps":
            reasoning_vector.update({
                "summary": llm_text,
                "example": llm_text,
            })

        elif domain == "summary":
            reasoning_vector.update({
                "summary": llm_text,
                "conclusion": llm_text,
            })

        elif domain == "example":
            reasoning_vector.update({
                "example": llm_text,
                "notes": llm_text,
            })

        elif domain == "compare":
            # compare は ReasoningLayer が生成するので触らない
            pass

        else:
            reasoning_vector.update({
                "summary": llm_text,
                "example": llm_text,
            })

        # ---------------------------------------------------------
        # デバッグログ
        # ---------------------------------------------------------
        print("\n===== TEACHER INPUT =====")
        for k, v in reasoning_vector.items():
            print(f"{k}: {v}")
        print("=========================\n")

        teacher_output = self.teacher_layer.run(
            reasoning_vector,
            external_context=external_context,
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
