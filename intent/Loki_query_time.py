#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
    Loki module for query_time

    Input:
        inputSTR      str,
        utterance     str,
        args          str[],
        resultDICT    dict

    Output:
        resultDICT    dict
"""
from datetime import datetime
dt = datetime.now()
import dateparser
DEBUG_query_time = True
userDefinedDICT = {"大": ["大人", "成人"], "小": ["小孩", "孩童"]}

# 將符合句型的參數列表印出。這是 debug 或是開發用的。
def debugInfo(inputSTR, utterance):
    if DEBUG_query_time:
        print("[query_time] {} ===> {}".format(inputSTR, utterance))

def time_check(hour, minute):
    if hour < 24 and hour > 1:
        if minute < 60 and minute >=0:
            return True
    else:
        return False

def format_identifier(time_STR):
    if dt.strftime("%p") == "PM":
        time_STR = time_STR + "PM"
        dt1 = dateparser.parse(time_STR)
        time_STR = datetime.strftime(dt1, '%H:%M')
        return time_STR
    else:
        return time_STR   

def getResult(inputSTR, utterance, args, resultDICT):
    debugInfo(inputSTR, utterance)
    if utterance == "[19]:[47]":
        # write your code here
        hour = int(args[0])
        if args[1][0] != "0":
            minute = int(args[1])
        else:
            minute = int(args[1][-1])
        if time_check(hour, minute):
            dt = args[0] + ":" + args[1]
            resultDICT ['departure_time'] = format_identifier(dt)
        pass

    return resultDICT