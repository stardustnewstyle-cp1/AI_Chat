# ============================================
# source_filter.py
# 安全フィルタ（案2：正確性＋分かりやすさ両立モデル）
# ============================================

class SourceFilter:

    def __init__(self):
        # 種類ごとの信頼スコア
        self.type_score = {
            "official": 1.0,
            "spec": 1.0,
            "paper": 0.9,
            "enterprise_blog": 0.8,
            "community": 0.6,
            "personal_blog": 0.3
        }

    # -----------------------------------------
    # 著作権チェック
    # -----------------------------------------
    def check_copyright(self, meta):
        if meta.get("is_copyright_safe", True):
            return True, "OK"
        return False, "著作権NG"

    # -----------------------------------------
    # 無料チェック
    # -----------------------------------------
    def check_free(self, meta):
        if meta.get("is_free", True):
            return True, "OK"
        return False, "有料記事のため除外"

    # -----------------------------------------
    # 信頼性チェック（情報源タイプ）
    # -----------------------------------------
    def check_reliability(self, meta):
        t = meta.get("type", "")
        score = self.type_score.get(t, 0.0)
        return score >= 0.5, f"信頼性スコア: {score}"

    # -----------------------------------------
    # 新しさチェック（5年以上前は除外）
    # -----------------------------------------
    def check_freshness(self, meta):
        year = meta.get("published_year", 2026)
        if year >= 2021:
            return True, "新しい情報"
        return False, "古い情報（5年以上前）"

    # -----------------------------------------
    # 曖昧性チェック（曖昧表現が多い記事はスコアを下げる）
    # -----------------------------------------
    def check_ambiguity(self, meta):
        if meta.get("has_ambiguity", False):
            return False, "曖昧表現が多い"
        return True, "明確な記事"

    # -----------------------------------------
    # スコアリング（0〜1）
    # -----------------------------------------
    def score_source(self, meta):
        base = self.type_score.get(meta.get("type", ""), 0.0)

        # 古い情報は減点
        if meta.get("published_year", 2026) < 2021:
            base -= 0.3

        # 曖昧なら減点
        if meta.get("has_ambiguity", False):
            base -= 0.2

        # 最低0.0、最高1.0に丸める
        base = max(0.0, min(1.0, base))
        return base

    # -----------------------------------------
    # 総合フィルタ
    # -----------------------------------------
    def filter_source(self, meta):
        # 個別チェック
        checks = [
            self.check_copyright(meta),
            self.check_free(meta),
            self.check_reliability(meta),
            self.check_freshness(meta),
            self.check_ambiguity(meta)
        ]

        # どれか1つでもNGなら除外
        for ok, reason in checks:
            if not ok:
                return {
                    "allowed": False,
                    "score": 0.0,
                    "reason": reason
                }

        # スコア計算
        score = self.score_source(meta)

        if score < 0.5:
            return {
                "allowed": False,
                "score": score,
                "reason": f"スコア不足（{score}）"
            }

        return {
            "allowed": True,
            "score": score,
            "reason": "通過"
        }
