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
    IntentDetector → ReasoningLayer → FeatureExtractor/LevelDetector
    → TeacherLayer（構造化）→ LLM（内容生成）→ UI（カード表示）
    """

    def __init__(self, llm: LLM, external_api_key: str = ""):
        # ★ FastAPI 側から渡された LLM（DummyModelClient）を使う
        self.llm = llm

        self.intent_detector = IntentDetector()
        self.reasoning_layer = ReasoningLayer()
        self.teacher_layer = TeacherLayer()
        self.extractor = FeatureExtractor()
        self.level_detector = LevelDetector()

    # ---------------------------------------------------------
    # 技術質問判定
    # ---------------------------------------------------------
    def _is_technical_question(self, text: str) -> bool:
        lower = text.lower()
        technical_keywords = [
            "python", "javascript", "typescript", "java", "go", "rust",
            "class", "クラス", "api", "設計", "implementation", "実装",
            "code", "コード", "function", "関数", "error", "エラー",
            "bug", "バグ", "fix", "修正", "refactor", "リファクタ",
            "architecture", "アーキテクチャ", "改善", "最適化",
            "高速化", "効率化", "backend", "frontend", "database",
            "db", "sql", "docker", "kubernetes", "system design",
            "プロジェクト", "this code", "this file", "this repository",
            "this function", "this api", "非同期", "同期", "処理",
            "実行", "ログ",            "cache", "redis", "mysql", "postgres",
            "flask", "fastapi", "django", "react", "vue", "node",
            "next", "http", "https", "gpt", "llama", "gemini",
            "claude", "diffusion", "stable diffusion", "sdxl",
            "transformer", "attention", "aiモデル", "モデル",
            "推論", "inference", "gpu", "cuda", "nvidia", "amd",
            "latency", "throughput",
        ]
        return any(keyword in lower for keyword in technical_keywords)

    # ---------------------------------------------------------
    # TeacherLayer 用構造ベクトル
    # ---------------------------------------------------------
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
            purpose = "技術や言語仕様の内部構造や挙動の違いを整理して理解する"
            architecture = "構造差分 → コンパイラ／ランタイムでの扱い → 実行時の挙動"
            flow = ["構造の違い把握", "コンパイラ内部処理の差分", "実行時影響の整理"]
            cautions = ["古い仕様と新しい仕様の混在に注意", "コンパイラ依存の挙動を誤解しない"]
        else:
            purpose = "質問の意図を把握して、要点を整理して説明する"
            architecture = "背景 → 要点 → 注意点"
            flow = ["本質把握", "背景と要点整理", "簡潔に説明"]
            cautions = ["前提違いは説明ズレ", "専門用語の多用に注意"]

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

    # ---------------------------------------------------------
    # メイン処理
    # ---------------------------------------------------------
    async def run(self, text: str) -> dict:

        text = text.strip()
        if not text:
            return {
                "title": "入力がありません",
                "sections": [{"header": "入力してください", "content": "質問を入力してください。"}],
            }

        if not self._is_technical_question(text):
            return {
                "title": "非技術質問",
                "sections": [{
                    "header": "このAIは技術専用です",
                    "content": "技術に関係ない質問には回答できません。"
                }],
            }

        intent_result = self.intent_detector.detect(text)
        domain = intent_result["domain"]
        intent = intent_result["intent"]
        axes = intent_result["axes"]
        score = intent_result["score"]

        reasoning_vector_rl = self.reasoning_layer.run(
            intent_result,
            {"api": {"name": "dummy", "params": []}},
            {"user_input": text or "内容がありません"}
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

        # ---------------------------------------------------------
        # ★ 外部検索は無効化
        # ---------------------------------------------------------
        external_context = None

        # ---------------------------------------------------------
        # LLM（DummyModelClient）
        # ---------------------------------------------------------
        llm_content = self.llm.generate(text or "内容がありません")
        reasoning_vector["llm_output"] = llm_content

        teacher_output = self.teacher_layer.run(
            reasoning_vector,
            external_context=external_context
        )

        sections = teacher_output.get("sections", [])

        return {
            "intent": intent,
            "reasoning": reasoning_type,
            "level": level,
            "axes": axes,
            "score": score,
            "title": teacher_output.get("title", "回答"),
            "sections": sections,
        }
