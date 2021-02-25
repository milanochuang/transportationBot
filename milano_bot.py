#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import discord
import datetime
dt = datetime.datetime
import json
from ref_data import callList
from TransportationBot import runLoki
import time

DISCORD_TOKEN=""
DISCORD_GUILD="Droidtown Linguistics Tech."
BOT_NAME = "幫你買票機器人"

# Documention
# https://discordpy.readthedocs.io/en/latest/api.html#client

client = discord.Client()

priceInfo = loadJson('THRS_ticketPrice.json') #DICT
timeTable = loadJson("THRS_timetable.json") #DICT

def amountSTRConvert(inputSTR): #將國字轉換成數字
    resultDICT={}
    resultDICT = articut.parse(inputSTR, level="lv3")
    return resultDICT['number']

def loadJson(filename):
    with open(filename,"r") as f:
        result = json.load(f)
    return result

def ticketTime(message): #
    inputLIST = [message]
    resultDICT = runLoki(inputLIST)
    departure = resultDICT['departure'] #str
    destination = resultDICT['destination'] #str
    if 'departure_time' in resultDICT:
        time = resultDICT['departure_time']
    elif 'destination_time' in resultDICT:
        time = resultDICT['destination_time'] #check if the time is correctly put in resultDICT
    else:
        time = dt.now().strftime('%H:%M')
    dtMessageTime = dt.strptime(time, "%H:%M") #datetime object
    departureTimeList=list()
    for station in stationDICT:
        if departure == station['stationName']:
            departureSeq = station['stationSeq'] #Normally departureSequence & destinationSeq will be object of integer
        if destination == station['stationName']:
            destinationSeq = station['stationSeq']
    if departureSeq < destinationSeq: 
        # check if it's going north or south. 
        # While departureSeq < destinationSeq, then it's going south.
        direction = 0
        for trainSchedule in timeTable:
            if direction == trainSchedule['GeneralTimetable']['GeneralTrainInfo']['Direction']: # Check json
                for trainStop in trainSchedule['GeneralTimetable']['StopTimes']:
                    if departure == trainStop['StationName']['Zh_tw']:
                        if 'DepartureTime' in trainStop:
                            dtDepartureTime = dt.strptime(trainStop['DepartureTime'], "%H:%M")
                            if dtDepartureTime > dtMessageTime:
                                departureTime = dt.strftime(dtDepartureTime, "%H:%M")
                                departureTimeList.append(departureTime) 
    if departureSeq > destinationSeq:
        # While departureSeq < destinationSeq, then it's going south.
        direction = 1
        for trainSchedule in timeTable:
            if direction == trainSchedule['GeneralTimetable']['GeneralTrainInfo']['Direction']: #check json
                for trainStop in trainSchedule['GeneralTimetable']['StopTimes']:
                    if departure == trainStop['StationName']['Zh_tw']:
                        if 'DepartureTime' in trainStop:
                            dtDepartureTime = dt.strptime(trainStop['DepartureTime'], "%H:%M")
                            if dtDepartureTime > dtMessageTime:
                                resultTime = dt.strftime(dtDepartureTime, "%H:%M")
                                departureTimeList.append(resultTime)                            
    departureTimeList.sort()
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
    for i in priceInfo:
        if departure == i['OriginStationName']['Zh_tw'] and destination == i['DestinationStationName']['Zh_tw']:
            for fareType in i['Fares']:
                if fareType['TicketType'] == "標準":
                    adultPrice = fareType['Price']
                    childrenPrice = 0.5*adultPrice
    totalPrice = adultAmount*adultPrice + childrenAmount*childrenPrice
    totalAmount = adultAmount + childrenAmount
    return "從{}到{}的{}張標準座位總共是{}元喔".format(departure, destination, totalAmount, totalPrice)

def ticketPriceBusiness(message):
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
    for i in priceInfo:
        if departure == i['OriginStationName']['Zh_tw'] and destination == i['DestinationStationName']['Zh_tw']:
            for fareType in i['Fares']:
                if fareType['TicketType'] == "商務":
                    adultPrice = fareType['Price']
                    childrenPrice = 0.5*adultPrice
    totalPrice = adultAmount*adultPrice + childrenAmount*childrenPrice
    totalAmount = adultAmount + childrenAmount
    return "從{}到{}的{}張商務艙總共是{}元喔".format(departure, destination, totalAmount, totalPrice)

