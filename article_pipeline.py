# ============================================
# article_pipeline.py（ArticlePipeline + Intent Layer 統合版）
# ============================================

from .classifier import Classifier
from .level_detector import LevelDetector
from .template_manager import TemplateManager
from .summarizer import Summarizer
from .evaluator import Evaluator
from .improver import Improver
from .validity import ValidityChecker

# Intent Layer（意味解析）
from intent_layer import intent_layer

# 既存の技術推論パイプライン（記事では使わない）
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

        # 技術推論は記事では使わないが残しておく
        self.reasoning_core = ImproverPipeline()

    def run(self, article: str) -> dict:
        """
        Intent Layer を追加して精度向上した記事処理パイプライン
        """

        # --- 1. Intent Layer（意味解析） ---
        intent = intent_layer(article)

        reasoning_type = intent["reasoning_type"]
        axes = intent["axes"]
        final_vector = intent["final_vector"]

        # --- 2. 分類（Intent の意味軸を補助に使う） ---
        category = self.classifier.classify(article, axes=axes)

        # --- 3. レベル判定（構造軸が強いとレベル判定精度が上がる） ---
        level = self.level_detector.detect(article, reasoning_type=reasoning_type)

        # --- 4. テンプレート選択（推論タイプを考慮） ---
        template = self.template_manager.select(category, level, reasoning_type=reasoning_type)

        # --- 5. 要約（意味軸に応じて要約スタイルを変える） ---
        summary = self.summarizer.summarize(
            article,
            template,
            axes=axes,
            reasoning_type=reasoning_type
        )

        # --- 6. 評価（Intent Layer の情報を使って改善可能） ---
        evaluation = self.evaluator.evaluate(
            article,
            axes=axes,
            reasoning_type=reasoning_type
        )

        # --- 7. 改善案（意味軸に応じて改善ポイントを変える） ---
        improvement = self.improver.improve(
            article,
            axes=axes,
            reasoning_type=reasoning_type
        )

        # --- 8. 妥当性チェック ---
        is_valid = self.validity.check(article)

        # --- 9. 統合結果を返す ---
        return {
            "intent": intent,
            "category": category,
            "level": level,
            "template": template,
            "summary": summary,
            "evaluation": evaluation,
            "improvement": improvement,
            "valid": is_valid
        }
