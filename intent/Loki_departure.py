#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
    Loki module for departure
    
    Input:
        inputSTR      str,
        utterance     str,
        args          str[],
        resultDICT    dict
    
    Output:
        resultDICT    dict
"""

DEBUG_departure = True
userDefinedDICT = {"大": ["大人", "成人"], "小": ["小孩", "孩童"]}
from datetime import datetime
dt = datetime.now()

# 將符合句型的參數列表印出。這是 debug 或是開發用的。
def debugInfo(inputSTR, utterance):
    if DEBUG_departure:
        print("[departure] {} ===> {}".format(inputSTR, utterance))

def getResult(inputSTR, utterance, args, resultDICT):
    debugInfo(inputSTR, utterance)
    if utterance == "[一張]從[台北]往台南的票":
        # write your code here
        resultDICT['departure'] = args[1]
        pass

    if utterance == "我要從[台北]到台南的票[一張]":
        # write your code here
        resultDICT['departure'] = args[0]
        pass

    if utterance == "給我[一張]從[台北]到台南的票":
        # write your code here
        resultDICT['departure'] = args[1]
        pass

    if utterance == "7:46[台北]到台南的票[一張]":
        # write your code here
        resultDICT['departure'] = args[0]
        pass

    if utterance == "[七點][四十六]分[台北]到台南的票[一張]":
        # write your code here
        resultDICT['departure'] = args[2]
        pass
    
    if utterance == "[新竹]往台北":
        # write your code here
        resultDICT['departure'] = args[0]
        resultDICT['departure_time'] = dt.strftime('%H:%M')
        pass
    if utterance == "[新竹]到台北":
        resultDICT['departure'] = args[0]
        pass
    if utterance == "從[台北]":
        resultDICT['departure'] = args[0]
        pass
    return resultDICT