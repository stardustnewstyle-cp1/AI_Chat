# pipeline.py

from .classifier import Classifier
from .level_detector import LevelDetector
from .template_manager import TemplateManager
from .summarizer import Summarizer
from .evaluator import Evaluator
from .improver import Improver
from .validity import ValidityChecker

# Intent Layer + Reasoning Layer + Knowledge Layer
from intent_layer import intent_layer
from improver_pipeline import ImproverPipeline


class ArticlePipeline:
    def __init__(self):
        # 既存モジュール
        self.classifier = Classifier()
        self.level_detector = LevelDetector()
        self.template_manager = TemplateManager()
        self.summarizer = Summarizer()
        self.evaluator = Evaluator()
        self.improver = Improver()
        self.validity = ValidityChecker()

        # 新規：Intent Layer + Reasoning Layer 統合パイプライン
        self.reasoning_core = ImproverPipeline()

    def run(self, article: str) -> dict:
        """
        Intent Layer → Technical Reasoning → Knowledge Layer を統合した
        新型の「脳を持つ」記事処理パイプライン
        """

        # --- 1. Intent Layer + Reasoning Layer + Knowledge Layer ---
        reasoning_bundle = self.reasoning_core.reasoning(article)

        intent = reasoning_bundle["intent"]
        reasoning_type = intent["reasoning_type"]
        final_vector = intent["final_vector"]

        # --- 2. 分類（Intent を使って精度向上可能） ---
        category = self.classifier.classify(article)

        # --- 3. レベル判定 ---
        level = self.level_detector.detect(article)

        # --- 4. テンプレート選択（推論タイプを考慮可能） ---
        template = self.template_manager.select(category, level)

        # --- 5. 要約 ---
        summary = self.summarizer.summarize(article, template)

        # --- 6. 評価（Intent Layer の情報を使って改善可能） ---
        evaluation = self.evaluator.evaluate(article)

        # --- 7. 改善案（Teacher Layer の入力になる） ---
        improvement = self.improver.improve(article)

        # --- 8. 妥当性チェック ---
        is_valid = self.validity.check(article)

        # --- 9. 統合結果を返す ---
        return {
            "intent": intent,
            "technical_reasoning": reasoning_bundle["technical_reasoning"],
            "search_queries": reasoning_bundle["search_queries"],
            "category": category,
            "level": level,
            "template": template,
            "summary": summary,
            "evaluation": evaluation,
            "improvement": improvement,
            "valid": is_valid
        }
