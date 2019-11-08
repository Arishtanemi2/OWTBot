# -*- coding: utf-8 -*-
"""
Author: Arishtanemi
"""
import random
import discord
from discord.ext import commands
from discord import Game,opus
import asyncio
import praw
import requests
import json
import youtube_dl
import urllib.request
import urllib.parse
import re


#----------------------------------------------------Variable Section---------------------------------------------------------------
users=[]
players={}
queues={}
password="pass"
f = open('participants.txt', 'r')
users = list(f)
f.close()
f = open('dialogues.txt', 'r')
dialogues = list(f)
f.close()
f = open('scrims.txt', 'r')
scrims = list(f)
f.close()
botprefix="!"
bot = commands.Bot(command_prefix=botprefix, description='')
bot.remove_command('help')
reddit = praw.Reddit(client_id='VxdjW8xlme18VA',
                     client_secret='I1uKbHIxRx0LEeZCT_EXvyL6Y4M',
                     user_agent='Discord:1234:0.6')
print(reddit.read_only)


@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    await bot.change_presence(game=Game(name="Beep Boop"))

#---------------------------------------------------------------------Game SECTION-------------------------------------------------------------------
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
    embed = discord.Embed(title="I am a simple bot", description="", color=0xeee657)
    
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

#---------------------------------------------------------------------MUSIC SECTION-------------------------------------------------------------------
@bot.command(pass_context=True)
async def join(ctx):
    channel=ctx.message.author.voice.voice_channel
    if channel== None:
        await bot.say("you are not connected to a voice channel")
    else:
        await bot.join_voice_channel(channel)

@bot.command(pass_context=True)
async def leave(ctx):
    server=ctx.message.server
    voice_client=bot.voice_client_in(server)
    await voice_client.disconnect()

@bot.command(pass_context=True)
async def play(ctx,searchstring="",*args):
    if searchstring=="":
        id=ctx.message.server.id
        players[id].resume()
        return
    for arg in args:
        searchstring+=" "+arg
    channel=ctx.message.author.voice.voice_channel
    server=ctx.message.server
    if channel== None:
        await bot.say("you are not connected to a voice channel")
    voice_client=bot.voice_client_in(server)
    if voice_client==None:
        await bot.join_voice_channel(channel)
    server=ctx.message.server
    voice_client=bot.voice_client_in(server)
    query_string = urllib.parse.urlencode({"search_query" : searchstring})
    html_content = urllib.request.urlopen("http://www.youtube.com/results?" + query_string)
    search_results = re.findall(r'href=\"\/watch\?v=(.{11})', html_content.read().decode())
    await bot.say("Arey Ganpat Baja: "+ "http://www.youtube.com/watch?v=" + search_results[0])
    opts="-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5" 
    player= await voice_client.create_ytdl_player(url="http://www.youtube.com/watch?v=" + search_results[0],before_options=opts,after=lambda: check_queue(server.id))
    players[server.id]=player
    player.start()

@bot.command(pass_context=True)
async def pause(ctx):
    id=ctx.message.server.id
    players[id].pause()

@bot.command(pass_context=True)
async def stop(ctx):
    id=ctx.message.server.id
    players[id].stop()


@bot.command(pass_context=True)
async def resume(ctx):
    id=ctx.message.server.id
    players[id].resume()

@bot.command(pass_context=True)
async def queue(ctx,searchstring="",*args):
    for arg in args:
        searchstring+=" "+arg
    server=ctx.message.server
    voice_client=bot.voice_client_in(server)
    query_string = urllib.parse.urlencode({"search_query" : searchstring})
    html_content = urllib.request.urlopen("http://www.youtube.com/results?" + query_string)
    search_results = re.findall(r'href=\"\/watch\?v=(.{11})', html_content.read().decode())
    opts="-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5" 
    player= await voice_client.create_ytdl_player(url="http://www.youtube.com/watch?v=" + search_results[0],before_options=opts,after=lambda: check_queue(server.id))
    if(server.id in queues):
        queues[server.id].append(player)
    else:
        queues[server.id]=[player]
    await bot.say("http://www.youtube.com/watch?v=" + search_results[0]+" Aage bajega")

def check_queue(id):
    if queues[id] !=[]:
        player=queues[id].pop(0)
        players[id]=player
        player.start()

@bot.command(pass_context=True)
async def skip(ctx):
    server=ctx.message.server
    player=players[server.id]
    player.stop()
    await bot.say("gaana fasakk")

