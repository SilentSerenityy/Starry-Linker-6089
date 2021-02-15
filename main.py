from __future__ import absolute_import, unicode_literals
from __future__ import division, print_function
import discord
import os
import lavalink
import B
import asyncio
import discord.utils
import random
import datetime
import time
import json
import aiohttp
import sqlite3
import pymongo
from difflib import SequenceMatcher
from discord import Webhook, AsyncWebhookAdapter
import itertools
import functools
from async_timeout import timeout
from pymongo import MongoClient
from datetime import *
from pytz import timezone
import requests
from io import BytesIO
from PIL import Image
from clear_code import clear
import DatabaseControl
import GlobalLinker
import DatabaseConfig
import ClientConfig
import urllib3
today = datetime.today()
day = today.strftime('%m/%d/%Y %H:%M:%S')
coin = ["Heads", "Tails", "Heads", "Tails", "Heads", "Tails", "Heads", "Tails","HA! The coin fell off the table! No one wins! (or loses....)"]
flip = coin[random.randint(0, 8)]
key = os.getenv('key')
wkey = os.getenv('wkey')

client = ClientConfig.client
discordprefix = "starlink+"
time_location = "America/New_York"



from discord_webhook import DiscordWebhook

@client.event
async def on_ready():
    print('Logged in as:')
    print("Username:", client.user.name + " #6089")
    print("Client ID:", client.user.id)
    print("Bot Creator: Shadi#7894")
    await client.change_presence(activity=discord.Streaming(name="starlink+help", url = 'https://www.twitch.tv/silentserenity87'))

