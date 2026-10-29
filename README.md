---
※ 本 README は成果物の説明を目的としており、Python の学習成果は別紙「学習まとめ.txt」に記載している。
---

## 1. アプリ名
技術質問多層解析 AI アシスタント

---

## 2. このアプリを作った目的
本アプリは、Python による **多層 AI システム構築の理解定着**を目的とした自己研鑽の一環として開発した。

Intent 判定・特徴量抽出・推論テンプレート・教師レイヤー・LLM 連携など、  
実務レベルの AI アーキテクチャを **AI と協働しながら一部を自力で実装する**ことで、  
技術質問に体系的に回答できる仕組みを理解することを目的としている。

アプリとして以下の価値を提供する：

- 技術質問に対して体系化された回答を返す  
- 質問の意図（Intent）を自動判定し、最適な推論構造を生成する  
- 質問者のレベル（初級・中級・上級）を推定し、適切な深さで回答する  

※ 本 README は成果物の説明を目的としており、Python の学習成果は別紙「学習まとめ.txt」に記載している。

---

## 3. アプリの概要
本アプリは、ユーザが入力した技術質問を多層構造で解析し、

**Intent 判定 → 推論構造生成 → 特徴量抽出 → レベル判定 → 教師レイヤー → LLM → カード表示**

という流れで体系化された技術回答を返す。

### ● 各レイヤーの役割

**IntentDetector**
- 質問文から Intent（compare / design / steps / caution / improvement / summary）を判定  
- 「仕組み」「とは」「教えて」などは design  
- 「手順」「方法」「追加する」などは steps  
- 「比較」「vs」などは compare  

**ReasoningLayer**
- Intent に応じた推論テンプレート（比較・設計・手順など）を生成  
- 推論構造①（design）  
- 推論構造②（compare）  
- 推論構造③（procedure）  

**FeatureExtractor**
- 文構造・接続詞・因果関係・技術語彙などを抽出  

**LevelDetector**
- FeatureExtractor の特徴量と domain 情報を用いて  
  質問者のレベル（初級 / 中級 / 上級）を判定する  
- compare / design / steps など、domain ごとの特徴量を踏まえてスコアを補正し、  
  過度に初級寄りにならないように調整している  

**TeacherLayer**
- 推論テンプレートに基づき、  
  summary / differences / pros_cons / use_cases / caution / flow / architecture  
  などの構造化カードを生成  

**LLM**
- TeacherLayer が生成した構造に沿って文章を生成  

**UI**
- カード形式で回答を表示  

---

## 4. 機能
- Intent（比較・設計・手順・改善・要約）自動判定  
- 推論テンプレートに基づく体系化された回答生成  
- 特徴量抽出による質問者レベル推定（初級・中級・上級）  
- summary / list / steps / pros_cons / caution などの構造化カード生成  
- 非技術質問の自動フィルタリング  
- FastAPI によるバックエンド API  
- UI によるカード表示  

---

## 5. データ処理の流れ

### ● 入力データ
- ユーザの質問文（text）

### ● 内部データ構造（統一フォーマット）
- domain  
- intent  
- reasoning_type  
- level  
- axes  
- score  
- sections（header / content / list / steps / code）

### ● 処理フロー
1. IntentDetector が質問の意図を判定  
2. ReasoningLayer が推論構造を決定  
3. FeatureExtractor が文章特徴量を抽出  
4. LevelDetector が質問者レベルを推定  
5. TeacherLayer が回答構造（セクション）を生成  
6. LLM が最終文章を生成  
7. UI がカード形式で表示  

---

## 6. UI の流れ（スクリーンショット）

`screenshots/` に格納されているスクリーンショットは、以下の UI フローを網羅している。

### ① 初期画面
- ①初期画面（チュートリアル）.png

