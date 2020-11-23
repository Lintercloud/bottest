# -*- coding: utf-8 -*-
"""
Created on Mon Nov 23 16:34:23 2020

@author: Linter
"""

from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)

line_bot_api = LineBotApi('ljI+46H1q51GgVCA8FI00Uij9b4JRAvVs428aaUVXHHVpsljRfrev0QGDaQJHKaHPdZG3orIwQk12oSIGlJry/yGCrZjA6ATDrSmIjx8QnHKjFZ0W+myjoVRpuPYkQgc5Z4vyhF5vSQPEDtPVgsjhgdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('8f00d6b36a5c4a6d7870d4198b516984')


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))


if __name__ == "__main__":
    app.run()