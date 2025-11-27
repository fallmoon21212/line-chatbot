LINEチャットボット（ビジネスメール添削）


AI の自然言語処理技術を活用し、ビジネスメールの文章を添削する LINE チャットボットです。  
ユーザーが LINE 上で文章を送信すると、文法や敬語表現を自動修正して返答します。  
短時間で適切なビジネスメールを作成することを目的として開発しました。  

主な機能
・送信された文章を AI により自動添削
・文法修正だけでなく、ビジネスメール形式へ整形
・LINE 上で結果返答

---

使用技術 / 開発環境

| 項目 | 内容 |
| 言語 | Python 3.12.5 |
| フレームワーク | Flask 3.0.3 |
| API | OpenAI 1.41.0 |
| LINE連携 | line-bot-sdk 3.11.0 |
| サーバー | ngrok |
| 環境変数管理 | python-dotenv 1.0.1 |
| プラットフォーム | LINEアプリ |

フォルダ構成
<img width="458" height="303" alt="image" src="https://github.com/user-attachments/assets/71cc3227-c2b3-4c4f-aaf5-e346807f96ce" />

※".env" や "ngrok.exe" は含まれていません。

---

実行方法（概要）

1. LINE Developers にてチャネルを作成し、以下を取得
   ・チャネルシークレット（LINE_CHANNEL_SECRET）
   ・チャネルアクセストークン（LINE_CHANNEL_ACCESS_TOKEN）

2. ".env"を作成し、以下のように設定します（APIキーなど実際の値は非公開）：

# ChatGPT のAPI key
CHATGPT_API_KEY=xxxx
# LINE公式アカウントのチャンネルシークレット
LINE_CHANNEL_SECRET=xxxx
# LINE公式アカウントのアクセストークン
LINE_CHANNEL_ACCESS_TOKEN=xxxx


3. 必要ライブラリをインストール

pip install flask python-dotenv openai line-bot-sdk

4. main.pyを起動

5. ngrok 起動

ngrok http --domain=固定ドメイン.ngrok-free.app 3000

---

動作イメージ
<img width="477" height="1005" alt="image" src="https://github.com/user-attachments/assets/a31d0eef-ea5d-4816-b55c-f83d6d9a1b86" />




