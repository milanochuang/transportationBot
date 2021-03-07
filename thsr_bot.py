#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import discord
import datetime
dt = datetime.datetime
import json
import logging
from ref_data import stationLIST, animalLIST, TaiwanLIST, AroundLIST
from TransportationBot import runLoki, ticketTime, ticketTimeAround, ticketPrice, ticketPriceBusiness, ticketPriceFree
import time

logging.basicConfig(level=logging.DEBUG)

DISCORD_TOKEN=""
DISCORD_GUILD="Droidtown Linguistics Tech."
BOT_NAME = "幫你買票機器人"

# Documention
# https://discordpy.readthedocs.io/en/latest/api.html#client

client = discord.Client()

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
            if set(animalLIST).intersection(set(inputSTR)):
                response = "<@!{}>".format(message.author.id) + "原則上高鐵不允許帶攜帶動物進入，但如果您要攜帶寵物上高鐵的話，請您要確認高鐵公司已同意其為不妨害公共安全的動物，且完固包裝於長、寬、高尺寸小於 55 公分、45公分、38公分之容器內，無糞便、液體漏出之虞。"
                await message.channel.send(response)
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
                    if paxDICT[str(message.author.id)]['station']['departure'] == "高雄" or paxDICT[str(message.author.id)]['station']['destination'] == "高雄":
                        response = "<@!{}>".format(message.author.id) + "高鐵沒有高雄站只有左營站喔"
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
                    if paxDICT[str(message.author.id)]['adultAmount'] == 0 and paxDICT[str(message.author.id)]['childrenAmount'] == 0:
                        response = "<@!{}>".format(message.author.id) + "有幾位大人幾位小孩要記得說喔！"
                        await message.channel.send(response)
                        return
                    if paxDICT[str(message.author.id)]['station']['departure'] == paxDICT[str(message.author.id)]['station']['destination']:
                        response = "<@!{}>".format(message.author.id) + "呃，你已經在目的地了喔！"
                        await message.channel.send(response)
                        return
                    if paxDICT[str(message.author.id)]['station']['departure'] not in TaiwanLIST or paxDICT[str(message.author.id)]['station']['destination'] not in TaiwanLIST:
                        response = "<@!{}>".format(message.author.id) + "呃，你確定你的出發地點跟抵達地點高鐵有到嗎？"
                        await message.channel.send(response)
                        return
                    print(resultDICT)
                    response = "<@!{}>".format(message.author.id) + ticketPriceFree(inputSTR)
                    await message.channel.send(response)
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
                    if paxDICT[str(message.author.id)]['station']['departure'] == "高雄" or paxDICT[str(message.author.id)]['station']['destination'] == "高雄":
                        response = "<@!{}>".format(message.author.id) + "高鐵沒有高雄站只有左營站喔"
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
                    if paxDICT[str(message.author.id)]['adultAmount'] == 0 and paxDICT[str(message.author.id)]['childrenAmount'] == 0:
                        response = "<@!{}>".format(message.author.id) + "有幾位大人幾位小孩要記得說喔！"
                        await message.channel.send(response)
                        return
                    if paxDICT[str(message.author.id)]['station']['departure'] == paxDICT[str(message.author.id)]['station']['destination']:
                        response = "<@!{}>".format(message.author.id) + "呃，你已經在目的地了喔！"
                        await message.channel.send(response)
                        return
                    if paxDICT[str(message.author.id)]['station']['departure'] not in TaiwanLIST or paxDICT[str(message.author.id)]['station']['destination'] not in TaiwanLIST:
                        response = "<@!{}>".format(message.author.id) + "呃，你確定你的出發地點跟抵達地點高鐵有到嗎？"
                        await message.channel.send(response)
                        return 
                    print(resultDICT)
                    response = "<@!{}>".format(message.author.id) + ticketPriceFree(inputSTR)                  
                    await message.channel.send(response)
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
                    if paxDICT[str(message.author.id)]['station']['departure'] == "高雄" or paxDICT[str(message.author.id)]['station']['destination'] == "高雄":
                        response = "<@!{}>".format(message.author.id) + "高鐵沒有高雄站只有左營站喔"
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
                    if paxDICT[str(message.author.id)]['adultAmount'] == 0 and paxDICT[str(message.author.id)]['childrenAmount'] == 0:
                        response = "<@!{}>".format(message.author.id) + "有幾位大人幾位小孩要記得說喔！"
                        await message.channel.send(response)
                        return
                    if paxDICT[str(message.author.id)]['station']['departure'] == paxDICT[str(message.author.id)]['station']['destination']:
                        response = "<@!{}>".format(message.author.id) + "呃，你已經在目的地了喔！"
                        await message.channel.send(response)
                        return
                    if paxDICT[str(message.author.id)]['station']['departure'] not in TaiwanLIST or paxDICT[str(message.author.id)]['station']['destination'] not in TaiwanLIST:
                        response = "<@!{}>".format(message.author.id) + "呃，你確定你的出發地點跟抵達地點高鐵有到嗎？"
                        await message.channel.send(response)
                        return
                    print(resultDICT)
                    response = "<@!{}>".format(message.author.id) + ticketPrice(inputSTR)
                    await message.channel.send(response)
                    del paxDICT[str(message.author.id)]
            elif bool([a for a in AroundLIST if a in inputSTR]): #1
                logging.debug('time checked')
                if str(message.author.id) not in paxDICT:
                    paxDICT[str(message.author.id)] = {"departure_time": "", "station": {"departure": "", "destination": ""}}
                if 'departure_time' in resultDICT:
                    paxDICT[str(message.author.id)]['departure_time'] = resultDICT['departure_time']
                if 'departure' in resultDICT:
                    paxDICT[str(message.author.id)]['station']['departure'] = resultDICT['departure']
                if 'destination' in resultDICT:
                    paxDICT[str(message.author.id)]['station']['destination'] = resultDICT['destination']
                if paxDICT[str(message.author.id)]['station']['departure'] == "高雄" or paxDICT[str(message.author.id)]['station']['destination'] == "高雄":
                    response = "<@!{}>".format(message.author.id) + "高鐵沒有高雄站只有左營站喔"
                    await message.channel.send(response)
                    return
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
                if paxDICT[str(message.author.id)]['station']['departure'] not in TaiwanLIST or paxDICT[str(message.author.id)]['station']['destination'] not in TaiwanLIST:
                    response = "<@!{}>".format(message.author.id) + "呃，你確定你的出發地點跟抵達地點高鐵有到嗎？"
                    await message.channel.send(response)
                    return
                print(resultDICT)
                response = "<@!{}>".format(message.author.id) + ticketTimeAround(inputSTR)
                await message.channel.send(response)
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
                if paxDICT[str(message.author.id)]['station']['departure'] == "高雄" or paxDICT[str(message.author.id)]['station']['destination'] == "高雄":
                    response = "<@!{}>".format(message.author.id) + "高鐵沒有高雄站只有左營站喔"
                    await message.channel.send(response)
                    return
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
                if paxDICT[str(message.author.id)]['station']['departure'] not in TaiwanLIST or paxDICT[str(message.author.id)]['station']['destination'] not in TaiwanLIST:
                    response = "<@!{}>".format(message.author.id) + "呃，你確定你的出發地點跟抵達地點高鐵有到嗎？"
                    await message.channel.send(response)
                    return
                print(resultDICT)
                response = "<@!{}>".format(message.author.id) + ticketTime(inputSTR)
                await message.channel.send(response)
                del paxDICT[str(message.author.id)]
    elif "bot 點名" in message.content:
        response = "有！"
        await message.channel.send(response)
client.run(DISCORD_TOKEN)