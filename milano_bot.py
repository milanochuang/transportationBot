#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import discord
from TransportationBot import runLoki
import time
import datetime
import json
dt = datetime.datetime

DISCORD_TOKEN=""
DISCORD_GUILD="Droidtown Linguistics Tech."
BOT_NAME = "幫你買票機器人"

# Documention
# https://discordpy.readthedocs.io/en/latest/api.html#client

client = discord.Client()



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

@client.event
async def on_ready():
    for guild in client.guilds:
        if guild.name == DISCORD_GUILD:
            break
    print(f'{BOT_NAME}bot has connected to Discord!')
    print(f'{guild.name}(id:{guild.id})')

    members = '\n - '.join([member.name for member in guild.members])
    print(f'Guild Members:\n - {members}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    print("message.content", message.content)
    if "<@!{}>".format(client.user.id) in message.content:
        paxDICT = {}
        if '出來' in message.content:
            response = "請輸入代碼選擇服務項目(1:查詢時間/2:查詢票價)"
            await message.channel.send(response)
            return
        if '謝謝' in message.content:
            response = "期待下次再幫你忙喔！"
            await message.channel.send(response)
            return
        else:
            if "1" in message.content:
                await message.channel.send("請告訴我您什麼時候要從哪裡出發到哪裡呢？")
                return
            if "2" in message.content:
                await message.channel.send("請告訴我您要從哪裡到哪裡，共有幾個大人幾個小孩呢？")
                return
            else:
                inputSTR = message.content.replace("<@!{}> ".format(client.user.id), "")
                inputLIST = [inputSTR]
                resultDICT = runLoki(inputLIST)
                if 'adultAmount' in resultDICT or 'childrenAmount' in resultDICT: #2
                    if str(message.author.id) not in paxDICT:
                        paxDICT[str(message.author.id)] = {"station": {"departure": "", "destination": ""}, "adultAmount": 0, "childrenAmount": 0}
                    if 'departure' in resultDICT:
                        paxDICT[str(message.author.id)]['station']['departure'] = resultDICT['departure']
                    if 'destination' in resultDICT:
                        paxDICT[str(message.author.id)]['station']['destination'] = resultDICT['destination']
                    if 'adultAmount' in resultDICT:
                        paxDICT[str(message.author.id)]['adultAmount'] = resultDICT['adultAmount']
                    if 'childrenAmount' in resultDICT:
                        paxDICT[str(message.author.id)]['childrenAmount'] = resultDICT['childrenAmount']
                    if paxDICT[str(message.author.id)]['station']['departure'] == "":
                        await message.channel.send("要記得說你從哪出發，還有要去哪裡喔！")
                        return
                    if paxDICT[str(message.author.id)]['station']['destination'] == "":
                        await message.channel.send("要記得說你要去哪裡喔！")
                        return
                    if paxDICT[str(message.author.id)]['adultAmount'] == 0 and paxDICT[str(message.author.id)]['childrenAmount'] == 0:
                        await message.channel.send("有幾位大人幾位小孩要記得說喔！")
                        return
                    await message.channel.send(ticketPrice(inputSTR))
                    del paxDICT[str(message.author.id)]
                else: #1
                    print(resultDICT)
                    if str(message.author.id) not in paxDICT:
                        paxDICT[str(message.author.id)] = {"departure_time": "", "station": {"departure": "", "destination": ""}}
                    if 'departure_time' in resultDICT:
                        paxDICT[str(message.author.id)]['departure_time'] = resultDICT['departure_time']
                    if 'departure' in resultDICT:
                        paxDICT[str(message.author.id)]['station']['departure'] = resultDICT['departure']
                    if 'destination' in resultDICT:
                        paxDICT[str(message.author.id)]['station']['destination'] = resultDICT['destination']
                    if paxDICT[str(message.author.id)]['departure_time'] == "":
                        await message.channel.send("要記得加入你的出發時間喔！")
                        return
                    if paxDICT[str(message.author.id)]['station']['departure'] == "":
                        await message.channel.send("要記得說你從哪出發，還有要去哪裡喔！")
                        return
                    if paxDICT[str(message.author.id)]['station']['destination'] == "":
                        await message.channel.send("要記得說你要去哪裡喔！")
                        return
                    await message.channel.send(ticketTime(inputSTR))
                    del paxDICT[str(message.author.id)]
    elif "bot 點名" in message.content:
        response = "有！"
        await message.channel.send(response)
client.run(DISCORD_TOKEN)