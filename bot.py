from discord.ext import commands
import os
import dotenv
import discord

dotenv.load_dotenv()

intents = discord.Intents.all()
intents.members = False
intents.presences = False
bot = commands.Bot(command_prefix=os.environ["PREFIX"], intents=intents)


@bot.event
async def on_ready():
	await bot.load_extension("cogs.cheese")
	await bot.load_extension("cogs.dictionary")
	await bot.load_extension("cogs.pilots")
	await bot.load_extension("cogs.secret")
	await bot.load_extension("cogs.songvs")
	await bot.load_extension("jishaku")

try:
	bot.run(os.environ["TOKEN"])
except KeyboardInterrupt:
	bot.close()
