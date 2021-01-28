#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
    Loki module for destination_time
    
    Input:
        inputSTR      str,
        utterance     str,
        args          str[],
        resultDICT    dict
    
    Output:
        resultDICT    dict
"""

DEBUG_destination_time = True
userDefinedDICT = {"大": ["大人", "成人"], "小": ["小孩", "孩童"]}
from ArticutAPI import ArticutAPI
articut = ArticutAPI.Articut()
def amountSTRConvert(inputSTR):
    resultDICT={}
    resultDICT = articut.parse(inputSTR, level="lv3")
    return resultDICT

# 將符合句型的參數列表印出。這是 debug 或是開發用的。
def debugInfo(inputSTR, utterance):
    if DEBUG_destination_time:
        print("[destination_time] {} ===> {}".format(inputSTR, utterance))

def getResult(inputSTR, utterance, args, resultDICT):
    debugInfo(inputSTR, utterance)
    if utterance == "[九點][半][以前]到台南的票":
        # write your code here
        datetime = amountSTRConvert(args[0]+args[1])["time"]
        # resultDICT['datetime'] = datetime[0][0]["datetime"]
        resultDICT['date'] = datetime[0][0]["datetime"][0:10]
        resultDICT['time'] = datetime[0][0]["datetime"][-8:-3]
        resultDICT['departure'] = "台北"
        # resultDICT['']
        pass

    if utterance == "我要[一張][9]:[30][以前]到台南的票":
        # write your code here
        resultDICT['time'] = args[1]+":"+args[2]
        resultDICT['departure'] = "台北"
        pass

    return resultDICT