def ticketPriceFree(message):
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
    for i in priceInfo:
        if departure == i['OriginStationName']['Zh_tw'] and destination == i['DestinationStationName']['Zh_tw']:
            for fareType in i['Fares']:
                if fareType['TicketType'] == "自由":
                    adultPrice = fareType['Price']
                    childrenPrice = 0.5*adultPrice
    totalPrice = adultAmount*adultPrice + childrenAmount*childrenPrice
    totalAmount = adultAmount + childrenAmount
    return "從{}到{}的{}張自由座總共是{}元喔".format(departure, destination, totalAmount, totalPrice)

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
        if message.content in callList:
            response = "<@!{}>".format(message.author.id) + "若想「查詢票價」，請告訴我您要從哪裡到哪裡，共有幾個大人幾個小孩?\n若您有特殊需求，請在輸入時註明「商務」或「自由」，謝謝。\n若想「查詢班次」，請告訴我您什麼時候要從哪裡出發到哪裡?"
            await message.channel.send(response)
            return
        if '謝謝' in message.content:
            response = "<@!{}>".format(message.author.id) + "期待下次再幫你忙喔！"
            await message.channel.send(response)
            return
        else:
            inputSTR = message.content.replace("<@!{}> ".format(client.user.id), "")
            inputLIST = [inputSTR]
            resultDICT = runLoki(inputLIST)
            if 'adultAmount' in resultDICT or 'childrenAmount' in resultDICT: #2
                if '商務' in message.content:
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
                        response = "<@!{}>".format(message.author.id) + "要記得說你從哪出發，還有要去哪裡喔！"
                        await message.channel.send(response)
                        return
                    if paxDICT[str(message.author.id)]['station']['destination'] == "":
                        response = "<@!{}>".format(message.author.id) + "要記得說你要去哪裡喔！"
                        await message.channel.send(response)
                        return
                    if paxDICT[str(message.author.id)]['adultAmount'] == 0 and paxDICT[str(message.author.id)]['childrenAmount'] == 0:
                        response = "<@!{}>".format(message.author.id) + "有幾位大人幾位小孩要記得說喔！"
                        await message.channel.send(response)
                        return
                    await message.channel.send(ticketPriceBusiness(inputSTR))
                    del paxDICT[str(message.author.id)]
                if '自由' in message.content:
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
                        response = "<@!{}>".format(message.author.id) + "要記得說你從哪出發，還有要去哪裡喔！"
                        await message.channel.send(response)
                        return
                    if paxDICT[str(message.author.id)]['station']['destination'] == "":
                        response = "<@!{}>".format(message.author.id) + "要記得說你要去哪裡喔！"
                        await message.channel.send(response)
                        return
                    if paxDICT[str(message.author.id)]['adultAmount'] == 0 and paxDICT[str(message.author.id)]['childrenAmount'] == 0:
                        response = "<@!{}>".format(message.author.id) + "有幾位大人幾位小孩要記得說喔！"
                        await message.channel.send(response)
                        return
                    await message.channel.send(ticketPriceFree(inputSTR))
                    del paxDICT[str(message.author.id)]
                else:
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
                        response = "<@!{}>".format(message.author.id) + "要記得說你從哪出發，還有要去哪裡喔！"
                        await message.channel.send(response)
                        return
                    if paxDICT[str(message.author.id)]['station']['destination'] == "":
                        response = "<@!{}>".format(message.author.id) + "要記得說你要去哪裡喔！"
                        await message.channel.send(response)
                        return
                    if paxDICT[str(message.author.id)]['adultAmount'] == 0 and paxDICT[str(message.author.id)]['childrenAmount'] == 0:
                        response = "<@!{}>".format(message.author.id) + "有幾位大人幾位小孩要記得說喔！"
                        await message.channel.send(response)
                        return
                    await message.channel.send(ticketPrice(inputSTR))
                    del paxDICT[str(message.author.id)]
            elif 'departure_time' in resultDICT #1
                if str(message.author.id) not in paxDICT:
                    paxDICT[str(message.author.id)] = {"departure_time": "", "station": {"departure": "", "destination": ""}}
                if 'departure_time' in resultDICT:
                    paxDICT[str(message.author.id)]['departure_time'] = resultDICT['departure_time']
                if 'departure' in resultDICT:
                    paxDICT[str(message.author.id)]['station']['departure'] = resultDICT['departure']
                if 'destination' in resultDICT:
                    paxDICT[str(message.author.id)]['station']['destination'] = resultDICT['destination']
                if paxDICT[str(message.author.id)]['departure_time'] == "":
                    response = "<@!{}>".format(message.author.id) + "要記得加入你的出發時間喔！"
                    await message.channel.send(response)
                    return
                if paxDICT[str(message.author.id)]['station']['departure'] == "":
                    response = "<@!{}>".format(message.author.id) + "要記得說你從哪出發，還有要去哪裡喔！"
                    await message.channel.send(response)
                    return
                if paxDICT[str(message.author.id)]['station']['destination'] == "":
                    response = "<@!{}>".format(message.author.id) + "要記得說你要去哪裡喔！"
                    await message.channel.send(response)
                    return
                await message.channel.send(ticketTimeStandard(inputSTR))
                del paxDICT[str(message.author.id)]
            else:
                response = "你在說什麼我幫不到你喔！"
                await message.,channel.send(response)
    elif "bot 點名" in message.content:
        response = "有！"
        await message.channel.send(response)
client.run(DISCORD_TOKEN)