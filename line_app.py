#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
$ pip3 install flask
"""

import datetime
dt = datetime.datetime
from flask import Flask
from flask import request
from flask import jsonify
import json
from line_sdk import Linebot
import logging
from ref_data import stationLIST, animalLIST, TaiwanLIST, AroundLIST
import time
from TransportationBot import runLoki, ticketTime, ticketTimeAround, ticketPrice, ticketPriceBusiness, ticketPriceFree

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
                        linebot.respText(dataDICT["replyToken"], "\n若想「查詢票價」，請告訴我您要從哪裡到哪裡，共有幾個大人幾個小孩?\n（若您有特殊需求，請在輸入時註明「商務」或「自由」，謝謝。）\n若想「查詢班次」，請告訴我您什麼時候要從哪裡出發到哪裡?") #回應的內容
                        return
                    if dataDICT["message"] == '謝謝':
                        linebot.respText(dataDICT["replyToken"], "期待下次再幫你忙喔！")
                    #token是確認不要回應錯
                    #傳送在Line裡的句子是存在dataDICT["message"]裡
                    #response = message(dataDICT["message"])
                    #linebot.respText(dataDICT["replyToken"], response)
                    #message()的回應是runLoki return回來的訊息
                    else:
                        inputSTR = dataDICT["message"]
                        inputLIST = [inputSTR]
                        resultDICT = runLoki(inputLIST)
                        if set(animalLIST).intersection(set(inputSTR)):
                            linebot.respText(dataDICT["replyToken"], "原則上高鐵不允許帶攜帶動物進入，但如果您要攜帶寵物上高鐵的話，請您要確認高鐵公司已同意其為不妨害公共安全的動物，且完固包裝於長、寬、高尺寸小於 55 公分、45公分、38公分之容器內，無糞便、液體漏出之虞。")
                        if 'adultAmount' in resultDICT or 'childrenAmount' in resultDICT:
                            if '商務' in inputSTR:
                                paxDICT = {"station": {"departure": "", "destination": ""}, "adultAmount": 0, "childrenAmount": 0}
                                if 'departure' in resultDICT:
                                    paxDICT['station']['departure'] = resultDICT['departure']
                                if 'destination' in resultDICT:
                                    paxDICT['station']['destination'] = resultDICT['destination']
                                if 'adultAmount' in resultDICT:
                                    paxDICT[str(message.author.id)]['adultAmount'] = resultDICT['adultAmount']
                                if 'childrenAmount' in resultDICT:
                                    paxDICT[str(message.author.id)]['childrenAmount'] = resultDICT['childrenAmount']
                                if paxDICT[str(message.author.id)]['station']['departure'] == "高雄" or paxDICT[str(message.author.id)]['station']['destination'] == "高雄":
                                    response = "高鐵沒有高雄站只有左營站喔"
                                    linebot.respText(dataDICT["replyToken"], response)
                                    return
                                if paxDICT['station']['departure'] == "":
                                    response = "要記得說你從哪出發，還有要去哪裡喔！"
                                    linebot.respText(dataDICT["replyToken"], response)                        
                                    return
                                if paxDICT['station']['destination'] == "":
                                    response = "要記得說你要去哪裡喔！"
                                    linebot.respText(dataDICT["replyToken"], response)
                                    return
                                if paxDICT['adultAmount'] == 0 and paxDICT[str(message.author.id)]['childrenAmount'] == 0:
                                    response = "有幾位大人幾位小孩要記得說喔！"
                                    linebot.respText(dataDICT["replyToken"], response)                        
                                    return
                                if paxDICT['station']['departure'] == paxDICT[str(message.author.id)]['station']['destination']:
                                    response = "呃，你已經在目的地了喔！"
                                    linebot.respText(dataDICT["replyToken"], response)
                                    return
                                if paxDICT['station']['departure'] not in TaiwanLIST or paxDICT[['station']['destination'] not in TaiwanLIST:
                                    response = "呃，你確定你的出發地點跟抵達地點高鐵有到嗎？"
                                    linebot.respText(dataDICT["replyToken"], response)
                                    return
                                print(resultDICT)
                                linebot.respText(dataDICT["replyToken"], ticketPriceBusiness(inputSTR))
                                del paxDICT
                            elif '自由' in inputSTR:
                                paxDICT = {"station": {"departure": "", "destination": ""}, "adultAmount": 0, "childrenAmount": 0}
                                if 'departure' in resultDICT:
                                    paxDICT['station']['departure'] = resultDICT['departure']
                                if 'destination' in resultDICT:
                                    paxDICT['station']['destination'] = resultDICT['destination']
                                if 'adultAmount' in resultDICT:
                                    paxDICT[str(message.author.id)]['adultAmount'] = resultDICT['adultAmount']
                                if 'childrenAmount' in resultDICT:
                                    paxDICT[str(message.author.id)]['childrenAmount'] = resultDICT['childrenAmount']
                                if paxDICT[str(message.author.id)]['station']['departure'] == "高雄" or paxDICT[str(message.author.id)]['station']['destination'] == "高雄":
                                    response = "高鐵沒有高雄站只有左營站喔"
                                    linebot.respText(dataDICT["replyToken"], response)
                                    return
                                if paxDICT['station']['departure'] == "":
                                    response = "要記得說你從哪出發，還有要去哪裡喔！"
                                    linebot.respText(dataDICT["replyToken"], response)                        
                                    return
                                if paxDICT['station']['destination'] == "":
                                    response = "要記得說你要去哪裡喔！"
                                    linebot.respText(dataDICT["replyToken"], response)
                                    return
                                if paxDICT['adultAmount'] == 0 and paxDICT[str(message.author.id)]['childrenAmount'] == 0:
                                    response = "有幾位大人幾位小孩要記得說喔！"
                                    linebot.respText(dataDICT["replyToken"], response)                        
                                    return
                                if paxDICT['station']['departure'] == paxDICT[str(message.author.id)]['station']['destination']:
                                    response = "呃，你已經在目的地了喔！"
                                    linebot.respText(dataDICT["replyToken"], response)
                                    return
                                if paxDICT['station']['departure'] not in TaiwanLIST or paxDICT[['station']['destination'] not in TaiwanLIST:
                                    response = "呃，你確定你的出發地點跟抵達地點高鐵有到嗎？"
                                    linebot.respText(dataDICT["replyToken"], response)
                                    return
                                print(resultDICT)
                                linebot.respText(dataDICT["replyToken"], ticketPriceFree(inputSTR))
                                del paxDICT
                            else:
                                paxDICT = {"station": {"departure": "", "destination": ""}, "adultAmount": 0, "childrenAmount": 0}
                                if 'departure' in resultDICT:
                                    paxDICT['station']['departure'] = resultDICT['departure']
                                if 'destination' in resultDICT:
                                    paxDICT['station']['destination'] = resultDICT['destination']
                                if 'adultAmount' in resultDICT:
                                    paxDICT[str(message.author.id)]['adultAmount'] = resultDICT['adultAmount']
                                if 'childrenAmount' in resultDICT:
                                    paxDICT[str(message.author.id)]['childrenAmount'] = resultDICT['childrenAmount']
                                if paxDICT[str(message.author.id)]['station']['departure'] == "高雄" or paxDICT[str(message.author.id)]['station']['destination'] == "高雄":
                                    response = "高鐵沒有高雄站只有左營站喔"
                                    linebot.respText(dataDICT["replyToken"], response)
                                    return
                                if paxDICT['station']['departure'] == "":
                                    response = "要記得說你從哪出發，還有要去哪裡喔！"
                                    linebot.respText(dataDICT["replyToken"], response)                        
                                    return
                                if paxDICT['station']['destination'] == "":
                                    response = "要記得說你要去哪裡喔！"
                                    linebot.respText(dataDICT["replyToken"], response)
                                    return
                                if paxDICT['adultAmount'] == 0 and paxDICT[str(message.author.id)]['childrenAmount'] == 0:
                                    response = "有幾位大人幾位小孩要記得說喔！"
                                    linebot.respText(dataDICT["replyToken"], response)                        
                                    return
                                if paxDICT['station']['departure'] == paxDICT[str(message.author.id)]['station']['destination']:
                                    response = "呃，你已經在目的地了喔！"
                                    linebot.respText(dataDICT["replyToken"], response)
                                    return
                                if paxDICT['station']['departure'] not in TaiwanLIST or paxDICT[['station']['destination'] not in TaiwanLIST:
                                    response = "呃，你確定你的出發地點跟抵達地點高鐵有到嗎？"
                                    linebot.respText(dataDICT["replyToken"], response)
                                    return
                                print(resultDICT)
                                linebot.respText(dataDICT["replyToken"], ticketPrice(inputSTR))
                                del paxDICT
                        elif bool([a for a in AroundLIST if a in inputSTR]):
                            paxDICT = {"departure_time": "", "station": {"departure": "", "destination": ""}}
                            if 'departure' in resultDICT:
                                paxDICT['station']['departure'] = resultDICT['departure']
                            if 'destination' in resultDICT:
                                paxDICT['station']['destination'] = resultDICT['destination']
                            if 'adultAmount' in resultDICT:
                                paxDICT[str(message.author.id)]['adultAmount'] = resultDICT['adultAmount']
                            if 'childrenAmount' in resultDICT:
                                paxDICT[str(message.author.id)]['childrenAmount'] = resultDICT['childrenAmount']
                            if paxDICT[str(message.author.id)]['station']['departure'] == "高雄" or paxDICT[str(message.author.id)]['station']['destination'] == "高雄":
                                response = "高鐵沒有高雄站只有左營站喔"
                                linebot.respText(dataDICT["replyToken"], response)
                                return
                            if paxDICT['station']['departure'] == "":
                                response = "要記得說你從哪出發，還有要去哪裡喔！"
                                linebot.respText(dataDICT["replyToken"], response)                        
                                return
                            if paxDICT['station']['destination'] == "":
                                response = "要記得說你要去哪裡喔！"
                                linebot.respText(dataDICT["replyToken"], response)
                                return
                            if paxDICT['adultAmount'] == 0 and paxDICT[str(message.author.id)]['childrenAmount'] == 0:
                                response = "有幾位大人幾位小孩要記得說喔！"
                                linebot.respText(dataDICT["replyToken"], response)                        
                                return
                            if paxDICT['station']['departure'] == paxDICT[str(message.author.id)]['station']['destination']:
                                response = "呃，你已經在目的地了喔！"
                                linebot.respText(dataDICT["replyToken"], response)
                                return
                            if paxDICT['station']['departure'] not in TaiwanLIST or paxDICT[['station']['destination'] not in TaiwanLIST:
                                response = "呃，你確定你的出發地點跟抵達地點高鐵有到嗎？"
                                linebot.respText(dataDICT["replyToken"], response)
                                return
                            print(resultDICT)
                            linebot.respText(dataDICT["replyToken"], ticketTimeAround(inputSTR))
                            del paxDICT
                        else:
                            paxDICT = {"departure_time": "", "station": {"departure": "", "destination": ""}}
                            if 'departure' in resultDICT:
                                paxDICT['station']['departure'] = resultDICT['departure']
                            if 'destination' in resultDICT:
                                paxDICT['station']['destination'] = resultDICT['destination']
                            if 'adultAmount' in resultDICT:
                                paxDICT[str(message.author.id)]['adultAmount'] = resultDICT['adultAmount']
                            if 'childrenAmount' in resultDICT:
                                paxDICT[str(message.author.id)]['childrenAmount'] = resultDICT['childrenAmount']
                            if paxDICT[str(message.author.id)]['station']['departure'] == "高雄" or paxDICT[str(message.author.id)]['station']['destination'] == "高雄":
                                response = "高鐵沒有高雄站只有左營站喔"
                                linebot.respText(dataDICT["replyToken"], response)
                                return
                            if paxDICT['station']['departure'] == "":
                                response = "要記得說你從哪出發，還有要去哪裡喔！"
                                linebot.respText(dataDICT["replyToken"], response)                        
                                return
                            if paxDICT['station']['destination'] == "":
                                response = "要記得說你要去哪裡喔！"
                                linebot.respText(dataDICT["replyToken"], response)
                                return
                            if paxDICT['adultAmount'] == 0 and paxDICT[str(message.author.id)]['childrenAmount'] == 0:
                                response = "有幾位大人幾位小孩要記得說喔！"
                                linebot.respText(dataDICT["replyToken"], response)                        
                                return
                            if paxDICT['station']['departure'] == paxDICT[str(message.author.id)]['station']['destination']:
                                response = "呃，你已經在目的地了喔！"
                                linebot.respText(dataDICT["replyToken"], response)
                                return
                            if paxDICT['station']['departure'] not in TaiwanLIST or paxDICT[['station']['destination'] not in TaiwanLIST:
                                response = "呃，你確定你的出發地點跟抵達地點高鐵有到嗎？"
                                linebot.respText(dataDICT["replyToken"], response)
                                return
                            print(resultDICT)
                            linebot.respText(dataDICT["replyToken"], ticketTimeAround(inputSTR))
                            del paxDICT
        return jsonify({"status": True, "msg": "Line Webhook Success."})

    # OTHER
    else:
        return jsonify({"status": False, "msg": "HTTP_405_METHOD_NOT_ALLOWED"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8003)
