import discord
import os
from dotenv import load_dotenv
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

client = commands.Bot(intents=intents, command_prefix="!")

async def count_pushups(ctx, users):
    users_lowercase = list(map(str.lower, users))
    pushups = {}
    async for message in ctx.channel.history(limit=None):
        if message.author.bot:
            continue
        if len(users) != 0:
            if message.author.name.lower() not in users_lowercase or message.author.nick.lower() not in users_lowercase or message.author.global_name.lower() not in users_lowercase:
                continue
        try:
            message_content_number = int(message.content)
        except:
            message_content_number = 0
        name = message.author.global_name
        if name == None:
            name = message.author.name
        if name in pushups:
            pushups[name] += message_content_number
        else:
            pushups[name] = message_content_number
    return dict(sorted(pushups.items(), key=lambda x:x[1], reverse=True))

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
    print('client ready')

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
