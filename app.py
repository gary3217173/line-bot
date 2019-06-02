# flask, django


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

line_bot_api = LineBotApi('o79Ha/JJoiDZdNs8k7qfACw9yiNGhBour9l8UN2bmTxfQSRhHSpJ6ML+/Gd9s9Da2OXHiZZ97RBtp9sI3kDzCTdJKauJGCG+YQpaiJpKcB7/R9bsqeC5xTf/cOFTuyUS6QIwmbEx6yD2f6Sy++e/pwdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('993f865d3e8ceada4719d844c654cbd8')


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
    msg = event.message.text
    r = '很抱歉, 我不知道你在說甚麼'
    
    if msg == 'hi':
        r = 'hi'
    elif msg == '你吃飯了嗎':
        r = '還沒'

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=r))


if __name__ == "__main__":
    app.run()