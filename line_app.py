#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
$ pip3 install flask
"""

from flask import Flask
from flask import request
from flask import jsonify
from line_sdk import Linebot
from TransportationBot import ticketTime
from intent import Loki_departure_time
from intent import Loki_destination_time
from intent import Loki_destination
from intent import Loki_departure
from intent import Loki_Children
from intent import Loki_Adult
LINE_ACCESS_TOKEN   = "B75494DO0qrlKXCfNrGZwbw1PcTdF4AB9Y7J7qHhajML3G+KGZ6RS5D2MrvomkqqBecqbzGV2b8SHkZ+q1ACLdqwuiDfH083Drm0xBJ+JAzpqPp5ybC1lRFhNeryfRp7szU79BjZV0DNLOPoI0Dh6wdB04t89/1O/w1cDnyilFU="
LINE_CHANNEL_SECRET = "a4a04fd9bddfdf479b24ac4a5f07e998"

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
                        print(dataDICT["type"])
                        linebot.respText(dataDICT["replyToken"], ticketTime([dataDICT["message"]]))                        
        return jsonify({"status": True, "msg": "Line Webhook Success."})

    # OTHER
    else:
        return jsonify({"status": False, "msg": "HTTP_405_METHOD_NOT_ALLOWED"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8003)
