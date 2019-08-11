# -*- coding: utf-8 -*-
"""
Author: Arishtanemi
"""
import random
import discord
from discord.ext import commands
from discord import Game

users=[]
password="NaiBolteJao"
f = open('participants.txt', 'r')
users = list(f)
f.close()
f = open('dialogues.txt', 'r')
dialogues = list(f)
f.close()
f = open('scrims.txt', 'r')
scrims = list(f)
f.close()
bot = commands.Bot(command_prefix='!', description='')
bot.remove_command('help')

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    activity = discord.Game(name="Happy Diwali folks")
    await bot.change_presence(status=discord.Status.idle, activity=activity)
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
    embed = discord.Embed(title="Chitti", description="Hi! I am Chitti the Bot, Memory 44.5 MegaByte, Length 95 lines", color=0xeee657)
    
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
    embed.add_field(name="!add <Your Username>", value="Add your name as a giveaway participant")
    embed.add_field(name="!startscrim <game-mode> <Time>", value="Start a scrim for others to join Ex: !startscrim QuickPlay 7PM")
    embed.add_field(name="!showscrims", value="Show all the Scheduled scrims")
    #extra featureslist
    
    embed.add_field(name= "!bored",value="Bored or server dead? Fetches a random GIF to keep you entertained")
    embed.add_field(name="!dialogue", value="I tell a random Telugu Movie Dialogue")
    #utility functions
    embed.add_field(name="!info", value="Show some info about me")
    embed.add_field(name="!help", value="show the help menu")
    await bot.say(embed=embed)
    
@bot.command()
async def bored():
       await bot.say("http://imgur.com/random")
       

bot.run("NDM3NTAzNDE4ODAyNjM0NzUy.XU-w9A.4G4e-OPye_-n7GQ5TI499Zz2XEU")
