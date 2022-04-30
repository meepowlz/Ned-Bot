from discord.ext import commands, tasks
import discord
import lyrics


# A list of keywords for Ned to look for
east_list = ["whats up","what's up", "whats up?", "what's up?", "wassup", "wassup?"]


@commands.command()
async def lyric(ctx: commands.Context):
	lyric = lyrics.random_lyric(lyrics.lyrics)
	await ctx.send(lyric)


@tasks.loop(hours=4)
async def lyric_loop():
	channel = await bot.fetch_channel(893887834396712960)
	lyric = lyrics.random_lyric(lyrics.lyrics)
	await channel.send(lyric)


@bot.event
async def on_message(message: discord.Message):
	await bot.process_commands(message)
	if message.content.lower() in east_list:
		await message.channel.send("East")
	elif message.content.lower() == "no":
		await message.channel.send("I move slow")
	if message.content.lower() == "cheese time":
		await message.channel.send(":cheese::timer:")


async def setup(bot):
	bot.add_command(lyric)
	lyric_loop.start()
