# router/api_router.py
#============================================
# ユーザ入力から“どのAPIカテゴリを使うべきか”を決めて、
# 対応するAPI辞書を返す層
#============================================

class APIRouter:
    def __init__(self):

        # ① カテゴリ → キーワードリスト
        self.api_keywords = {
            "weather": ["天気", "気温", "weather", "forecast"],
            "translate": ["翻訳", "translate", "英語にして", "日本語にして"],
            "stock": ["株", "株価", "stock", "market"],
            "image": ["画像", "image", "resize", "filter"],
            "database": ["DB", "database", "SQL", "query"],
            "auth": ["認証", "login", "token", "auth"],
            "ml": ["機械学習", "ML", "model", "predict"],
            "file": ["ファイル", "file", "read", "write"],
            "network": ["通信", "network", "request", "http"],
            "math": ["数学", "math", "calc", "compute"]
        }

        # ② カテゴリ → API辞書（技術情報）
        self.api_db = {
            "weather": {
                "api": {
                    "name": "getWeather",
                    "params": ["city", "unit"],
                    "exceptions": ["TimeoutError", "ValueError"]
                },
                "usage": {
                    "examples": ["getWeather('Tokyo', 'C')"]
                },
                "notes": {
                    "important": ["APIキーが必要", "レスポンスはJSON"],
                    "performance": ["キャッシュ推奨"]
                }
            },

            "translate": {
                "api": {
                    "name": "translateText",
                    "params": ["text", "target_lang"],
                    "exceptions": ["AuthError", "RateLimitError"]
                },
                "usage": {
                    "examples": ["translateText('こんにちは', 'en')"]
                },
                "notes": {
                    "important": ["文字数制限あり"],
                    "performance": ["短文は高速"]
                }
            },

            # …他のカテゴリも同じ構造で続く…
        }

    # カテゴリ選択ロジック
    def match_api(self, user_input):

        for category, keywords in self.api_keywords.items():
            for kw in keywords:
                if kw in user_input:
                    return self.api_db.get(category)
        return None
            
           