# backend/external/external_search_engine.py
import httpx


class ExternalSearchEngine:
    """
    外部検索エンジン（FastAPI と整合する非同期 httpx 実装）
    SearchQueryBuilder が生成したクエリを受け取り、
    TeacherLayer が扱える list[dict] に整形して返す。
    """

    def __init__(self, api_key: str):
        self.api_key = api_key

    async def search(self, query: str):
        """
        単一クエリを検索し、構造化しやすい形式で返す。
        TeacherLayer がそのまま list として扱える。
        """
        url = "https://api.bing.microsoft.com/v7.0/search"
        headers = {"Ocp-Apim-Subscription-Key": self.api_key}
        params = {"q": query, "count": 5}

        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(url, headers=headers, params=params)
                data = response.json()

            results = []
            for item in data.get("webPages", {}).get("value", []):
                results.append({
                    "title": item.get("name", ""),
                    "summary": item.get("snippet", ""),
                    "url": item.get("url", "")
                })

            return results

        except Exception:
            return [{
                "title": "検索エラー",
                "summary": "外部検索に失敗しました",
                "url": ""
            }]
