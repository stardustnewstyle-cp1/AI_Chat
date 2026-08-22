from .classifier import Classifier
from .level_detector import LevelDetector
from .template_manager import TemplateManager
from .summarizer import Summarizer
from .evaluator import Evaluator
from .improver import Improver
from .validity import ValidityChecker


class ArticlePipeline:
    def __init__(self):
        # 各モジュールを初期化
        self.classifier = Classifier()
        self.level_detector = LevelDetector()
        self.template_manager = TemplateManager()
        self.summarizer = Summarizer()
        self.evaluator = Evaluator()
        self.improver = Improver()
        self.validity = ValidityChecker()

    def run(self, article: str) -> dict:
        """記事を処理して結果をまとめて返す"""

        # 1. 分類
        category = self.classifier.classify(article)

        # 2. レベル判定
        level = self.level_detector.detect(article)

        # 3. テンプレート選択
        template = self.template_manager.select(category, level)

        # 4. 要約
        summary = self.summarizer.summarize(article, template)

        # 5. 評価
        evaluation = self.evaluator.evaluate(article)

        # 6. 改善案
        improvement = self.improver.improve(article)

        # 7. 妥当性チェック
        is_valid = self.validity.check(article)

        # まとめて返す
        return {
            "category": category,
            "level": level,
            "template": template,
            "summary": summary,
            "evaluation": evaluation,
            "improvement": improvement,
            "valid": is_valid
        }