@client.event
async def on_message(message):
  user = message.author
  time = message.created_at
  #CHANNEL LINKER COMMANDS
  if not message.author.bot: #Channel Link Message Repeater
    if not message.content.startswith(discordprefix):
      ret_str = str(user) +": "+GlobalLinker.FilterMessage(message)
      for gChan in DatabaseConfig.db.g_link_testing.find():
        if message.channel.id == gChan['chan_id']:
          for gChan in DatabaseConfig.db.g_link_testing.find():
            if message.guild.id != gChan['ser_id']:
              embed = discord.Embed(title=message.author.name, color=random.randint(0, 16777215))
              pfp = message.author.avatar_url
              icon = message.guild.icon_url
              embed.set_thumbnail(url=(pfp))
              embed.set_author(name=message.guild.name,icon_url=(icon))
              embed.set_footer(text="Credits to JDJG Inc. Official#3493 and RenDev#2616!")
              embed.add_field(name=str(GlobalLinker.FilterMessage(message)),value=day,inline=True)
              channel = client.get_channel(gChan['chan_id'])
              try:
                await channel.send(embed=embed)
              except:
                print(gChan['chan_id'])
      for chanId in DatabaseControl.GetLinkedChannelsList(message.channel.id):
        await client.get_channel(chanId).send(ret_str)
        if len(message.attachments) !=0: #attachment Code
          picture = str(message.attachments[0].url)
          await client.get_channel(chanId).send(picture)
  if message.content.startswith(discordprefix+"GetChannelId") and not message.author.bot:
    await message.channel.send(message.channel.id)
    return 
  if message.content.startswith(discordprefix+"linkchannel") and not message.author.bot:
      n1 = str(message.content.split(" ")[1])
      n1 = DatabaseControl.to_ChannelId(n1)
      n2 = str(message.content.split(" ")[2])
      n2 = DatabaseControl.to_ChannelId(n2)
      await message.channel.send(DatabaseControl.AddChannelLink(n1,n2))
      return
  if message.content.startswith(discordprefix+"guilds") and not message.author.bot:
    for guild in client.guilds:
      a = f'Guild Name:\t\t{guild.name}\n'
      b = f'Guild Owner:\t\t{guild.owner}\n'
      c = f'Guild ID:\t\t\t{guild.id}\n'
      d = f'Guild Owner ID:\t\t{guild.owner.id}\n'
      e = f'Guild Member Count:\t{guild.member_count}\n'
      f = f'Server Creation Date:\t{guild.created_at}\n'
      g = f'Owner Creation Date:\t{guild.owner.created_at}\n\n'
      r = open("guilds.txt","a")
      r.write(a)
      r = open("guilds.txt","a")
      r.write(b)
      r = open("guilds.txt","a")
      r.write(c)
      r = open("guilds.txt","a")
      r.write(d)
      r = open("guilds.txt","a")
      r.write(e)
      r = open("guilds.txt","a")
      r.write(f)
      r = open("guilds.txt","a")
      r.write(g)
      r.close()
    file = discord.File("guilds.txt")
    await message.channel.send(f"{len(client.guilds)} servers | {len(client.users)} users")
    await message.channel.send(f"Here is the info you requested",file = file)
    os.remove("guilds.txt")
  if message.content.startswith(discordprefix+"deletelink") and not message.author.bot:
      if n1 == None or n2 == None:
        n1 = str(message.content.split(" ")[1])
        n1 = DatabaseControl.to_ChannelId(n1)
        n2 = str(message.content.split(" ")[2])
        n2 = DatabaseControl.to_ChannelId(n2)
        await message.channel.send(DatabaseControl.DeleteChannelLink_ChanNum(n1,n2))
        return
  if message.content.startswith(discordprefix+"global") and not message.author.bot:
    args = "NULL"
    try:
      args = message.content.split(" ")[1]
    except:
      await message.channel.send("No argument put! ``link`` adds a link, and ``delete`` deletes the link!")
    if(args=="link"):
      await message.channel.send(GlobalLinker.AddGlobalLink(client,message))
      return
    if(args=="delete"):
      await message.channel.send(GlobalLinker.TerminateLink(message))
      return
    if(args=="test"):
      await GlobalLinker.FindGlobal(message)
      return
    return
  if message.content.startswith(discordprefix+"invite") and not message.author.bot:
    embed = discord.Embed(title = "Here is my invitation link!", description = "https://discord.com/api/oauth2/authorize?client_id=739480439030284390&permissions=379904&scope=bot")
    await message.channel.send(embed=embed)
  if message.content.startswith(discordprefix+"help") and not message.author.bot:
    embed = discord.Embed(title = "Welcome to the Starry Linker!", description = "My prefix is ``starlink+``", color=random.randint(0, 16777215))
    embed.set_footer(text = "The creator of this app is <@717822288375971900> (Shadi#8794), and many credits are given to <@168422909482762240> (JDJG Inc. Official#3493) and <@357006546674253826> (RenDev#2616) for making much of the code that helps this bot work!)")
    embed.add_field(name = "Get the Channel ID", value = '``starlink+GetChannelId``')
    embed.add_field(name = "Global Linker", value = '``starlink+global``')
    embed.add_field(name = "Link Two Channels", value = '``starlink+linkchannel <id1> <id2>``')
    embed.add_field(name = "Invite Me!", value = '``starlink+invite``')
    embed.add_field(name = "``starlink+global`` args:", value = "``link`` does global link, ``delete`` will delete the link.", inline = False)
    embed.set_footer(text = f"{len(client.guilds)} servers | {len(client.users)} users")
    embed.set_image(url='https://media1.tenor.com/images/24b4cf8512e58420d0cdfea3df5a3cce/tenor.gif?itemid=14432583')
    await message.channel.send(embed=embed)
  if message.content.startswith(discordprefix+"getlinkedchannels") and not message.author.bot:
    for gChan in DatabaseConfig.db.g_link_testing.find():
      if message.channel.id == gChan['chan_id']:
        for gChan in DatabaseConfig.db.g_link_testing.find():
          if message.guild.id != gChan['ser_id']:
            for chanId in DatabaseControl.GetLinkedChannelsList(message.channel.id):
              await client.get_channel(chanId).send(ret_str)
              channel = client.get_channel(gChan['chan_id'])
              link = await message.channel.create_invite(max_age = 300)
              channel = client.get_channel(768222305687699477)
              await channel.send(link)

@client.event
async def on_message_delete(message):
  if not message.author.bot:
    try:
     can = await GlobalLinker.FindGlobal(message)
     for obj in can:
        channel = client.get_channel(int(obj["chan_id"]))
        msg= await channel.fetch_message(obj["mes_id"].id)
        print(msg.id)
        await msg.delete()
    except:
      banana = 0

@client.event
async def on_typing(channel,user,_time):
  if not user.bot:
    #try:
    docs = DatabaseConfig.db.g_link_testing.find()
    for chan in docs:
      if (chan["chan_id"]!=channel.id):
       # print("CHAN_ID: "+str(chan["chan_id"]))
        try:
          #print(client.get_channel(int(chan["chan_id"])).name)
          await client.get_channel(int(chan["chan_id"])).trigger_typing()
        except:
          banana = 1
    return
    #except:
  return

@client.event
async def on_message_edit(before,after):
   if not after.author.bot:
    try:
     can = await GlobalLinker.FindGlobal(before)
     newEmbed = GlobalLinker.GetGlobalEmbed(after)
     for obj in can:
        channel = client.get_channel(int(obj["chan_id"]))
        msg= await channel.fetch_message(obj["mes_id"].id)
        await msg.edit(embed = newEmbed)
    except:
      banana = 0

@client.event
async def on_command_error(message, error):
  await message.channel.send("There has been an error!!")
  await message.channel.send(f'{error}')
  return




B.b()
client.run(os.getenv('TOKEN'))