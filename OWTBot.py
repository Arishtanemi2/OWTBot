# -*- coding: utf-8 -*-
"""
Spyder Editor

Author: Arishtanemi
"""
import random
import asyncio
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
@bot.command()
async def info():
    embed = discord.Embed(title="OWTBot", description="Namaskaram! I am here to make your server experiance better!", color=0xeee657)
    
    # author info
    embed.add_field(name="Author:", value="Arishtanemi")
    # command list for general users
    embed.add_field(name="Commands:", value="Use the following to interact with me")
    #add user to giveawaY COMMAND
    embed.add_field(name="!add <Your Username>", value="Add your name as a giveaway participant")
    #extra featureslist
    embed.add_field(name="!dialogue", value="I tell a random Telugu Movie Dialogue")

    await bot.say(embed=embed)
    
async def my_background_task():
    await bot.wait_until_ready()
    counter = 0
    while not bot.is_closed:
        counter += 1
        await bot.say(counter)
        await asyncio.sleep(5) # task runs every 60 seconds
bot.loop.create_task(my_background_task())
bot.run('NDM3NTAzNDE4ODAyNjM0NzUy.Db9F0w.kxrmOB_5zYr3713w_MI3pL6JFGI')
