import discord
from discord.ext import commands, tasks
import datetime

import lyrics

# A list of keywords for Ned to look for
EAST_LIST = ["whats up", "what's up", "whats up?", "what's up?", "wassup", "wassup?"]
CLIQUE_GANG_GUILD_ID = 521178844128870413
LOOP_TIMES = [datetime.time(hour=6), datetime.time(hour=12), datetime.time(hour=18), datetime.time(hour=24)]


class Pilots(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.lyric_loop.start()

	@commands.command()
	async def lyric(self, ctx: commands.Context):
		# Sends a random lyric
		lyric = lyrics.random_lyric(lyrics.lyrics)
		await ctx.send(lyric)

	@commands.command()
	@commands.is_owner()
	async def ned_hello(self, ctx: commands.Context):
		"""
		Displays informational embed overviewing all of Ned's features
		:param ctx: commands.Context
		:return: None
		"""
		embed = discord.Embed(color=ctx.guild.me.color)
		embed.title = "Meet Ned! <a:nedvibe:970466324369260564>"
		embed.set_author(name=f"{ctx.guild.me.display_name}", icon_url=ctx.guild.me.avatar.url)
		embed.description = "__*<@940021429414559784> is here to make Clique Gang unique!*__\n" \
			"He has a variety of features to provide interactive & fun experiences here in our community!\n" \
			"Made by <@198536490672848896> with help from their lovely partner :heart:"
		embed.add_field(name="Song vs. Song",
						value=f"- Sends a pair of Twenty One Pilots songs to <#{self.bot.songvs_channel_id}>,\
							adding reactions for voting, and creating a thread for discussion\n"
							"- Vote for your favorite song and defend your position in the thread below!\n"
							"- Sends a new matchup every 24 hours",
						inline=False)
		embed.add_field(name="Lyric Feed",
						value=f"- Sends a random Twenty One Pilots lyric to <#{self.bot.lyrics_channel_id}>\n"
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
		await ctx.send("@everyone", embed=embed)

	@commands.command()
	async def channel_explain(self, ctx: commands.Context):
		"""
		Explains the purpose of Song vs. Song and Lyric channels
		:param ctx: commands.Context
		:return: None
		"""
		if ctx.channel.id == 830946358981689405:
			title = "Song vs. Song"
			description = f"- Sends a pair of Twenty One Pilots songs to <#{self.bot.songvs_channel_id}>," \
				f" adding reactions for voting, and creating a thread for discussion\n" \
				f"- Vote for your favorite song and defend your position in the thread below!\n" \
				f"- Sends a new matchup every 24 hours"
		elif ctx.channel.id == 943596688931713075:
			title = "Lyric Feed"
			description = f"- Sends a random Twenty One Pilots lyric to <#{self.bot.lyrics_channel_id}>\n" \
				f"- Continue the lyric chain with him!\n" \
				f"- Sends a new lyric every 4 hours"
		else:
			await ctx.send("Must be in correct channel to use")
			return
		embed = discord.Embed(color=ctx.guild.me.color)
		embed.title = f"{title} <a:nedvibe:970466324369260564>"
		embed.set_author(name=f"{ctx.guild.me.display_name}", icon_url=ctx.guild.me.avatar.url)
		embed.description = description
		embed.add_field(name="If you have any questions or issues:",
						value="Message <@198536490672848896>!",
						inline=False)
		await ctx.send(embed=embed)

	@tasks.loop(time=LOOP_TIMES)
	async def lyric_loop(self):
		# Sends a random song lyric every 4 hours
		channel = self.bot.get_channel(self.bot.lyrics_channel_id)
		lyric = lyrics.random_lyric(lyrics.lyrics)
		await channel.send(lyric)

	@commands.Cog.listener()
	async def on_message(self, message: discord.Message):
		# Checks if a user says a keyword to reply to
		if message.guild.id == CLIQUE_GANG_GUILD_ID:
			if message.content.lower() in EAST_LIST:
				await message.channel.send("East")
			elif message.content.lower() == "no":
				await message.channel.send("I move slow")
			if message.content.lower() == "cheese time":
				await message.channel.send(":cheese::timer:")


async def setup(bot):
	await bot.add_cog(Pilots(bot))
