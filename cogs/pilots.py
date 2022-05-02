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
		embed.title = "Meet <@Ned#8134>! <a:nedvibe:970466324369260564>"
		embed.description = "__*Ned is here to make Clique Gang unique!*__\n" \
			"He has a variety of features to provide interactive & fun experiences here in our community!\n" \
			"Made by <@198536490672848896> with help from their lovely partner :heart:"
		embed.add_field(name="Song vs. Song",
						value="- Sends a pair of Twenty One Pilots songs to <#Songvschannel>,\
							adding reactions for voting, and creating a thread for discussion\n"
							"- Vote for your favorite song and defend your position in the thread below!\n"
							"- Sends a new matchup every 24 hours",
						inline=False)
		embed.add_field(name="Lyric Feed",
						value="- Sends a random Twenty One Pilots lyric to <#Lyricschannel>\n"
							"- Continue the lyric chain with him!\n"
							"- Sends a new lyric every 4 hours",
						inline=False)
		embed.add_field(name="Auto Replies",
						value="- Talk in the server, and sometimes Ned will reply back :eyes:",
						inline=False)
		embed.add_field(name="Commands",
						value="Bored?\n"
								"+lyric to send a random Twenty One Pilots lyric\n"
								"+define \<term> to look up a word",
						inline=False)
		embed.add_field(name="If you have any questions or issues:",
						value="Message <@198536490672848896>!",
						inline=False)
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
