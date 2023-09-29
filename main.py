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


def get_pushup_data_from_user(user_id: int):
    file = open(JSON_FILE, "r") 
    pushups_data = json.load(file)
    file.close()
    return pushups_data.get(str(user_id), 0)

def get_pushup_data():
    file = open(JSON_FILE, "r") 
    pushups_data = json.load(file)
    file.close()
    return pushups_data

def set_pushup_data(pushup_data):
    file = open(JSON_FILE, "w")
    json.dump(pushup_data, file)
    file.close()

def remove_empty_values(array: list[str]):
    result: list[str] = []
    for v in array:
        if v:
            result.append(v)
    return result


@client.event
async def on_ready():
    client.command_prefix = f"<@{client.user.id}> "
    print('client ready')


@client.event
async def on_message(message):
    if message.author.bot:
        return

    true_message = str.replace(message.content, "<@" + str(client.user.id) + "> ", "")
    args = true_message.split(" ")
    args = remove_empty_values(args)
    if not len(args):
        return
    if args[0] == "stats":
        if len(args) > 1:
            args_users_pushups = {}
            for i in range(len(args)):
                if i == 0:
                    continue
                user_id = int(args[i][2:len(args[i])-1])
                args_users_pushups[user_id] = get_pushup_data_from_user(user_id)
            return await message.reply(embed=pushups_embed(args_users_pushups))
                
        pushup_data = get_pushup_data()

        await message.reply(embed=pushups_embed(pushup_data))

    try:
        pushups = int(true_message)
    except:
        return

    pushup_data = get_pushup_data()
    
    total_pushups = pushup_data.get(message.author.id, 0)
    pushup_data[str(message.author.id)] = total_pushups + pushups

    set_pushup_data(pushup_data)

    await message.reply(f"Wow! <@{message.author.id}> just did {pushups} pushups!")

BASEDIR = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(BASEDIR, '.env'))
token = os.getenv('TOKEN')
client.run(token)