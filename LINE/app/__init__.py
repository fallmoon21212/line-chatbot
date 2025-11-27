import os
from typing import Dict

from dotenv import load_dotenv
from flask import Flask, abort, request
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

from app.gpt.client import ChatGPTClient
from app.gpt.constants import Model, Role
from app.gpt.message import Message

load_dotenv(".env", verbose=True)

app = Flask(__name__)

if not (access_token := os.environ.get("LINE_CHANNEL_ACCESS_TOKEN")):
    raise Exception("access token is not set as an environment variable")

if not (channel_secret := os.environ.get("LINE_CHANNEL_SECRET")):
    raise Exception("channel secret is not set as an environment variable")

line_bot_api = LineBotApi(access_token)
handler = WebhookHandler(channel_secret)

chatgpt_instance_map: Dict[str, ChatGPTClient] = {}

def to_polite(text: str) -> str:
    system_prompt = "以下の文章を、ビジネスメールに適した形式に修正してください。返信ではなく、送信者が書くべきビジネスメールとして修正してください。条件は以下の通りです：1.丁寧な表現にする（失礼がないように）。2.挨拶、本文、締めの形式を整える。3.「拝啓」や「敬具」などの格式ばった表現を避け、現代的で簡潔なビジネスメールにする。4.誤字や不自然な表現を修正する。5.メールの内容が明確で、相手が読みやすいように構成する。6.返答を評価・解説するコメントではなく、修正された実際のビジネスメールの文面を出力する。"
    client = ChatGPTClient(model=Model.GPT35TURBO)
    client.add_message(Message(role=Role.SYSTEM, content=system_prompt))
    client.add_message(Message(role=Role.USER, content=text))
    res = client.create()
    return res.choices[0].message.content.strip()

@app.route("/callback", methods=["POST"])
def callback() -> str:
    signature = request.headers["X-Line-Signature"]

    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return "OK"

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event: MessageEvent) -> None:
    text_message: TextMessage = event.message
    user_id: str = event.source.user_id

    # 入力テキストを敬語に変換
    polite_text = to_polite(text_message.text)

    if (gpt_client := chatgpt_instance_map.get(user_id)) is None:
        gpt_client = ChatGPTClient(model=Model.GPT35TURBO)

    gpt_client.add_message(
        message=Message(role=Role.USER, content=polite_text)
    )
    res = gpt_client.create()
    chatgpt_instance_map[user_id] = gpt_client

    res_text: str = res.choices[0].message.content

    line_bot_api.reply_message(
        event.reply_token, TextSendMessage(text=res_text.strip())
    )