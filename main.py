import discord
import os
from dotenv import load_dotenv
from discord.ext import commands
import json

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

client = commands.Bot(intents=intents, command_prefix="!")

JSON_FILE = "pushups.json"

def error_embed(name, value):
    embed = discord.Embed(title="Error", colour=discord.Colour.red())
    embed.add_field(name=name, value=value)
    return embed

def pushups_embed(users_pushups):
    embed = discord.Embed(title='Pushups', colour = discord.Colour.blue())
    for user_id, pushups in users_pushups.items():
        user = client.get_user(int(user_id))

        embed.add_field(name=user.display_name, value=pushups, inline=False)
    return embed

@client.event
async def on_ready():
    client.command_prefix = f"<@{client.user.id}> "
    print('client ready')


def get_pushup_data():
    file = open(JSON_FILE, "r") 
    pushups_data = json.load(file)
    file.close()
    return pushups_data


@client.event
async def on_message(message):
    if message.author.bot:
        return

    true_message = str.replace(message.content, "<@" + str(client.user.id) + ">", "").strip()

    if true_message == "stats":
        pushup_data = get_pushup_data()

        await message.reply(embed=pushups_embed(pushup_data))

    try:
        pushups = int(true_message)
    except:
        return

    pushup_data = get_pushup_data()
    
    total_pushups = pushup_data.get(message.author.id, 0)
    pushup_data[str(message.author.id)] = total_pushups + pushups

    file = open(JSON_FILE, "w")
    json.dump(pushup_data, file)
    file.close()

    await message.reply(f"Wow! <@{message.author.id}> just did {pushups} pushups!")

BASEDIR = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(BASEDIR, '.env'))
token = os.getenv('TOKEN')
client.run(token)