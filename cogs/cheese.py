from discord.ext import commands


@commands.command()
async def otter(ctx: commands.Context):
	await ctx.send(f"{ctx.author.display_name} is NOT an otter!")


def setup(bot):
	bot.add_command(otter)