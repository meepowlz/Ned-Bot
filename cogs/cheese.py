from discord.ext import commands

# Cheese stuff


class Cheese:

	def __init__(self, species: str, age: int, weight: float):
		self.species = species
		self.age = age
		self.weight = weight


mark = Cheese("Cheddar", 12, 14)


# Commands

@commands.command()
async def otter(ctx: commands.Context):
	await ctx.send(f"{ctx.author.display_name} is NOT an otter!")


@commands.command()
async def cheesetime(ctx: commands.Context):
	await ctx.send(f"{ctx.author.display_name}, it is ALWAYS cheese time.")


def setup(bot):
	bot.add_command(otter)
	bot.add_command(cheesetime)
