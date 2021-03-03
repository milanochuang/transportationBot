#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
    Loki 2.0 Template For Python3

    [URL] https://api.droidtown.co/Loki/BulkAPI/

    Request:
        {
            "username": "your_username",
            "input_list": ["your_input_1", "your_input_2"],
            "loki_key": "your_loki_key",
            "filter_list": ["intent_filter_list"] # optional
        }

    Response:
        {
            "status": True,
            "msg": "Success!",
            "version": "v223",
            "word_count_balance": 2000,
            "result_list": [
                {
                    "status": True,
                    "msg": "Success!",
                    "results": [
                        {
                            "intent": "intentName",
                            "pattern": "matchPattern",
                            "utterance": "matchUtterance",
                            "argument": ["arg1", "arg2", ... "argN"]
                        },
                        ...
                    ]
                },
                {
                    "status": False,
                    "msg": "No Match Intent!"
                }
            ]
        }
"""
import datetime
dt = datetime.datetime
import json
import logging
from ref_data import stationLIST
import requests
from THRS import *
import time

logging.basicConfig(level=logging.DEBUG)

try:
    from intent import Loki_departure_time
    from intent import Loki_destination_time
    from intent import Loki_destination
    from intent import Loki_departure
    from intent import Loki_Children
    from intent import Loki_Adult
except:
    from .intent import Loki_departure_time
    from .intent import Loki_destination_time
    from .intent import Loki_destination
    from .intent import Loki_departure
    from .intent import Loki_Children
    from .intent import Loki_Adult


LOKI_URL = "https://api.droidtown.co/Loki/BulkAPI/"
USERNAME = "milanochuang@gmail.com"
LOKI_KEY = ""
# 意圖過濾器說明
# INTENT_FILTER = []        => 比對全部的意圖 (預設)
# INTENT_FILTER = [intentN] => 僅比對 INTENT_FILTER 內的意圖
INTENT_FILTER = []

from ArticutAPI import ArticutAPI
articut = ArticutAPI.Articut()

class LokiResult():
    status = False
    message = ""
    version = ""
    balance = -1
    lokiResultLIST = []

    def __init__(self, inputLIST):
        self.status = False
        self.message = ""
        self.version = ""
        self.balance = -1
        self.lokiResultLIST = []

        try:
            result = requests.post(LOKI_URL, json={
                "username": USERNAME,
                "input_list": inputLIST,
                "loki_key": LOKI_KEY,
                "filter_list": INTENT_FILTER
            })

            if result.status_code == requests.codes.ok:
                result = result.json()
                self.status = result["status"]
                self.message = result["msg"]
                if result["status"]:
                    self.version = result["version"]
                    self.balance = result["word_count_balance"]
                    self.lokiResultLIST = result["result_list"]
            else:
                self.message = "Connect failed."
        except Exception as e:
            self.message = str(e)

    def getStatus(self):
        return self.status

    def getMessage(self):
        return self.message

    def getVersion(self):
        return self.version

    def getBalance(self):
        return self.balance

    def getLokiStatus(self, index):
        rst = False
        if index < len(self.lokiResultLIST):
            rst = self.lokiResultLIST[index]["status"]
        return rst

    def getLokiMessage(self, index):
        rst = ""
        if index < len(self.lokiResultLIST):
            rst = self.lokiResultLIST[index]["msg"]
        return rst

    def getLokiLen(self, index):
        rst = 0
        if index < len(self.lokiResultLIST):
            if self.lokiResultLIST[index]["status"]:
                rst = len(self.lokiResultLIST[index]["results"])
        return rst

    def getLokiResult(self, index, resultIndex):
        lokiResultDICT = None
        if resultIndex < self.getLokiLen(index):
            lokiResultDICT = self.lokiResultLIST[index]["results"][resultIndex]
        return lokiResultDICT

    def getIntent(self, index, resultIndex):
        rst = ""
        lokiResultDICT = self.getLokiResult(index, resultIndex)
        if lokiResultDICT:
            rst = lokiResultDICT["intent"]
        return rst

    def getPattern(self, index, resultIndex):
        rst = ""
        lokiResultDICT = self.getLokiResult(index, resultIndex)
        if lokiResultDICT:
            rst = lokiResultDICT["pattern"]
        return rst

    def getUtterance(self, index, resultIndex):
        rst = ""
        lokiResultDICT = self.getLokiResult(index, resultIndex)
        if lokiResultDICT:
            rst = lokiResultDICT["utterance"]
        return rst

    def getArgs(self, index, resultIndex):
        rst = []
        lokiResultDICT = self.getLokiResult(index, resultIndex)
        if lokiResultDICT:
            rst = lokiResultDICT["argument"]
        return rst

def runLoki(inputLIST):
    resultDICT = {}
    lokiRst = LokiResult(inputLIST)
    if lokiRst.getStatus():
        for index, key in enumerate(inputLIST):
            for resultIndex in range(0, lokiRst.getLokiLen(index)):
                # departure_time
                if lokiRst.getIntent(index, resultIndex) == "departure_time":
                    resultDICT = Loki_departure_time.getResult(key, lokiRst.getUtterance(index, resultIndex), lokiRst.getArgs(index, resultIndex), resultDICT)

                # destination_time
                if lokiRst.getIntent(index, resultIndex) == "destination_time":
                    resultDICT = Loki_destination_time.getResult(key, lokiRst.getUtterance(index, resultIndex), lokiRst.getArgs(index, resultIndex), resultDICT)

                # destination
                if lokiRst.getIntent(index, resultIndex) == "destination":
                    resultDICT = Loki_destination.getResult(key, lokiRst.getUtterance(index, resultIndex), lokiRst.getArgs(index, resultIndex), resultDICT)

                # departure
                if lokiRst.getIntent(index, resultIndex) == "departure":
                    resultDICT = Loki_departure.getResult(key, lokiRst.getUtterance(index, resultIndex), lokiRst.getArgs(index, resultIndex), resultDICT)

                # Children
                if lokiRst.getIntent(index, resultIndex) == "Children":
                    resultDICT = Loki_Children.getResult(key, lokiRst.getUtterance(index, resultIndex), lokiRst.getArgs(index, resultIndex), resultDICT)

                # Adult
                if lokiRst.getIntent(index, resultIndex) == "Adult":
                    resultDICT = Loki_Adult.getResult(key, lokiRst.getUtterance(index, resultIndex), lokiRst.getArgs(index, resultIndex), resultDICT)

    else:
        resultDICT = {"msg": lokiRst.getMessage()}
    return resultDICT
def amountSTRConvert(inputSTR):
    resultDICT={}
    resultDICT = articut.parse(inputSTR, level="lv3")
    return resultDICT['number']

def loadJson(filename):
    with open(filename,"r") as f:
        result = json.load(f)
    return result

def ticketTime(message):
    inputLIST = [message]
    resultDICT = runLoki(inputLIST)
    departure = resultDICT['departure']
    destination = resultDICT['destination']
    if 'departure_time' in resultDICT:
        time = resultDICT['departure_time']
    elif 'destination_time' in resultDICT:
        time = resultDICT['destination_time'] #須確認「抵達時間前的高鐵」邏輯
    else:
        time = dt.now().strftime('%H:%M')
    dtMessageTime = dt.strptime(time, "%H:%M")
    timeTable = loadJson("THRS_timetable.json")
    departureTimeList=list()
    for station in stationLIST:
        if departure == station['stationName']:
            departureSeq = station['stationSeq']
        if destination == station['stationName']:
            destinationSeq = station['stationSeq']
    print(destination)
    if departureSeq < destinationSeq: #判斷北上還是南下 若departureSeq < destinationSeq 則南下 反之則北上 （要記得處理等於的情形）
        direction = 0
        for trainSchedule in timeTable:
            if direction == trainSchedule['GeneralTimetable']['GeneralTrainInfo']['Direction']: #確認json檔內的車次是南下還是北上
                for trainStop in trainSchedule['GeneralTimetable']['StopTimes']:
                    if departure == trainStop['StationName']['Zh_tw']:
                        if 'DepartureTime' in trainStop:
                            dtDepartureTime = dt.strptime(trainStop['DepartureTime'], "%H:%M")
                            if dtDepartureTime > dtMessageTime:
                                departureTime = dt.strftime(dtDepartureTime, "%H:%M")
                                departureTimeList.append(departureTime) 
    if departureSeq > destinationSeq:
        direction = 1
        for trainSchedule in timeTable:
            if direction == trainSchedule['GeneralTimetable']['GeneralTrainInfo']['Direction']: #確認json檔內的車次是南下還是北上 
                for trainStop in trainSchedule['GeneralTimetable']['StopTimes']:
                    if departure == trainStop['StationName']['Zh_tw']:
                        if 'DepartureTime' in trainStop:
                            dtDepartureTime = dt.strptime(trainStop['DepartureTime'], "%H:%M")
                            if dtDepartureTime > dtMessageTime:
                                resultTime = dt.strftime(dtDepartureTime, "%H:%M")
                                departureTimeList.append(resultTime)                            
    departureTimeList.sort()
    print(resultDICT)
    return "以下是您指定時間可搭乘最接近的班次時間： {}".format(departureTimeList[0])
def ticketPrice(message):
    inputLIST = [message]
    resultDICT = runLoki(inputLIST)
    departure = resultDICT['departure']
    destination = resultDICT['destination']
    if 'adultAmount' in resultDICT:
        adultAmount = resultDICT['adultAmount']
    else:
        adultAmount = 0
    if 'childrenAmount' in resultDICT:
        childrenAmount = resultDICT['childrenAmount']
    else:
        childrenAmount = 0
    priceInfo = loadJson('THRS_ticketPrice.json')
    for i in priceInfo:
        if departure == i['OriginStationName']['Zh_tw'] and destination == i['DestinationStationName']['Zh_tw']:
            for fareType in i['Fares']:
                if fareType['TicketType'] == "標準":
                    adultPrice = fareType['Price']
                    childrenPrice = 0.5*adultPrice
    totalPrice = adultAmount*adultPrice + childrenAmount*childrenPrice
    return "從{}到{}總共是{}元喔".format(departure, destination, totalPrice)
def ticketPriceFree(message):
    inputLIST = [message]
    resultDICT = runLoki(inputLIST)
    departure = resultDICT['departure']
    destination = resultDICT['destination']
    if 'adultAmount' in resultDICT:
        logging.debug('adult exist')
        adultAmount = resultDICT['adultAmount']
    else:
        logging.debug('no adult')
        adultAmount = 0
    if 'childrenAmount' in resultDICT:
        logging.debug('children exist')
        childrenAmount = resultDICT['childrenAmount']
    else:
        logging.debug('no children')
        childrenAmount = 0
    priceInfo = loadJson('THRS_ticketPrice.json') #DICT
    for i in priceInfo:
        if departure == i['OriginStationName']['Zh_tw'] and destination == i['DestinationStationName']['Zh_tw']:
            for fareType in i['Fares']:
                if fareType['TicketType'] == "自由":
                    adultPrice = fareType['Price']
                    childrenPrice = 0.5*adultPrice
    totalPrice = adultAmount*adultPrice + childrenAmount*childrenPrice
    totalAmount = adultAmount + childrenAmount
    print(adultPrice, childrenPrice)
    return "從{}到{}的{}張自由座總共是{}元喔".format(departure, destination, totalAmount, totalPrice)
if __name__ == "__main__":
    inputLIST = ["我要一張五十分到台南的票"]
    resultDICT = runLoki(inputLIST)
    print(resultDICT)
    # print("Result => {}".format(resultDICT))
    # print(ticketTime('早上五點半台北到左營'))
    print(ticketPriceFree('自由座兩張 彰化到台北 一個大人一個小孩 19:00'))
    
    
