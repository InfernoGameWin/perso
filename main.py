import discord
from discord.ext import commands
# import os
# from setToken import getToken
from secret.config import TOKEN

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix='b!', help_command=None, intents=intents)

owner_ids = ["830486558896816128"]

bot.load_extension("cogs.commands")
# bot.load_extension("cogs.ErrorHandler")
bot.load_extension("cogs.economy")

bot.run(TOKEN)
