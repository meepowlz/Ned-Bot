from discord.ext import commands, tasks
import os
import dotenv
import discord
import lyrics

dotenv.load_dotenv()

intents = discord.Intents.all()
intents.members = False
intents.presences = False
bot = commands.Bot(command_prefix="+", intents=intents)


@bot.command()
async def cheeseyay(ctx: commands.Context, *, name: str = None):
	await ctx.send(f"yaycheese {ctx.author.nick} {name or ''}")


@bot.command()
async def lyric(ctx: commands.Context):
	lyric = lyrics.random_lyric(lyrics.lyrics)
	await ctx.send(lyric)


@bot.event
async def on_message(message: discord.Message):
	await bot.process_commands(message)
	if message.content == "what's up":
		await message.channel.send("east")


try:
	bot.run(os.environ["TOKEN"])
except KeyboardInterrupt:
	bot.close()
