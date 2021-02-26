#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
    Loki module for destination
    
    Input:
        inputSTR      str,
        utterance     str,
        args          str[],
        resultDICT    dict
    
    Output:
        resultDICT    dict
"""

DEBUG_destination = True
userDefinedDICT = {"大": ["大人", "成人"], "小": ["小孩", "孩童"]}

# 將符合句型的參數列表印出。這是 debug 或是開發用的。
def debugInfo(inputSTR, utterance):
    if DEBUG_destination:
        print("[destination] {} ===> {}".format(inputSTR, utterance))

def getResult(inputSTR, utterance, args, resultDICT):
    debugInfo(inputSTR, utterance)
    if utterance == "7:46台北到[台南]的票[一張]":
        # write your code here
        resultDICT['destination'] = args[0]
        pass

    if utterance == "[七點][四十六]分台北到[台南]的票[一張]":
        # write your code here
        resultDICT['destination'] = args[2]
        pass

    if utterance == "到[台北]":
        # write your code here
        resultDICT['destination'] = args[0]
        pass

    if utterance == "到[台北]的票[一張]":
        # write your code here
        resultDICT['destination'] = args[0]
        pass

    if utterance == "往[台北]":
        # write your code here
        resultDICT['destination'] = args[0]
        pass

    if utterance == "我要[一張]到[台北]的票":
        # write your code here
        resultDICT['destination'] = args[1]
        pass

    if utterance == "我要到[台北]":
        # write your code here
        resultDICT['destination'] = args[0]
        pass

    if utterance == "我要去[台北車站]":
        # write your code here
        if "去{}".format(args[0]) in inputSTR:
            resultDICT['destination'] = args[0]
        pass

    if utterance == "我要買從台北到[台南]的車票":
        # write your code here
        resultDICT['destination'] = args[0]
        pass
    if utterance == "去[台北]":
        if "去{}".format(args[0]) in inputSTR:
            resultDICT['destination'] = args[0]
        pass
    return resultDICT