import discord
import os
from dotenv import load_dotenv
from discord.ext import commands
import json

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

client = commands.Bot(intents=intents, command_prefix="!")

def error_embed(name, value):
    embed = discord.Embed(title="Error", colour=discord.Colour.red())
    embed.add_field(name=name, value=value)
    return embed

def pushups_embed(users_pushups):
    embed = discord.Embed(title='Pushups', colour = discord.Colour.blue())
    for k, v in users_pushups.items():
        embed.add_field(name=k, value=v, inline=False)
    return embed

@client.event
async def on_ready():
    client.command_prefix = "<@" + str(client.user.id) + "> "
    print('client ready')

@client.event
async def on_message(message):
    if message.author.bot:
        return
    true_message = str.replace(message.content,"<@" + str(client.user.id) + "> ", "")

    try:
        pushups = int(true_message)
    except:
        return
    
    file = open("pushups.json", "r") 
    pushupsData = json.load(file)
    file.close()

    totalPushups = pushupsData.get(message.author.id, 0)
    pushupsData[str(message.author.id)] = totalPushups + pushups

    file = open("pushups.json", "w")
    json.dump(pushupsData, file)
    file.close()

    await message.reply("Wow! <@" + str(message.author.id) + "> just did " + str(pushups) + " pushups!")
    

@client.command()
async def stats(ctx, *args):
    """Shows stats of members in arguments, if blank shows all members stats"""
    users_pushups = await count_pushups(ctx, args)
    if len(users_pushups) == 0:
        return await ctx.send(embed=error_embed("Invalid arguments", "Arguments doesn\'t match any users in server"))
    return await ctx.send(embed=pushups_embed(users_pushups))

BASEDIR = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(BASEDIR, '.env'))
token = os.getenv('TOKEN')
client.run(token)
