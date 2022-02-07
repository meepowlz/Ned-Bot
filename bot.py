from discord.ext import commands
import os
import dotenv
import discord

dotenv.load_dotenv()

intents = discord.Intents.all()
intents.members = False
intents.presences = False
bot = commands.Bot(command_prefix="+", intents=intents)


@bot.command()
async def cheeseyay(ctx: commands.Context, *, name: str = None):
	await ctx.send(f"yaycheese {ctx.author.nick} {name or ''}")


@bot.event
async def on_message(message: discord.Message):
	await bot.process_commands(message)
	if message.content == "what's up":
		await message.channel.send("east")


bot.run(os.environ["TOKEN"])
