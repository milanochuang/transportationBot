#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import discord
from TransportationBot import ticket, runLoki


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
        if '買票' in message.content:
            response = "還不能買票啦！我還沒那麼厲害，但或許你可以問我時刻表跟票價喔！"
            await message.channel.send(response)
        else:
            inputSTR = message.content.replace("<@!{}> ".format(clinet.user.id), "")
            inputLIST = [inputSTR]
            resultDICT = runLoki(inputLIST)
            paxDICT = {}
                    #       "ID": 
                    #           {
                    #               "time": {"departure time": "", "destination time": ""}, 
                    #               "station": {"departure": "", "destination": ""},
                    #               "adultAmount": "", 
                    #               "childrenAmount": ""
                    #           }
                    #   }
            if str(message.author.id) not in paxDICT:
                paxDICT[str(message.author.id)] = {
                    "time": ["departure_time": "", "destination_time": ""], 
                    "station": ["departure": "", "destination": ""],
                    "adultAmount": "", 
                    "childrenAmount": ""
                }
            if 'departure_time' in resultDICT:
                paxDICT[str(message.author.id)]['time']['departure_time'] = resultDICT['departure_time']
            if 'destination_time' in resultDICT:
                paxDICT[str(message.author.id)]['time']['destination_time'] = resultDICT['destination_time']
            if 'departure' in resultDICT:
                paxDICT[str(message.author.id)]['station']['departure'] = resultDICT['departure']
            if 'destination' in resultDICT:
                paxDICT[str(message.author.id)]['station']['destination'] = resultDICT['destination']
            if 'adultAmount' in resultDICT:
                paxDICT[str(message.author.id)]['adultAmount'] = resultDICT['adultAmount']
            if 'childrenAmount' in resultDICT:
                paxDICT[str(message.author.id)]['childrenDICT'] = resultDICT['childrenAmount']
            if paxDICT[str(message.author.id)]['time']['departure_time'] == "":
                await message.channel.response("你沒有打時間啊！想知道幾點以前到請打時間")
            if paxDICT[str(message.author.id)]['station']
            response = ticket(message.content)
            await message.channel.send(response)
    elif "bot 點名" in message.content:
        response = "有！"
        await message.channel.send(response)
client.run(DISCORD_TOKEN)