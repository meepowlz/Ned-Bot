from discord.ext import commands
import os
import dotenv
import discord

dotenv.load_dotenv()

intents = discord.Intents.all()
intents.members = False
intents.presences = False

bot = commands.Bot(command_prefix=os.environ["PREFIX"], intents=intents)
bot.lyrics_channel_id = int(os.environ["LYRICS_CHANNEL_ID"])
bot.songvs_channel_id = int(os.environ["SONGVS_CHANNEL_ID"])


@bot.event
async def on_ready():
	await bot.load_extension("jishaku")
	await bot.load_extension("cogs.cheese")
	await bot.load_extension("cogs.dictionary")
	await bot.load_extension("cogs.pilots")
	await bot.load_extension("cogs.rtt")
	await bot.load_extension("cogs.songvs")

try:
	bot.run(os.environ["TOKEN"])
except KeyboardInterrupt:
	bot.close()
