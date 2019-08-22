# -*- coding: utf-8 -*-
"""
Author: Arishtanemi
"""
import random
import discord
from discord.ext import commands
from discord import Game
import asyncio
import praw
import requests
import json
users=[]
password="Gochi"
f = open('participants.txt', 'r')
users = list(f)
f.close()
f = open('dialogues.txt', 'r')
dialogues = list(f)
f.close()
f = open('scrims.txt', 'r')
scrims = list(f)
f.close()
bot = commands.Bot(command_prefix='gg', description='')
bot.remove_command('help')
reddit = praw.Reddit(client_id='VxdjW8xlme18VA',
                     client_secret='I1uKbHIxRx0LEeZCT_EXvyL6Y4M',
                     user_agent='Discord:1234:0.6')
print(reddit.read_only)

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    await bot.change_presence(game=Game(name="Gochi Gang"))
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
    f.close()
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
    embed = discord.Embed(title="Ganesh Gaitonde", description="Jaake dekh file main matherchod kis bhagwan ka naam likha hain", color=0xeee657)
    
    # author info
    embed.add_field(name="Author:", value="Arishtanemi")
    # command list for general users
    await bot.say(embed=embed)
@bot.command(pass_context=True)
async def startscrim(ctx,play:str,time:str):
    msg = '{0.author.mention} wants to play '.format(ctx.message)
    save= '{0.author.mention}'.format(ctx.message)
    f=open('scrims.txt','a+')
    f.write(save+' '+play+' '+time+'\n')
    scrims.append(save+' '+play+' '+time)
    f.close()
    await bot.say(msg+play+' at '+time)
@bot.command()
async def showscrims():
    embed = discord.Embed(title="Scrims Scheduled", description="", color=0xff0000)
    if(scrims.__len__()==0):
        embed.add_field(name="No Scrims Scheduled", value="")
    for i in range(0,scrims.__len__()):
        embed.add_field(name=str(i+1), value=str(scrims[i]))
    await bot.say(embed=embed)
@bot.command()
async def help():
    embed = discord.Embed(title="My Commands", description="Use the following to interact with me", color=0x0080ff)
    #main COMMANDS
    embed.add_field(name="ggadd <Your Username>", value="Add your name as a giveaway participant")
    embed.add_field(name="ggstartscrim <game-mode> <Time>", value="Start a scrim for others to join Ex: ggstartscrim QuickPlay 7PM")
    embed.add_field(name="ggshowscrims", value="Show all the Scheduled scrims")
    #extra featureslist
    
    embed.add_field(name= "ggbored",value="Bored or server dead? Fetches a random GIF to keep you entertained")
    embed.add_field(name="ggdialogue", value="Apne Andar ke Gaitonde ko jagao")
    #utility functions
    embed.add_field(name="gginfo", value="Show some info about me")
    embed.add_field(name="gghelp", value="show the help menu")
    await bot.say(embed=embed)
    
@bot.command()
async def bored():
       await bot.say("http://imgur.com/random")

@bot.command()
async def r6meme():       
    subreddit = reddit.subreddit('shittyrainbow6')
    rand=random.randrange(0,10)
    i=0
    for submission in subreddit.new(limit=10):
        if rand==i:
            await bot.say(submission.title)  
            await bot.say(submission.url)
        i+=1


@bot.command()
async def r6sstats(user : str):
    request = requests.get('https://r6tab.com/api/search.php?platform=uplay&search='+user, auth=('', ''))
    data=json.loads(json.dumps(request.json()))
    embed = discord.Embed(title=user, description="Statistics", color=0x0080ff)
    embed.add_field(name="Username", value=data['results'][0]['p_name'])
    embed.add_field(name="Level", value=data['results'][0]['p_level'])
    embed.add_field(name="K/D", value=data['results'][0]['kd'])
    embed.add_field(name="MMR", value=data['results'][0]['p_currentmmr'])
    embed.add_field(name="Rank", value=data['results'][0]['p_currentrank'])
    await bot.say(embed=embed)

bot.run("NDM3NTAzNDE4ODAyNjM0NzUy.XU-w9A.4G4e-OPye_-n7GQ5TI499Zz2XEU")
