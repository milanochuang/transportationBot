#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
$ pip3 install flask
"""

from flask import Flask
from flask import request
from flask import jsonify
from line_sdk import Linebot
from TransportationBot import ticket
LINE_ACCESS_TOKEN   = ""
LINE_CHANNEL_SECRET = ""

app = Flask(__name__)

@app.route("/Milano/", methods=["GET", "POST"])
def webhook():
    # GET
    if request.method == "GET":
        return jsonify({"status": True, "msg": "Line Webhook Success."})

    # POST
    elif request.method == "POST":
        body = request.get_data(as_text=True)
        signature = request.headers["X-Line-Signature"] #解密

        # Line
        linebot = Linebot(LINE_ACCESS_TOKEN, LINE_CHANNEL_SECRET)

        # dataLIST = [{status, type, message, userID, replyToken, timestamp}] #送上來的東西
        dataLIST = linebot.parse(body, signature)
        for dataDICT in dataLIST:
            if dataDICT["status"]:
                if dataDICT["type"] == "message": #若回應訊息類別是訊息（or sticker）
                    # Send Message // replyToken是確認聊天室
                    if dataDICT["message"] == '出來':
                        linebot.respText(dataDICT["replyToken"], "我來了") #回應的內容
                    #token是確認不要回應錯
                    #傳送在Line裡的句子是存在dataDICT["message"]裡
                    #response = message(dataDICT["message"])
                    #linebot.respText(dataDICT["replyToken"], response)
                    #message()的回應是runLoki return回來的訊息
                    else:
                        linebot.respText(dataDICT["replyToken"], ticketTime(dataDICT["message"]))
                        # linebot.respText(dataDICT["replyToken"], ticketPrice(dataDICT["message"]))         
        return jsonify({"status": True, "msg": "Line Webhook Success."})

    # OTHER
    else:
        return jsonify({"status": False, "msg": "HTTP_405_METHOD_NOT_ALLOWED"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8003)
