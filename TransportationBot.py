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
from THRS import *
import requests
import time
import datetime
import json
dt = datetime.datetime

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

stationDICT=[
            {'stationName': '南港', 'stationID': '0990', 'stationSeq': 1},
            {'stationName': '台北', 'stationID': '1000', 'stationSeq': 2},
            {'stationName': '板橋', 'stationID': '1010', 'stationSeq': 3},
            {'stationName': '桃園', 'stationID': '1020', 'stationSeq': 4},
            {'stationName': '新竹', 'stationID': '1030', 'stationSeq': 5},
            {'stationName': '苗栗', 'stationID': '1035', 'stationSeq': 6},
            {'stationName': '台中', 'stationID': '1040', 'stationSeq': 7},
            {'stationName': '彰化', 'stationID': '1043', 'stationSeq': 8},
            {'stationName': '雲林', 'stationID': '1047', 'stationSeq': 9},
            {'stationName': '嘉義', 'stationID': '1050', 'stationSeq': 10},
            {'stationName': '台南', 'stationID': '1060', 'stationSeq': 11},
            {'stationName': '左營', 'stationID': '1070', 'stationSeq': 12},
            ]

def loadJson(filename):
    with open(filename,"r") as f:
        result = json.load(f)
    return result

def varExist(var):
    try:
        var
    except NameError:
        var = False
        print("你打的站名可能不存在喔！")
    else:
        var = True

def ticketTime(message):
    inputLIST = [message]
    resultDICT = runLoki(inputLIST)
    departure = resultDICT['departure']
    destination = resultDICT['destination']
    time = resultDICT['time']
    dtMessageTime = dt.strptime(time, "%H:%M")
    destination = resultDICT['destination']
    timeTable = loadJson("THRS_timetable.json")
    departureTimeList=list()
    arrivalTimeList=list()
    for station in stationDICT:
        if departure == station['stationName']:
            departureSeq = station['stationSeq']
        if destination == station['stationName']:
            destinationSeq = station['stationSeq']
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
                        # if destination == trainStop['StationName']['Zh_tw']:
                        #     if 'ArrivalTime' in trainStop:
                        #         dtArrivalTime = dt.strptime(trainStop['ArrivalTime'], "%H:%M")
                        #         if dtArrivalTime > dtDepartureTime:
                        #             arrivalTime = dt.strftime(dtArrivalTime, "%H:%M")
                        #             arrivalTimeList.append(arrivalTime)
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
    arrivalTimeList.sort()
    return "以下是您指定時間可搭乘最接近的班次時間： {}".format(departureTimeList[0])

        # if ('adultAmount' in resultDICT or 'childAmount' in resultDICT):
        #     departure = resultDICT['departure']
        #     destination = resultDICT['destination']
        #     priceList = loadJson('THRS_ticketPrice.json')
        #     for price in priceList:
        #         if(departure == price['OriginStationName']['Zh_tw'] and destination == price['DestinationStationName']['Zh_tw']):
        #             if('adultAmount' in resultDICT):
        #                 adultAmount = int(resultDICT['adultAmount'])
        #                 adultPrice = price['Fares'][3]['Price']
        #             else:
        #                 adultPrice = 0
        #             if('childrenAmount' in resultDICT):
        #                 childrenAmount = int(resultDICT['childrenAmount'])
        #                 childrenPrice = 0.5*price['Fares'][2]['Price']
        #             else:
        #                 childrenPrice = 0
        #             totalPrice = adultPrice*adultAmount + childrenPrice*childrenAmount
        #     return "您所搭的高鐵票價是：{}，最近的班次時間是 {}".format(totalPrice, response[0])

def ticketPrice(message):
    # curl = "curl"
    # if CURL_PATH != "":
    #     curl = CURL_PATH
    inputLIST = [message]
    resultDICT = runLoki(inputLIST)
    adultAmount = int(resultDICT['adultAmount'])
    childrenAmount = int(resultDICT['childrenAmount'])
    totalPrice = 1490*adultAmount + 745*childrenAmount
    return "從台北到左營的票價為{}元".format(totalPrice)

if __name__ == "__main__":
    # inputLIST = ["七點四十六分台北到台南的票一張"]
    # resultDICT = runLoki(inputLIST)
    # time = amountSTRConvert(resultDICT['time'])
    # print(time)
    # print("Result => {}".format(resultDICT))
    # result = getTrainStationStartEnd(curl, "0990", "1070", "2021-01-01")
    # print(result)
    print(ticketTime('18:14桃園到台南的票一張 '))
    # print(ticketPrice('五大三小'))
    
