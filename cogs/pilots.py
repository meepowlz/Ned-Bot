import discord
from discord.ext import commands, tasks

import lyrics

# A list of keywords for Ned to look for
EAST_LIST = ["whats up","what's up", "whats up?", "what's up?", "wassup", "wassup?"]


class Pilots(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.lyric_loop.start()

	@commands.command()
	async def lyric(self, ctx: commands.Context):
		lyric = lyrics.random_lyric(lyrics.lyrics)
		await ctx.send(lyric)

	@commands.command()
	@commands.is_owner()
	async def ned_hello(self, ctx: commands.Context):
		embed = discord.Embed(color=ctx.guild.me.color)
		embed.title = "Meet <@940021429414559784>! <a:nedvibe:970466324369260564>"
		embed.description = "**Ned is here to make Clique Gang unique!**\n" \
							"He has a variety of features to provide interactive & fun experiences here in our community!\n" \
							"Made by <@198536490672848896> with help from their lovely partner (heart emoji)"
		await ctx.send("hello", embed=embed)

	@tasks.loop(hours=4)
	async def lyric_loop(self):
		channel = self.bot.get_channel(self.bot.lyrics_channel_id)
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
