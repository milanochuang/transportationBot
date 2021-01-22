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
        time = amountSTRConvert(args[0]+args[1])["time"]
        resultDICT['hour'] = time[0][0]["time_span"]["hour"][0]
        resultDICT['minute'] = time[0][0]["time_span"]["minute"][0]
        pass

    if utterance == "我要[一張][9]:[30][以前]到台南的票":
        # write your code here
        resultDICT['hour'] = args[1]
        resultDICT['minute'] = args[0]
        pass

    return resultDICT