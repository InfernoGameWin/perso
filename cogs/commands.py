import random

from discord.ext import commands
import discord
import time
from random import randint
import asyncio

import requests
from bs4 import BeautifulSoup


class SomeCommands(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.last_msg = None

    @commands.Cog.listener()
    async def on_ready(self):
        print("| *-* Bot prêt *-* |")

    @commands.command(name="ping")
    async def ping(self, ctx: commands.Context):
        start_time = time.time()
        message = await ctx.send("Testing ping...")
        end_time = time.time()

        await message.edit(content=f"Ping **{round(self.bot.latency * 1000)}ms**\n"
                                   f"API: **{round(end_time - start_time) * 1000}ms**")

    @commands.command(name="setstatus", aliases=["ss"])
    @commands.cooldown(rate=1, per=15)
    @commands.has_guild_permissions(manage_guild=True)
    @commands.is_owner()
    async def _setstatus(self, ctx: commands.Context, *, text: str):
        if text == "None":
            await self.bot.change_presence(activity=None)
            print("1")
        else:
            await self.bot.change_presence(activity=discord.Game(name=text))

    @_setstatus.error
    @commands.is_owner()
    async def _setstatus_error(self, ctx: commands.Context, error: commands.CommandError):
        if isinstance(error, commands.CommandOnCooldown):
            message = f"Attendez {round(error.retry_after, 1)}s"
        elif isinstance(error, commands.MissingPermissions):
            message = f"Il faut que vous ayez la permission {error.missing_perms}."

        embed = discord.Embed(title="Error message",
                              colour=discord.Colour.red,
                              description=message)

        await ctx.send(embed=embed)
        await ctx.message.delete(delay=5)

    @commands.Cog.listener()
    @commands.is_owner()
    async def on_member_join(self, member: discord.Member):
        channel = self.bot.get_channel(837067435696848976)

        if not channel:
            return

        await channel.send(f"Bienvenue, {member.mention} le frérot!")

    @commands.Cog.listener()
    @commands.is_owner()
    async def on_message_delete(self, message: discord.Message):
        self.last_msg = message

    @commands.command(name="snipe")
    @commands.is_owner()
    async def snipe(self, ctx: commands.Context):
        if not self.last_msg:
            await ctx.send("There is no message to snipe!")
            return

        author = self.last_msg.author
        content = self.last_msg.content

        embed = discord.Embed(title=f"Message from {author}", description=content)
        await ctx.send(embed=embed)

    @commands.command(name="embed")
    @commands.is_owner()
    async def _embed(self, ctx: commands.Context):

        avatar_url = ctx.author.avatar_url

        embed = discord.Embed(title="Hello world!",
                              description=":D",
                              colour=discord.Color(random.randrange(0, 100000, 5000)))
        embed.set_author(name=ctx.author, icon_url=avatar_url)

        await ctx.send(embed=embed)

    @commands.command(name="hackhtmlpro", aliases=["hackprohtmlomg", "hhp"])
    @commands.is_owner()
    async def _hax(self, ctx: commands.Context):

        message = await ctx.send("...")
        timea = time.time()
        for _ in range(50):
            binary = list()
            for _ in range(750):
                n = randint(0, 1)
                binary.append(str(n))
                title = ""

            binary = "".join(binary)
            embed = discord.Embed(title="??!!?", colour=discord.Colour.dark_green(), description=binary)
            await message.edit(content=None, embed=embed)
            await asyncio.sleep(0.5)
        await message.delete()
        timeb = time.time()
        print(f"Temps commande: _hax :\n{round(timeb - timea, 1)}s\n")

    @commands.command(name="btc")
    @commands.cooldown(rate=1, per=15)
    @commands.is_owner()
    async def _btc(self, ctx: commands.Context):
        url = "https://www.google.com/finance/quote/BTC-EUR"

        response = requests.get(url)

        if response.ok:
            soup = BeautifulSoup(response.text, "html.parser")
            div = soup.find_all("div", class_="ln0Gqe")
            btc = div[0]
            price = str(btc.div.div.div.div.text) + "€"
            embed = discord.Embed(title="BTC Price",
                                  description=price,
                                  colour=discord.Colour.green())
            await ctx.send(embed=embed)

    @commands.command(name="clear")
    @commands.has_guild_permissions(manage_messages=True)
    async def _clear(self, ctx: commands.Context, amount: int):
        await ctx.channel.purge(limit=amount)

    # @commands.command(name="allcommands", aliases=["ac"])
    # @commands.is_owner()
    # async def _all_commands(self, ctx):
    #     for cog in self.bot.cogs:
    #         print(cog)
    #
    #     print("--------------")
    #
    #     for command in self.bot.walk_commands():
    #         print(command)


def setup(bot: commands.Bot):
    bot.add_cog(SomeCommands(bot))
