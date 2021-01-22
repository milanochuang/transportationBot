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

    return resultDICT