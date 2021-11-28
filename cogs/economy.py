from discord.ext import commands
import discord
import json
import random
import asyncio

class EconomyCommands(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    # c'est des methodes la :
    @staticmethod
    async def is_registered(user_id):
        with open("./data/economy.json") as f:
            data = json.load(f)

        for user in data["users"]:
            try:
                if user["id"] == user_id:
                    return True
            except KeyError:
                return False


    @staticmethod
    async def create_account(user_id):

        with open("./data/economy.json", "r") as f:
            data = json.load(f)

        to_add = {"id": user_id, "money": 1000}
        data["users"].append(to_add)

        with open("./data/economy.json", "w") as f:
            json.dump(data, f, indent=2)

    @staticmethod
    async def get_money(user_id):
        with open("./data/economy.json") as f:
            data = json.load(f)
        for user in data["users"]:
            if user["id"] == user_id:
                return user["money"]

    @staticmethod
    async def change_money(user_id, amount):
        with open("./data/economy.json") as f:
            data = json.load(f)
        for user in data["users"]:
            if user["id"] == user_id:
                user["money"] += amount
                break

        with open("./data/economy.json", "w") as f:
            json.dump(data, f, indent=2)
            return user["money"]

    @commands.command(name="balance", aliases=["bl"])
    async def _balance(self, ctx: commands.Context):
        # SEE YOUR MONEY
        user = ctx.author
        user_id = user.id

        if await EconomyCommands.is_registered(user_id) is True:
            money = await EconomyCommands.get_money(user_id)
            embed = discord.Embed(title=":money_with_wings: Your balance :money_with_wings: ",
                                  description=f"Your money: {money}$",
                                  colour=discord.Colour.green())
            embed.set_footer(text=user.name, icon_url=user.avatar_url)
            await ctx.send(embed=embed)
        else:
            message = await ctx.send("isn't registered")
            await EconomyCommands.create_account(user_id)
            embed = discord.Embed(title="Balance",
                                  description="Your bank account has been created.",
                                  colour=discord.Colour(random.randint(1, 5)))
            await message.edit(embed=embed)

    @commands.command(name="roulette", aliases=["rl"])
    async def _roulette(self, ctx: commands.Context):
        # PLAY ROULETTE

        #CONSTANTS
        global plr_color, message, plr_number, color

        #CHECK IF THE USER HAS A BANK ACCOUNT
        if await EconomyCommands.is_registered(ctx.author.id) and await EconomyCommands.get_money(ctx.author.id) > 0:
            pass #IS REGISTERED AND HAVE MONEY
        elif await EconomyCommands.is_registered(ctx.author.id) is False or await EconomyCommands.get_money(ctx.author.id) <= 0:
            if await EconomyCommands.is_registered(ctx.author.id) is False:
                await EconomyCommands.create_account(ctx.author.id)
            embed = discord.Embed(colour=discord.Colour.red())
            embed.add_field(name="Bank", value="You have 0$ or less on your bank account.\n\
                            Get some money then come to play to the roulette.")
            embed.set_footer(text=ctx.author.name,icon_url=ctx.author.avatar_url)
            await ctx.send(embed=embed)
            return

        embed = discord.Embed(title="Roulette",
                                    description="**Voulez-vous jouer à la roulette?**",
                                    colour=discord.Colour.orange())
        embed.set_footer(text=ctx.author.name, icon_url=ctx.author.avatar_url)
        actual_message = await ctx.send(embed=embed)
        await actual_message.add_reaction("✅")
        await actual_message.add_reaction("❌")

        #CHECKS
        def check_reaction(reaction, user):
            return ctx.message.author == user and reaction.message.id == actual_message.id

        def check_message(message):
            return message.author == ctx.author and message.channel == actual_message.channel

        try:
            reaction, user = await self.bot.wait_for("reaction_add", timeout=30, check=check_reaction)
            if reaction.emoji == "✅":
                # ca continue
                embed = discord.Embed(title="Roulette",
                                      description="Voulez-vous choisir une couleur? Si oui, "
                                                  "quelle couleur choisissez vous?",
                                      color=discord.Colour(random.randrange(0, 100000, 5000)))
                await actual_message.clear_reactions()
                await actual_message.edit(embed=embed)
                await actual_message.add_reaction("⚫")
                await actual_message.add_reaction("🔴") # un probleme ici
                await actual_message.add_reaction("🟢") # et la aussi
                await actual_message.add_reaction("❌")

                reaction, user = await self.bot.wait_for("reaction_add", timeout=30, check=check_reaction)

                if reaction.emoji == "⚫":
                    plr_color = "noir"
                elif reaction.emoji == "🔴":
                    plr_color = "rouge"
                elif reaction.emoji == "🟢":
                    plr_color = "vert"
                elif reaction.emoji == "❌":
                    plr_color = None

                # on prend le numéro mtn

                nb_lock = False

                while nb_lock is False:

                    embed = discord.Embed(title="Roulette",
                                          description="Choisissez un numéro entre **0** et **36**",
                                          color=discord.Colour(random.randrange(0, 100000, 5000)))
                    await actual_message.clear_reactions()
                    await actual_message.edit(embed=embed)

                    message = await self.bot.wait_for("message", timeout=30, check=check_message)

                    plr_number = str(message.content).split()
                    try:
                        for n in plr_number:
                            n = int(n)
                            if len(plr_number) > 1 or not 0 <= n <= 36:
                                await ctx.send("Veuillez n'entrer qu'un numéro valide", delete_after=5)
                                await message.delete()
                                continue
                            elif len(plr_number) == 1 and 0 <= n <= 36:
                                nb_lock = True
                                await message.delete()
                    except ValueError:
                        await ctx.send("Veuillez entrer un numéro valide.", delete_after=5)
                        await message.delete()
                        continue

                plr_number = int("".join(plr_number))
                await actual_message.edit(content=f"Vous avez choisis le {plr_number} {plr_color}", embed=None)

                await asyncio.sleep(2)
                # LE JOUEUR DONNE LA SOMME D'ARGENT A JOUER
                embed = discord.Embed(title="Roulette",
                                      description="Combien d'argents voulez-vous miser?")
                await actual_message.edit(content=None, embed=embed)
                money_lock = False

                while money_lock is False:
                    try:
                        message = await self.bot.wait_for("message", timeout=30, check=check_message)
                        bet_money = int(message.content)
                        plr_money = int(await EconomyCommands.get_money(ctx.author.id))
                        if bet_money <= plr_money:
                            money_lock = True
                            await message.delete()
                            break
                    except ValueError:
                        await ctx.send("Veuillez entrer un numéro valide.", delete_after=5)
                        await message.delete()
                        continue

                print("salut")

                nombre_de_point = 0
                point = ""
                while nombre_de_point < 10:
                    embed = discord.Embed(title="Roulette",
                                          description=f"Le croupier lance la bille{point}")
                    nombre_de_point += 1
                    if point == "...":
                        point = ""
                    point += "."
                    await actual_message.edit(content=None, embed=embed)
                    await asyncio.sleep(0.2)

                result_number = random.randrange(0, 36)
                result_color = random.randrange(0, 38)

                if result_color <= 1:
                    color = "vert"
                elif result_color <= 19:
                    color = "rouge"
                elif result_color <= 37:
                    color = "noir"

                multiplicator = 0.0

                # ON APPLIQUE LE MULTIPLICATOR POUR LA SOMME GAGNEE OU PERDUE
                if plr_color == color and color == "vert":
                    multiplicator += 2.5
                elif plr_color == color:
                    multiplicator += 1.5

                if plr_number == result_number:
                    multiplicator += 3.0

                # ON DEFINIT LA SOMME DARGENT GAGNEE OU PERDUE GRACE AU MULTIPLICATOR
                result_money = bet_money * multiplicator
                embed = discord.Embed(colour=discord.Color.random())
                embed.add_field(name="Roulette",
                                value=f"La bille est tombé sur le {result_number} {color}")
                await actual_message.edit(content=None, embed=embed)
                await asyncio.sleep(2)
                embed.clear_fields()
                if result_money == 0:
                    embed.add_field(name="Roulette",
                                    value=f"Vous avez perdu {bet_money}$! (CHEH)")
                    await actual_message.edit(content=None, embed=embed)
                    await EconomyCommands.change_money(ctx.author.id, (-bet_money))
                else:
                    embed.add_field(name="Roulette",
                                    value=f"Vous ressortez du casino avec {result_money}$! (konar)")
                    await actual_message.edit(content=None, embed=embed)
                    await EconomyCommands.change_money(ctx.author.id, bet_money)
                return

            else:
                cancelled_embed = discord.Embed(description="❌ Partie annulée ❌",
                                                colour=discord.Colour.red())
                await actual_message.clear_reactions()
                await actual_message.edit(embed=cancelled_embed)
                return
        except asyncio.TimeoutError:
            cancelled_embed = discord.Embed(description="❌ Partie annulée ❌",
                                            colour=discord.Colour.red())
            await actual_message.clear_reactions()
            await actual_message.edit(embed=cancelled_embed)
            return

    # @commands.command(name="givemoney", aliases=["gm"])
    # async def _give_money(self, ctx: commands.Context, user: discord.Member, amount: int()):
    #     # GIVE MONEY TO SOMEONE
    #     pass
    #
    # @commands.command(name="shop")
    # async def _shop(self, ctx: commands.Context):
    #     # SHOW SHOP
    #     pass
    #
    # """
    # @commands.command()
    # async def _stats(self, ctx: commands.Context):
    #     #SHOW YOUR STATS
    #     pass
    # """
    #
    # @commands.command(name="buy", aliases=["buy"])
    # async def _buy(self, ctx: commands.Context, object, amount: int()):
    #     # BUY SOMETHING IN THE SHOP
    #     pass
    #
    # @commands.command(name="inventory", aliases=["inv"])
    # async def _inventory(self, ctx: commands.Context):
    #     # SHOW YOUR INVENTORY
    #     pass
    #
    # """
    # CASINO JEUX:
    # ROULETTE
    # """
    #

def setup(bot: commands.Bot):
    bot.add_cog(EconomyCommands(bot))
