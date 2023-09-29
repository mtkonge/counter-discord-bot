import discord
import os
from collections import OrderedDict
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

def help_embed():
    with open("help.md") as file:
        embed = discord.Embed(title='Help', colour = discord.Colour.blue(), )
        embed.add_field(name=" ", value=file.read(), inline=True)
        return embed

def pushups_embed(users_pushups: dict):
    embed = discord.Embed(title='Pushups', colour = discord.Colour.blue())
    for user_id, pushups in users_pushups:
        user = client.get_user(int(user_id))
        embed.add_field(name=user.display_name, value=pushups, inline=False)
    return embed


def get_pushup_data_from_user(user_id: int) -> int:
    file = open(JSON_FILE, "r")  
    pushups_data = json.load(file)
    file.close()
    return pushups_data.get(str(user_id), 0)

def get_pushup_data() -> dict:
    file = open(JSON_FILE, "r") 
    pushups_data = json.load(file)
    file.close()
    return pushups_data

def set_pushup_data(pushup_data: str):
    file = open(JSON_FILE, "w")
    json.dump(pushup_data, file)
    file.close()

def strip_whitespace(array: list[str]):
    result: list[str] = []
    for v in array:
        if v.strip() != "":
            result.append(v.strip())
    return result

def extract_id_from_ping(message: str) -> int | None:
    if message[:2] != '<@':
        return None
    if message[-1:] != '>':
        return None
    try:
        return int(message[2:-1])
    except:
        return None

def get_pushups_data_from_users(users: list[str]) -> dict | None:
    args_users_pushups = {}
    for user_id in users:
        args_users_pushups[user_id] = get_pushup_data_from_user(user_id)
    return args_users_pushups

def is_int(message: str) -> bool:
    try:
        int(message)
        return True
    except:
        return False


@client.event
async def on_ready():
    print('client ready')

@client.event
async def on_message(message):
    if message.author.bot:
        return

    args = strip_whitespace(message.content.split(" "))
    if extract_id_from_ping(args[0]) != client.user.id:
        return
    
    match args[1:]:
        case ['stats', *users] if len(users) != 0:
            users = map(extract_id_from_ping, users)
            await message.reply(embed=pushups_embed(get_pushups_data_from_users(users).items()))
        case ['stats']:
            pushup_data = sorted(get_pushup_data().items(), key=lambda item: item[1], reverse=True)
            await message.reply(embed=pushups_embed(pushup_data))
        case [pushups] if is_int(pushups):
            pushups = int(pushups)

            pushups_data = get_pushup_data()
            total_pushups = pushups_data.get(message.author.id, 0)

            pushups_data[str(message.author.id)] = total_pushups + pushups
            set_pushup_data(pushups_data)

            await message.reply(f"Wow! <@{message.author.id}> just did {pushups} pushups!")
        case _:
            await message.reply(embed=help_embed())

if not os.path.exists("pushups.json"):
    with open("pushups.json", "+w") as file:
        file.write("{}")

BASEDIR = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(BASEDIR, '.env'))
token = os.getenv('TOKEN')
client.run(token)