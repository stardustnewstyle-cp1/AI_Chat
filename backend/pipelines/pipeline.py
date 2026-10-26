from backend.intent_layer.intent_detector import IntentDetector
from backend.reasoning_layer.reasoning_layer import ReasoningLayer
from backend.teacher_layer.teacher_layer import TeacherLayer
from backend.ml.feature_extractor import FeatureExtractor
from backend.ml.level_detector import LevelDetector
from backend.llm.llm import LLM

# クエリ生成器（純粋関数）
from backend.utils.search_query_builder import SearchQueryBuilder

# 外部検索エンジン（httpx）
from backend.external.external_search_engine import ExternalSearchEngine


class Pipeline:
    """
    技術質問専用パイプライン（README の設計思想と完全整合）

    IntentDetector → ReasoningLayer → FeatureExtractor/LevelDetector →
    TeacherLayer（構造化）→ LLM（内容生成）→ UI（カード表示）
    """

    def __init__(self, llm: LLM, external_api_key: str):
        self.llm = llm
        self.intent_detector = IntentDetector()
        self.reasoning_layer = ReasoningLayer()
        self.teacher_layer = TeacherLayer()
        self.extractor = FeatureExtractor()
        self.level_detector = LevelDetector()

        # クエリ生成器（検索実行はしない）
        self.query_builder = SearchQueryBuilder()

        # 外部検索エンジン（httpx）
        self.search_engine = ExternalSearchEngine(api_key=external_api_key)

    # ---------------------------------------------------------
    # 技術質問判定（最優先） ← ★ここが今回の修正ポイント
    # ---------------------------------------------------------
    def _is_technical_question(self, text: str) -> bool:
        lower = text.lower()

        technical_keywords = [
            # 言語
            "python", "javascript", "typescript", "java", "go", "rust",

            # 基本語彙
            "class", "クラス",
            "api", "設計", "implementation", "実装",
            "code", "コード",
            "function", "関数",
            "error", "エラー",
            "bug", "バグ",
            "fix", "修正",
            "refactor", "リファクタ",
            "architecture", "アーキテクチャ",

            # 改善系（追加）
            "改善", "最適化", "高速化", "効率化",

            # 実務語彙
            "backend", "frontend",
            "database", "db", "sql",
            "docker", "kubernetes",
            "system design", "プロジェクト",

            # ローカル参照
            "this code", "this file", "this repository",
            "this function", "this api",

            # 処理系
            "非同期", "同期", "処理", "実行", "ログ",

            # インフラ
            "cache", "redis", "mysql", "postgres",

            # フレームワーク
            "flask", "fastapi", "django",
            "react", "vue", "node", "next",

            # 通信
            "http", "https",
        ]

        # ★日本語では split が機能しないため部分一致が正しい
        return any(keyword in lower for keyword in technical_keywords)

    # ---------------------------------------------------------
    # 外部情報が必要かどうか（判定は最後）
    # ---------------------------------------------------------
    def _should_use_external_search(self, text: str) -> bool:
        lower = text.lower()
        external_keywords = [
            "latest", "latest version", "official docs", "official",
            "spec", "specification", "api docs", "documentation",
            "what is the current", "newest", "how to use the latest",
            "breaking change", "release notes", "compare latest",
            "official guide", "public api",
        ]
        return any(k in lower for k in external_keywords)

    # ---------------------------------------------------------
    # TeacherLayer が読む構造ベクトル
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

        # domain に応じた構造テンプレート
        if domain == "design":
            purpose = "技術的な設計を安全かつ保守しやすく行うための考え方を整理する"
            architecture = "責務を分離し、データの流れと状態管理を明確にして設計する"
            flow = ["要件整理", "責務分離", "状態管理と例外処理", "改善点評価"]
            cautions = ["責務混在は危険", "状態管理が曖昧だとバグ増加", "例外処理不足は障害対応困難"]

        elif domain == "compare":
            purpose = "複数の手法や技術を比較して適切な選択を行う"
            architecture = "比較軸を揃え、機能・性能・保守性・制約を見比べる"
            flow = ["比較軸定義", "手法整理", "利点と制約比較", "結論判断"]
            cautions = ["比較軸が揃わないと誤判断", "運用コストも考慮すべき"]

        elif domain == "steps":
            purpose = "手順を明確にして再現しやすい実行方法を提供する"
            architecture = "前提条件 → 手順 → 中間確認 → 最終確認"
            flow = ["前提確認", "手順実行", "中間チェック", "最終確認"]
            cautions = ["前提条件の見落とし", "順序崩れは再現性低下"]

        elif domain == "caution":
            purpose = "技術的な失敗やトラブルを未然に防ぐポイントを理解する"
            architecture = "リスク → 原因 → 対策 → 再発防止"
            flow = ["リスク洗い出し", "根本原因特定", "対策適用", "再発防止確認"]
            cautions = ["原因見逃しは再発", "対策だけでなく再発防止が必要"]

        elif domain == "improvement":
            purpose = "改善余地を見つけて、より良い設計や実装へ進める"
            architecture = "課題 → 改善方針 → 設計変更 → 効果検証"
            flow = ["課題特定", "改善方針決定", "設計変更", "効果検証"]
            cautions = ["改善が複雑化しすぎないように", "副作用や運用コストも比較"]

        else:
            purpose = "質問の意図を把握して、要点を整理して説明する"
            architecture = "背景 → 要点 → 注意点"
            flow = ["本質把握", "背景と要点整理", "簡潔に説明"]
            cautions = ["前提違いは説明ズレ", "専門用語の多用に注意"]

        if text_clean:
            purpose = f"{purpose}（質問: {text_clean[:40]}{'...' if len(text_clean) > 40 else ''}）"

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
    # メイン処理（local/external 共通）
    # ---------------------------------------------------------
    async def run(self, text: str) -> dict:
        text = text.strip()
        if not text:
            return {
                "title": "入力がありません",
                "sections": [{"header": "入力してください", "content": "質問を入力してください。"}],
            }

        # ① 非技術質問判定 ← ★ここが修正で正しく動くようになる
        if not self._is_technical_question(text):
            return {
                "title": "非技術質問",
                "sections": [{
                    "header": "このAIは技術専用です",
                    "content": "技術に関係ない質問には回答できません。"
                }],
            }

        # ② Intent 判定
        intent_result = self.intent_detector.detect(text)
        domain = intent_result["domain"]
        intent = intent_result["intent"]
        axes = intent_result["axes"]
        score = intent_result["score"]

        # ③ Reasoning 判定
        reasoning_type = self.reasoning_layer.map_domain_to_reasoning(domain)

        # ④ Level 判定
        features = self.extractor.extract(text)
        level = self.level_detector.detect(features)

        # ⑤ 構造ベクトル生成
        reasoning_vector = self._build_response_vector(
            text=text,
            domain=domain,
            intent=intent,
            reasoning_type=reasoning_type,
            level=level,
            axes=axes,
            score=score,
        )

        # ⑥ LLM 内容生成
        llm_content = self.llm.generate(text, domain=domain)
        reasoning_vector.update(llm_content)

        # ⑦ external 判定（最後）
        external_context = None
        if self._should_use_external_search(text):

            # クエリ生成（SearchQueryBuilder）
            queries = self.query_builder.build(text, axes)

            # 外部検索（httpx）
            external_context = await self.search_engine.search(queries[0])

            reasoning_vector["notes"] = (
                "外部情報（公式ドキュメント・公開情報）を補助として統合しています。"
            )

        # ⑧ TeacherLayer による構造化
        teacher_output = self.teacher_layer.run(
            reasoning_vector,
            external_context=external_context
        )
        sections = teacher_output.get("sections", [])

        # ⑨ UI 用返却
        return {
            "intent": intent,
            "reasoning": reasoning_type,
            "level": level,
            "axes": axes,
            "score": score,
            "title": teacher_output.get("title", "回答"),
            "sections": sections,
        }
