from discord.ext import commands, tasks
import discord
import lyrics
from .utils import paginator


# A list of keywords for Ned to look for
EAST_LIST = ["whats up","what's up", "whats up?", "what's up?", "wassup", "wassup?"]


class Pilots(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		#self.lyric_loop.start()

	@commands.command()
	async def lyric(self, ctx: commands.Context):
		lyric = lyrics.random_lyric(lyrics.lyrics)
		await ctx.send(lyric)

	@commands.command()
	async def test(self, ctx: commands.Context):
		view = paginator.View()
		await ctx.send("stuff", view=view)

	@tasks.loop(hours=4)
	async def lyric_loop(self):
		channel = await self.bot.fetch_channel(893887834396712960)
		lyric = lyrics.random_lyric(lyrics.lyrics)
		await channel.send(lyric)

	@commands.Cog.listener()
	async def on_message(self, message: discord.Message):
		if message.content.lower() in EAST_LIST:
			await message.channel.send("East")
		elif message.content.lower() == "no":
			await message.channel.send("I move slow")
		if message.content.lower() == "cheese time":
			await message.channel.send(":cheese::timer:")


async def setup(bot):
	await bot.add_cog(Pilots(bot))
