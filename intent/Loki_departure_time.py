#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
    Loki module for departure_time

    Input:
        inputSTR      str,
        utterance     str,
        args          str[],
        resultDICT    dict

    Output:
        resultDICT    dict
"""

DEBUG_departure_time = True
userDefinedDICT = {"大": ["大人", "成人"], "小": ["小孩", "孩童"]}

from ArticutAPI import ArticutAPI
articut = ArticutAPI.Articut()
from datetime import datetime
dt = datetime.now()

def amountSTRConvert(inputSTR):
    resultDICT={}
    resultDICT = articut.parse(inputSTR, level="lv3")
    return resultDICT

def numberSTRConvert(inputSTR):
    resultDICT={}
    resultDICT = articut.parse(inputSTR, level="lv3")
    return resultDICT['number']

# 將符合句型的參數列表印出。這是 debug 或是開發用的。
def debugInfo(inputSTR, utterance):
    if DEBUG_departure_time:
        print("[departure_time] {} ===> {}".format(inputSTR, utterance))

def getResult(inputSTR, utterance, args, resultDICT):
    debugInfo(inputSTR, utterance)
    if utterance == "[7]:[46]台北到台南的票[一張]":
        # write your code here
        # resultDICT['hour'] = args[0]
        # resultDICT['minute'] = args[1]
        resultDICT['adultAmount'] = numberSTRConvert(args[2][0])[args[2][0]]
        resultDICT['date'] = dt.strftime('%Y-%m-%d')
        resultDICT['time'] = args[0]+":"+args[1]
        pass

    if utterance == "[9]:[30]出發的票[一張]":
        # write your code here
        # resultDICT['hour'] = args[0]
        # resultDICT['minute'] = args[1]
        # resultDICT['ticketAmount'] = args[2][0]
        resultDICT['date'] = dt.strftime('%Y-%m-%d')
        resultDICT['time'] = args[0]+":"+args[1]
        resultDICT['destination'] = "左營"
        pass

    if utterance == "[七點][四十六]分台北到台南的票[一張]":
        # write your code here
        datetime = amountSTRConvert(args[0]+args[1])["time"]
        # resultDICT['hour'] = time[0][0]["time_span"]["hour"][0]
        # resultDICT['minute'] = time[0][0]["time_span"]["minute"][0]
        resultDICT['ticketAmount'] = args[2][0]
        resultDICT['date'] = datetime[0][0]["datetime"][0:10] #抓articutAPI中time的日期（前十格）
        resultDICT['time'] = datetime[0][0]["datetime"][-8:-3] #抓articutAPI中time的時間（後八格）
        pass

    if utterance == "[九點][半]出發的票":
        # write your code here
        # time = amountSTRConvert(args[0]+args[1])["time"]
        # resultDICT['hour'] = time[0][0]["time_span"]["hour"][0]
        # resultDICT['minute'] = time[0][0]["time_span"]["minute"][0]
        resultDICT['ticketAmount'] = 1
        datetime = amountSTRConvert(args[0]+args[1])["time"]
        resultDICT['datetime'] = datetime[0][0]["datetime"]
        resultDICT['date'] = datetime[0][0]["datetime"][0:10]
        resultDICT['time'] = datetime[0][0]["datetime"][-8:-3]
        resultDICT['destination'] = "左營"
        pass

    if utterance == "我要[一張][7]:[46]到台南的票":
        # write your code here
        resultDICT['date'] = dt.strftime('%Y-%m-%d')
        resultDICT['time'] = args[1]+":"+args[2]
        #resultDICT['ticketAmount'] = amountSTRConvert(args[0][0])
        resultDICT['departure'] = "台北"
        pass

    if utterance == "我要[一張][9]:[30]出發的票":
        # write your code here
        resultDICT['date'] = dt.strftime('%Y-%m-%d')
        resultDICT['time'] = args[1]+":"+args[2]
        # resultDICT['ticketAmount'] = args[0][0]
        resultDICT['destination'] = "左營"
        pass

    if utterance == "我要[一張][七點][四十六]分到台南的票":
        # write your code here
        datetime = amountSTRConvert(args[1]+args[2])["time"]
        resultDICT['hour'] = datetime[0][0]["time_span"]["hour"][0]
        resultDICT['minute'] = datetime[0][0]["time_span"]["minute"][0]
        resultDICT['date'] = datetime[0][0]["datetime"][0:10]
        resultDICT['time'] = datetime[0][0]["datetime"][-8:-3]
        resultDICT['ticketAmount'] = args[0][0]
        resultDICT['departure'] = "台北"
        pass

    if utterance == "我要[一張][九點][半]出發的票":
        # write your code here
        datetime = amountSTRConvert(args[1]+args[2])["time"]
        resultDICT['hour'] = datetime[0][0]["time_span"]["hour"][0]
        resultDICT['minute'] = datetime[0][0]["time_span"]["minute"][0]
        resultDICT['date'] = datetime[0][0]["datetime"][0:10]
        resultDICT['time'] = datetime[0][0]["datetime"][-8:-3]
        resultDICT['ticketAmount'] = args[0][0]
        resultDICT['destination'] = "左營"
        resultDICT['departure'] = "台北"
        pass
    if utterance == "[三十分]出發的高鐵":   #利用判斷是確認時分
        hour = dt.strftime("%H")
        minute = numberSTRConvert(args[0][0:2])[args[0][0:2]]
        resultDICT['time'] = "{}:{}".format(hour, minute)
        resultDICT['date'] = dt.strftime('%Y-%m-%d')
        resultDICT['destination'] = "左營"
        pass
    if utterance == "[八點左右]":
        datetime = amountSTRConvert(args[0][0:2])["time"]
        resultDICT['time'] = datetime[0][0]["datetime"][-8:-3]
        pass
    return resultDICT