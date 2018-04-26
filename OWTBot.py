# -*- coding: utf-8 -*-
"""
Spyder Editor

Author: Arishtanemi
"""
import random
import discord
from discord.ext import commands
users=[]
password="AMEIZING"
f = open('participants.txt', 'r')
users = list(f)
f.close();
f = open('dialogues.txt', 'r')
dialogues = list(f)
f.close();
bot = commands.Bot(command_prefix='!', description='')


@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
@bot.command()
async def giveaway(pas: str):
    if pas==password:
        await bot.say("The winner is : " + users[random.randrange(0,users.__len__())])
    else:
        await bot.say('Wrong password cant start the giveaway!')
@bot.command()
async def add(a: str):
    users.append(a)
    f = open('participants.txt', 'a')
    f.write(a+'\n')
    f.close();
    await bot.say('added '+ a)
@bot.command()
async def showparticipants():
    for i in range (0,users.__len__()):
       await bot.say(str(str(i+1) +'. '+ str(users[i])))
@bot.command()
async def dialogue():
       await bot.say(dialogues[random.randrange(0,dialogues.__len__())])
bot.run('NDM3NTAzNDE4ODAyNjM0NzUy.Db9F0w.kxrmOB_5zYr3713w_MI3pL6JFGI')