### ② 質問入力
- ②-1質問入力画面.png  
- ②-2コンソール画面(質問入力時）.png

### ③ Intent 判定
- ③-1Intent 判定が UI に反映されたカード①.png  
- ③-2Intent 判定が UI に反映されたカード②.png  
- ③-3Intent 判定が UI に反映されたカード③.png  
- ③-4Intent 判定が UI に反映されたカード④.png  
- ③-5Intent 判定が UI に反映されたカード⑤.png  

### ④ 推論構造（ReasoningLayer）
- 推論構造①(design).png  
- 推論構造②(compare).png  
- 推論構造③(procedure).png  

---

## 7. テストで確認した内容（UI の流れに沿った形）

### ① 初期画面
- UI が正常に起動し、チュートリアルが表示される

### ② 質問入力
- 入力欄が正常に動作する  
- FastAPI にリクエストが送信されていることを確認

### ③ Intent 判定
- IntentDetector が質問の意図を正しく分類  
- Intent カードが UI 上で複数パターン正しく表示される

### ④ 推論構造
- ReasoningLayer が domain に応じた推論構造を生成  
- design / compare / procedure の 3 種類を screenshots で確認

### ⑤ レベル判定
- LevelDetector が特徴量と domain 情報を用いて、  
  初級 / 中級 / 上級 のレベルを一貫性のある基準で判定していることを確認

### ⑥ 構造化カード生成
- TeacherLayer が summary / differences / pros_cons / use_cases / caution など、  
  domain に応じた構造化カードを生成していることをコードベースで確認

---

## 8. 使用技術
- Python  
- FastAPI  
- BeautifulSoup  
- JSON  
- JavaScript  
- HTML / CSS  
- GitHub  
- VS Code  

---

## 9. フォルダ構成

```text
/AIchat/
│
├─ README.md
├─ 学習まとめ.txt
├─ start_ai.bat
│
├─ backend/
│   ├─ api/
│   │   ├─ __init__.py
│   │   └─ main.py
│   │
│   ├─ core/
│   │   └─ classifier.py
│   │
│   ├─ data/
│   │   └─ （学習用データ・設定ファイルなど）
│   │
│   ├─ external/
│   │   ├─ external_search_engine.py
│   │   └─ （その他外部連携モジュール）
│   │
│   ├─ intent_layer/
│   │   ├─ intent_detector.py
│   │   ├─ intent_terms.json
│   │   └─ semantic_axes.json
│   │
│   ├─ ml/
│   │   ├─ feature_extractor.py
│   │   ├─ level_detector_ml.py
│   │   └─ level_detector.py
│   │
│   ├─ reasoning_layer/
│   │   └─ reasoning_layer.py
│   │
│   ├─ teacher_layer/
│   │   └─ teacher_layer.py
│   │
│   ├─ llm/
│   │   ├─ llm.py
│   │   └─ dummy_model_client.py
│   │
│   └─ utils/
│       ├─ search_query_builder.py
│       └─ self_improvement_cycle.py
│
├─ frontend/
│   ├─ index.html
│   ├─ script.js
│   └─ style.css
│
└─ screenshots/
    ├─ ①初期画面（チュートリアル）.png
    ├─ ②-1質問入力画面.png
    ├─ ②-2コンソール画面(質問入力時）.png
    ├─ ③-1Intent 判定が UI に反映されたカード①.png
    ├─ ③-2Intent 判定が UI に反映されたカード②.png
    ├─ ③-3Intent 判定が UI に反映されたカード③.png
    ├─ ③-4Intent 判定が UI に反映されたカード④.png
    ├─ ③-5Intent 判定が UI に反映されたカード⑤.png
    ├─ 推論構造①(design).png
    ├─ 推論構造②(compare).png
    └─ 推論構造③(procedure).png
```

---

## 10. 学習まとめ
別紙「学習まとめ.txt」に記載。

---

## 11. 参考文献

- FastAPI  
  [https://fastapi.tiangolo.com/](https://fastapi.tiangolo.com/)  
- scikit-learn  
  [https://scikit-learn.org/stable/](https://scikit-learn.org/stable/)  
- BeautifulSoup4  
  `https://www.crummy.com/software/BeautifulSoup/bs4/doc/` [(crummy.com in Bing)](https://www.bing.com/search?q="https%3A%2F%2Fwww.crummy.com%2Fsoftware%2FBeautifulSoup%2Fbs4%2Fdoc%2F")  
- Python 公式（例外処理）  
  `https://docs.python.org/3/tutorial/errors.html` [(docs.python.org in Bing)](https://www.bing.com/search?q="https%3A%2F%2Fdocs.python.org%2F3%2Ftutorial%2Ferrors.html")  
- OpenAI API  
  [https://platform.openai.com/docs/](https://platform.openai.com/docs/)  
- JSON 仕様  
  `https://www.json.org/json-en.html` [(json.org in Bing)](https://www.bing.com/search?q="https%3A%2F%2Fwww.json.org%2Fjson-en.html")  
- GitHub Docs  
  [https://docs.github.com/](https://docs.github.com/)  

---
