import asyncio
import discord
import os
import json
import random
from discord.embeds import Embed
from discord.ext import commands
from discord.ext.commands import errors
from discord.message import Message
# from discord_slash import SlashCommand
# from discord_slash.utils.manage_commands import create_option, create_choice
from datetime import datetime
# from collections import namedtuple
import traceback
import sys
from jsonfuncs import *

intents = discord.Intents.default()
intents.members = True
intents.reactions = True
client = commands.Bot(command_prefix = '_', intents=intents, help_command=None, allowed_mentions = discord.AllowedMentions(everyone = False, roles = False))
# slash = SlashCommand(client, sync_commands=True)
# Wonyoung, Sakura, Yuri, Yena, Yujin, Nako, Eunbi, Hyewon, Hitomi, Chaewon, Minju, Chaeyeon
embedcolours = [discord.Color.from_rgb(217,89,140), discord.Color.from_rgb(241,210,231), discord.Color.from_rgb(243,170,81), discord.Color.from_rgb(252,246,149), discord.Color.from_rgb(86,122,206), discord.Color.from_rgb(183,211,233), discord.Color.from_rgb(187,176,220), discord.Color.from_rgb(219,112,108), discord.Color.from_rgb(241,195,170), discord.Color.from_rgb(206,229,213), discord.Color.from_rgb(254,254,254), discord.Color.from_rgb(167,224,225)]
helplist = [['reportabug', '**DM-ONLY:** Allows the user to report a bug!', '`bugreport`, `reportabug`, `reportbug`, `rab`, `rb`'], ['snow', 'Who knows?', '`snow`'], ['help', 'Displays the help message with all of the commands!', '`help`, `h`'], ['say', '**DEV-ONLY:** Lets the bot say something in a channel!', '`say`'], ['shutdown', '**DEV-ONLY:** Shuts the bot down.', '`shutdown`, `sd`, `jaljjayo`, `snowwhendubu`, `maliwhensunoo`'], ['ping', "Checks the bot's latency.", '`ping`, `p`'], ['pong', '**DM-ONLY:** Make the bot say "Pong"! Made to test DM-Only commands.', '`pong`'], ['bugreport', '**DM-ONLY:** Allows the user to report a bug!', '`bugreport`, `reportabug`, `reportbug`, `rab`, `rb`'], ['reportbug', '**DM-ONLY:** Allows the user to report a bug!', '`bugreport`, `reportabug`, `reportbug`, `rab`, `rb`'], ['rb', '**DM-ONLY:** Allows the user to report a bug!', '`bugreport`, `reportabug`, `reportbug`, `rab`, `rb`'], ['rab', '**DM-ONLY:** Allows the user to report a bug!', '`bugreport`, `reportabug`, `reportbug`, `rab`, `rb`']]
staffids = [389897179701182465, 221188745414574080, 303901339891531779, 257900648618655746, 193962293342502912, 364045258004365312, 297278578435948545]

intents = discord.Intents.default()
intents.members = True

@client.event
async def on_ready():
    await client.change_presence(activity = discord.Activity(type=discord.ActivityType.listening, name='DMs!'))
    print(f'{datetime.now().strftime("%d/%m/%Y %H:%M:%S")}::: Bot is ready!')
# --Load cogs--
cogs = ["testcmds"]

for cog in cogs:
    client.load_extension("cogs." + cog)
    print(f"{datetime.now().strftime("%d/%m/%Y %H:%M:%S")}::: Loaded {cog} cog")

# --Start bot--
client_token = os.environ.get("TOKEN")
client.run(client_token)
