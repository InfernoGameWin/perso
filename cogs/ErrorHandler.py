from discord.ext import commands


class ErrorHandler(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx: commands.Context, error: commands.CommandError):
        if isinstance(error, commands.CommandNotFound):
            message = "This commands doesn't exist."
        elif isinstance(error, commands.CommandOnCooldown):
            message = f"Please wait {round(error.retry_after, 1)}s"

        await ctx.send(message)


def setup(bot: commands.Bot):
    bot.add_cog(ErrorHandler(bot))
