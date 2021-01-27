#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import discord
from TransportationBot import ticketTime


DISCORD_TOKEN="Nzg5Mzc0ODk3OTA5Mzk5NjA1.X9xIqQ.pQULJ3-j67EVpX9aleTSAO1kB_M"
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
        if 'test' in message.content:
            response = "Send message."
            await message.channel.send(response)
        elif '我要買票' in message.content:
            response = "才不給你買票呢"
            await message.channel.send(response)
        elif "bot 點名" in message.content:
            response = "有！"
            await message.channel.send(response)
        else:
            response = ticketTime(message.content)
            await message.channel.send(response)





client.run(DISCORD_TOKEN)
