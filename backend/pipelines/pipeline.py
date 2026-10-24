from backend.intent_layer.intent_detector import IntentDetector
from backend.reasoning_layer.reasoning_layer import ReasoningLayer
from backend.teacher_layer.teacher_layer import TeacherLayer
from backend.ml.feature_extractor import FeatureExtractor
from backend.ml.level_detector import LevelDetector
from backend.llm.llm import LLM


class Pipeline:
    def __init__(self, llm: LLM):
        self.llm = llm
        self.intent_detector = IntentDetector()
        self.reasoning_layer = ReasoningLayer()
        self.teacher_layer = TeacherLayer()
        self.extractor = FeatureExtractor()
        self.level_detector = LevelDetector()

    def _is_technical_question(self, text: str) -> bool:
        """
        技術質問かどうかを簡易的に判定する。
        これが true なら non_technical 判定を通さない。
        """
        lower = text.lower()
        technical_keywords = [
            "python",
            "javascript",
            "typescript",
            "java",
            "go",
            "rust",
            "class",
            "クラス",
            "api",
            "api docs",
            "design",
            "設計",
            "implementation",
            "実装",
            "code",
            "コード",
            "function",
            "関数",
            "error",
            "エラー",
            "bug",
            "バグ",
            "fix",
            "修正",
            "refactor",
            "リファクタ",
            "architecture",
            "アーキテクチャ",
            "backend",
            "frontend",
            "database",
            "db",
            "sql",
            "docker",
            "kubernetes",
            "system design",
            "プロジェクト",
            "this code",
            "this file",
            "this repository",
            "this function",
            "this api",
        ]
        return any(keyword in lower for keyword in technical_keywords)

    def _should_use_internal_search(self, text: str) -> bool:
        """
        外部公式情報が必要かどうかを判定する。
        ここで true になった場合、ユーザーには見えない内部検索を使う。
        """
        lower = text.lower()
        external_keywords = [
            "latest",
            "latest version",
            "official docs",
            "official",
            "spec",
            "specification",
            "api docs",
            "documentation",
            "what is the current",
            "newest",
            "how to use the latest",
            "breaking change",
            "release notes",
            "compare latest",
            "official guide",
            "public api",
        ]
        if any(k in lower for k in external_keywords):
            return True

        # 典型的なローカル質問なら false
        local_keywords = [
            "this code",
            "this file",
            "this repository",
            "this api",
            "this module",
            "error",
            "design",
            "implementation",
            "this function",
            "class",
            "import",
            "bug",
            "fix",
            "refactor",
            "architecture",
            "backend",
            "frontend",
        ]
        if any(k in lower for k in local_keywords):
            return False

        return True

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
        """
        TeacherLayer が期待するキーをここで生成する。
        これがないと、TeacherLayer は空文字・空配列しか作れない。
        既存のインターフェースを壊さず、Pipeline だけで本文データを補う。
        """
        text_clean = text.strip()

        if domain == "design":
            purpose = "技術的な設計を安全かつ保守しやすく行うための考え方を整理する"
            architecture = "責務を分離し、データの流れと状態管理を明確にして設計する"
            flow = [
                "要件を整理する",
                "責務を分離する",
                "状態管理と例外処理を設計する",
                "改善点を評価する",
            ]
            cautions = [
                "責務が混ざると保守性が落ちる",
                "状態管理が曖昧だとバグが増える",
                "例外処理を省略すると障害対応が難しくなる",
            ]

        elif domain == "compare":
            purpose = "複数の手法や技術を比較して適切な選択を行う"
            architecture = "比較軸を揃えて、機能・性能・保守性・制約を見比べる"
            flow = [
                "比較軸を定義する",
                "各手法を整理する",
                "利点と制約を比較する",
                "結論を判断する",
            ]
            cautions = [
                "比較軸が揃っていないと誤判断になる",
                "運用コストや制約も考慮する必要がある",
            ]

        elif domain == "steps":
            purpose = "手順を明確にして再現しやすい実行方法を提供する"
            architecture = "前提条件・手順・確認ポイントを順に整理する"
            flow = [
                "前提条件を確認する",
                "手順を順に実行する",
                "中間結果をチェックする",
                "最終結果を確認する",
            ]
            cautions = [
                "前提条件を見落とすと失敗しやすい",
                "順序が崩れると再現しにくくなる",
            ]

        elif domain == "caution":
            purpose = "技術的な失敗やトラブルを未然に防ぐポイントを理解する"
            architecture = "発生しやすい問題とその防止策を整理する"
            flow = [
                "発生しうるリスクを洗い出す",
                "根本原因を特定する",
                "対策を適用する",
                "再発防止を確認する",
            ]
            cautions = [
                "根本原因を見逃すと同じ問題が再発する",
                "対策だけでなく再発防止も必要",
            ]

        elif domain == "improvement":
            purpose = "改善余地を見つけて、より良い設計や実装へ進める"
            architecture = "現状の課題、改善方針、効果を整理して判断する"
            flow = [
                "現在の課題を特定する",
                "改善方針を決める",
                "設計を変更する",
                "効果を検証する",
            ]
            cautions = [
                "改善が複雑化しすぎないようにする",
                "副作用や運用コストも比較する",
            ]

        else:
            purpose = "質問の意図を把握して、要点を整理して説明する"
            architecture = "背景・要点・注意点を簡潔に構造化して伝える"
            flow = [
                "質問の本質を把握する",
                "背景と要点を整理する",
                "説明を簡潔にまとめる",
            ]
            cautions = [
                "前提が違うと説明がズレる",
                "専門用語を多用しすぎない",
            ]

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

    def run(self, text: str):
        text = text.strip()
        if not text:
            return {
                "title": "入力がありません",
                "sections": [
                    {
                        "header": "入力してください",
                        "content": "質問を入力してください。"
                    }
                ]
            }

        # ここが重要:
        # 技術キーワードがあるなら、まず技術質問として扱う
        if self._is_technical_question(text):
            intent_result = self.intent_detector.detect(text)
            domain = intent_result["domain"]
        else:
            intent_result = {"domain": "non_technical", "intent": "general", "axes": {}, "score": 0.0}

        # 2. 非技術質問
        if intent_result.get("domain") == "non_technical":
            return {
                "title": "非技術質問",
                "sections": [
                    {
                        "header": "このAIは技術専用です",
                        "content": "技術に関係ない質問には回答できません。"
                    }
                ]
            }

        # 3. 内部検索を使うべきかどうかを判定
        use_internal_search = self._should_use_internal_search(text)

        # 4. 既存のロジックをそのまま使う
        intent = intent_result.get("intent")
        axes = intent_result.get("axes")
        score = intent_result.get("score")
        reasoning_type = self.reasoning_layer.map_domain_to_reasoning(domain)

        features = self.extractor.extract(text)
        level = self.level_detector.detect(features)

        reasoning_vector = self._build_response_vector(
            text=text,
            domain=domain,
            intent=intent,
            reasoning_type=reasoning_type,
            level=level,
            axes=axes,
            score=score,
        )

        # ここが重要:
        # 追加の外部補助情報が必要なら、ユーザーには見せずに使う
        if use_internal_search:
            internal_context = (
                "公式ドキュメントと公開情報を補助として確認し、"
                "最新仕様と一般的な実装方法に沿って回答する。"
            )
            reasoning_vector["notes"] = internal_context

        print("REASONING_VECTOR:", reasoning_vector)

        teacher_output = self.teacher_layer.run(reasoning_vector)
        print("TEACHER OUTPUT:", teacher_output)

        sections = teacher_output.get("sections", []) if isinstance(teacher_output, dict) else []

        return {
            "intent": intent,
            "reasoning": reasoning_type,
            "level": level,
            "score": score,
            "sections": sections,
        }