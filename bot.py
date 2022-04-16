from discord.ext import commands, tasks
import os
import dotenv
import discord
import lyrics

dotenv.load_dotenv()

intents = discord.Intents.all()
intents.members = False
intents.presences = False
bot = commands.Bot(command_prefix=os.environ["PREFIX"], intents=intents)


@bot.event
async def on_ready():
	await bot.load_extension("cogs.cheese")
	await bot.load_extension("cogs.dictionary")
	await bot.load_extension("cogs.secret")
	#await bot.load_extension("jishaku")
	#lyric.start()


# A list of keywords for Ned to look for
east_list = ["whats up","what's up", "whats up?", "what's up?", "wassup", "wassup?"]


@bot.command()
async def cheeseyay(ctx: commands.Context, *, name: str = None):
	await ctx.send(f"yaycheese {ctx.author.nick} {name or ''}")


# @bot.command()
# async def gabiplaying(ctx: commands.Context):
# 	current, recent = listenbrainz.user_recent_activity()
# 	await ctx.send(current)
# 	await ctx.send(recent)


@bot.command()
async def lyric(ctx: commands.Context):
	lyric = lyrics.random_lyric(lyrics.lyrics)
	await ctx.send(lyric)


# @tasks.loop(hours=4)
# async def lyric():
# 	channel = await bot.fetch_channel(893887834396712960)
# 	lyric = lyrics.random_lyric(lyrics.lyrics)
# 	await channel.send(lyric)


@bot.event
async def on_message(message: discord.Message):
	await bot.process_commands(message)
	if message.content.lower() in east_list:
		await message.channel.send("East")
	elif message.content.lower() == "no":
		await message.channel.send("I move slow")
	if message.content.lower() == "cheese time":
		await message.channel.send(":cheese::timer:")


try:
	bot.run(os.environ["TOKEN"])
except KeyboardInterrupt:
	bot.close()
