#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import discord
import datetime
dt = datetime.datetime
import json
import logging
from ref_data import stationLIST
from TransportationBot import runLoki
import time

logging.basicConfig(level=logging.DEBUG)

DISCORD_TOKEN="Nzg5Mzc0ODk3OTA5Mzk5NjA1.X9xIqQ.5B6tqQGE74tXRGMmxULqB-OCly0"
DISCORD_GUILD="Droidtown Linguistics Tech."
BOT_NAME = "幫你買票機器人"

# Documention
# https://discordpy.readthedocs.io/en/latest/api.html#client

client = discord.Client()

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
        logging.debug('departure time in resultDICT')
        time = resultDICT['departure_time']
    elif 'destination_time' in resultDICT:
        logging.debug('destination time in resultDICT')
        time = resultDICT['destination_time'] #check if the time is correctly put in resultDICT
    else:
        logging.debug('Take the present time')
        time = dt.now().strftime('%H:%M')
    dtMessageTime = dt.strptime(time, "%H:%M") #datetime object
    departureTimeList=list()
    timeTable = loadJson("THRS_timetable.json") #DICT
    for station in stationLIST:
        if departure == station['stationName']:
            logging.debug('Departure sequence = 0 recorded')
            departureSeq = station['stationSeq'] #Normally departureSequence & destinationSeq will be object of integer
        if destination == station['stationName']:
            logging.debug('destination sequence recorded')
            destinationSeq = station['stationSeq']
    if departureSeq < destinationSeq: 
        # check if it's going north or south. 
        # While departureSeq < destinationSeq, then it's going south.
        direction = 0
        for trainSchedule in timeTable:
            if direction == trainSchedule['GeneralTimetable']['GeneralTrainInfo']['Direction']: # Check json
                logging.debug('direction checked')
                for trainStop in trainSchedule['GeneralTimetable']['StopTimes']:
                    if departure == trainStop['StationName']['Zh_tw']:
                        logging.debug('departure name checked')
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
                logging.debug('direction = 1 checked')
                for trainStop in trainSchedule['GeneralTimetable']['StopTimes']:
                    if departure == trainStop['StationName']['Zh_tw']:
                        logging.debug('destination name checked')
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
            logging.debug('station name match')
            for fareType in i['Fares']:
                if fareType['TicketType'] == "標準":
                    logging.debug('standard detected')
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
        logging.debug('adult exist')
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
        if "出來" in message.content:
            logging.debug('initiator succeed')
            response = "<@!{}>".format(message.author.id) + "\n若想「查詢票價」，請告訴我您要從哪裡到哪裡，共有幾個大人幾個小孩?\n（若您有特殊需求，請在輸入時註明「商務」或「自由」，謝謝。）\n若想「查詢班次」，請告訴我您什麼時候要從哪裡出發到哪裡?"
            await message.channel.send(response)
            return
        if message.content == "謝謝":
            response = "<@!{}>".format(message.author.id) + "期待下次再幫你忙喔！"
            await message.channel.send(response)
            return
        else:
            inputSTR = message.content.replace("<@!{}> ".format(client.user.id), "")
            inputLIST = [inputSTR]
            resultDICT = runLoki(inputLIST)
            if 'adultAmount' in resultDICT or 'childrenAmount' in resultDICT: #2
                logging.debug('count the price')
                if '商務' in message.content:
                    logging.debug('business class')
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
                    if paxDICT[str(message.author.id)]['station']['departure'] == paxDICT[str(message.author.id)]['station']['destination']:
                        response = "<@!{}>".format(message.author.id) + "呃，你已經在目的地了喔！"
                        await message.channel.send(response)
                        return
                    print(resultDICT)
                    await message.channel.send(ticketPriceBusiness(inputSTR))
                    del paxDICT[str(message.author.id)]
                elif '自由' in message.content:
                    logging.debug('free type')
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
                    if paxDICT[str(message.author.id)]['station']['departure'] == paxDICT[str(message.author.id)]['station']['destination']:
                        response = "<@!{}>".format(message.author.id) + "呃，你已經在目的地了喔！"
                        await message.channel.send(response)
                        return
                    print(resultDICT)
                    await message.channel.send(ticketPriceFree(inputSTR))
                    del paxDICT[str(message.author.id)]
                else:
                    logging.debug('standard type')
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
                    if paxDICT[str(message.author.id)]['station']['departure'] == paxDICT[str(message.author.id)]['station']['destination']:
                        response = "<@!{}>".format(message.author.id) + "呃，你已經在目的地了喔！"
                        await message.channel.send(response)
                        return
                    print(resultDICT)
                    await message.channel.send(ticketPrice(inputSTR))
                    del paxDICT[str(message.author.id)]
            else: #1
                logging.debug('time checked')
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
                if paxDICT[str(message.author.id)]['station']['departure'] == paxDICT[str(message.author.id)]['station']['destination']:
                    response = "<@!{}>".format(message.author.id) + "呃，你已經在目的地了喔！"
                    await message.channel.send(response)
                    return
                print(resultDICT)
                await message.channel.send(ticketTime(inputSTR))
                del paxDICT[str(message.author.id)]
    elif "bot 點名" in message.content:
        response = "有！"
        await message.channel.send(response)
client.run(DISCORD_TOKEN)