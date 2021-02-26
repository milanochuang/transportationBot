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

def timeConverter(time_str):
    t = time_str + " PM"
    in_time = datetime.strptime(t, "%I:%M %p")
    out_time = datetime.strftime(in_time, "%H:%M")
    return out_time

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
        resultDICT['departure_time'] = args[0]+":"+args[1]
        pass

    if utterance == "[9]:[30]出發的票[一張]":
        # write your code here
        resultDICT['departure_time'] = args[0]+":"+args[1]
        pass

    if utterance == "[七點][四十六]分台北到台南的票[一張]":
        # write your code here
        datetime = amountSTRConvert(args[0]+args[1])["time"]
        resultDICT['departure_time'] = datetime[0][0]["datetime"][-8:-3] #抓articutAPI中time的時間（後八格）
        pass

    if utterance == "[九點][半]出發的票":
        # write your code here
        datetime = amountSTRConvert(args[0]+args[1])["time"]
        resultDICT['departure_time'] = datetime[0][0]["datetime"][-8:-3]
        pass

    if utterance == "我要[一張][7]:[46]到台南的票":
        # write your code here
        resultDICT['departure_time'] = args[1]+":"+args[2]
        pass

    if utterance == "我要[一張][9]:[30]出發的票":
        # write your code here
        resultDICT['departure_time'] = args[1]+":"+args[2]
        pass

    if utterance == "我要[一張][七點][四十六]分到台南的票":
        # write your code here
        datetime = amountSTRConvert(args[1]+args[2])["time"]
        resultDICT['departure_time'] = datetime[0][0]["datetime"][-8:-3]
        pass
    if utterance == "[五十分]到台南":
        hour = dt.strftime("%H")
        minute = numberSTRConvert(args[0][0:2])[args[0][0:2]]
        resultDICT['departure_time'] = "{}:{}".format(hour, minute)
        pass
    if utterance == "我要[一張][九點][半]出發的票":
        # write your code here
        datetime = amountSTRConvert(args[1]+args[2])["time"]
        resultDICT['departure_time'] = datetime[0][0]["datetime"][-8:-3]
        pass
    if utterance == "[三十分]出發的高鐵":   #利用判斷是確認時分
        hour = dt.strftime("%H")
        minute = numberSTRConvert(args[0][0:2])[args[0][0:2]]
        resultDICT['departure_time'] = "{}:{}".format(hour, minute)
        pass
    if utterance == "[八點][三十分]出發的高鐵":
        datetime = amountSTRConvert(args[0]+args[1])["time"]
        resultDICT['departure_time'] = datetime[0][0]["datetime"][-8:-3]
    if utterance == "[八點]出發的高鐵":
        datetime = amountSTRConvert(args[0])["time"]
        resultDICT['departure_time'] = datetime[0][0]["datetime"][-8:-3] 
        pass
    if utterance == "[五點][五十分]從台北到台中":
        datetime = amountSTRConvert(args[0]+args[1])["time"]
        resultDICT['departure_time'] = datetime[0][0]["datetime"][-8:-3]
    if utterance == "[五十分]從台北到台中":
        if len(args) == 1:  
            if args[0][-1] in "分一二三四五六七八九十":
                hour = dt.strftime("%H")
                minute = numberSTRConvert(args[0][0:2])[args[0][0:2]]
                resultDICT['departure_time'] = "{}:{}".format(hour, minute)
            else: # 只有時
                datetime = amountSTRConvert(args[0])["time"]
                resultDICT['departure_time'] = datetime[0][0]["datetime"][-8:-3]     
    if utterance == "[早上][五點][半]台北到左營":
        datetime = amountSTRConvert(args[1]+args[2])["time"]
        if args[0] == '早上':
            resultDICT['departure_time'] = datetime[0][0]["datetime"][-8:-3]
        else:
            t = datetime[0][0]["datetime"][-8:-3]
            resultDICT['departure_time'] = timeConverter(t)
    return resultDICT