#---------------------------------------------------------------------Help SECTION-------------------------------------------------------------------
@bot.command()
async def help():
    embed = discord.Embed(title="My Commands", description="Use the following to interact with me", color=0x0080ff)
    #main COMMANDS
    embed.add_field(name=botprefix+"add <Your Username>", value="Add your name as a giveaway participant")
    embed.add_field(name=botprefix+"startscrim <game-mode> <Time>", value="Start a scrim for others to join Ex: ggstartscrim QuickPlay 7PM")
    embed.add_field(name=botprefix+"showscrims", value="Show all the Scheduled scrims")
    #music Commands
    embed.add_field(name=botprefix+"join", value="invite bot to music channel to play")
    embed.add_field(name=botprefix+'play <"Song Name">', value="Start playing the song name")
    embed.add_field(name=botprefix+'queue <"Song Name">', value="queues the song to the current playlist")
    embed.add_field(name=botprefix+"pause", value="pause the current song")
    embed.add_field(name=botprefix+"resume", value="resumes the current song")
    embed.add_field(name=botprefix+"stop", value="stop the current song")
    embed.add_field(name=botprefix+"skip", value="stop the current song")
    #extra featureslist
    embed.add_field(name=botprefix+ "bored",value="Bored or server dead? Fetches a random GIF to keep you entertained")
    embed.add_field(name= botprefix+"r6meme",value="Fetches an R6 meme")
    embed.add_field(name= botprefix+"r6sstats <player name>",value="Fetches the in-game Rainbow 6 siege stats of the player mentioned")
    embed.add_field(name=botprefix+"dialogue", value="Apne Andar ke Gaitonde ko jagao")
    #utility functions
    embed.add_field(name=botprefix+"info", value="Show some info about me")
    embed.add_field(name=botprefix+"help", value="show the help menu")
    await bot.say(embed=embed)
    
#---------------------------------------------------------------------Utility SECTION-------------------------------------------------------------------
@bot.command()
async def bored():
       await bot.say("http://imgur.com/random")

@bot.command()
async def r6meme():       
    subreddit = reddit.subreddit('shittyrainbow6')
    rand=random.randrange(0,50)
    i=0
    for submission in subreddit.hot(limit=50):
        if rand==i:
            await bot.say(submission.title)  
            await bot.say(submission.url)
        i+=1

@bot.command()
async def meme():       
    subreddit = reddit.subreddit('memes')
    rand=random.randrange(0,50)
    i=0
    for submission in subreddit.hot(limit=50):
        if rand==i:
            await bot.say(submission.title)  
            await bot.say(submission.url)
        i+=1

@bot.command()
async def boysmeme():       
    subreddit = reddit.subreddit('theboys')
    rand=random.randrange(0,50)
    i=0
    for submission in subreddit.hot(limit=50):
        if rand==i:
            await bot.say(submission.title)  
            await bot.say(submission.url)
        i+=1

@bot.command()
async def gaali(name :str):
    await bot.say("Neem ka patta kadwa hain "+ name+ " gandu Bhadwa hain")

@bot.command()
async def r6sstats(user : str):
    request = requests.get('https://r6tab.com/api/search.php?platform=uplay&search='+user, auth=('', ''))
    data=json.loads(json.dumps(request.json()))
    fullrequest = requests.get('https://r6tab.com/api/player.php?p_id='+data['results'][0]['p_id'], auth=('', ''))
    fulldata=json.loads(json.dumps(fullrequest.json()))
    embed = discord.Embed(title=user, description="Statistics", color=0x0080ff)
    embed.add_field(name="Username", value=data['results'][0]['p_name'])
    embed.add_field(name="Level", value=data['results'][0]['p_level'])
    embed.add_field(name="Casual Time Played", value=fulldata['data'][5])
    embed.add_field(name="Casual Kills", value=fulldata['data'][6])
    embed.add_field(name="Casual Deaths", value=fulldata['data'][7])
    embed.add_field(name="Casual K/D", value=round(fulldata['data'][6]/fulldata['data'][7],4))
    embed.add_field(name="Casual wins", value=fulldata['data'][8])
    embed.add_field(name="Casual losses", value=fulldata['data'][9])
    embed.add_field(name="Total Bullets", value=fulldata['data'][16])
    embed.add_field(name="Total Headshots", value=fulldata['data'][17])
    embed.add_field(name="Total Suicides :P", value=fulldata['data'][20])
    embed.add_field(name="MMR", value=data['results'][0]['p_currentmmr'])
    embed.add_field(name="Rank", value=data['results'][0]['p_currentrank'])
    await bot.say(embed=embed)

bot.run("NDM3NTAzNDE4ODAyNjM0NzUy.XU-w9A.4G4e-OPye_-n7GQ5TI499Zz2XEU")
