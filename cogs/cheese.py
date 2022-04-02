from discord.ext import commands

# Cheese stuff


class Cheese:

	def __init__(self, name: str, species: str, age: int, weight: float, moldy_after: int):
		"""
		A class for making new cheeses
		species: the name of the cheese (ex. cheddar)
		age: # of months aged
		weight: in oz
		moldy_after: expiration in months
		"""
		self.name = name
		self.species = species
		self.age = age
		self.weight = float(round(weight, 2))
		self.moldy_after = moldy_after

	def age_cheese(self, months):
		print(f"{self.name} was {self.age} months old")
		print(f"{self.name} is being aged {months} months")
		self.age += months
		print(f"{self.name} is now {self.age} months old")

	def slice_cheese(self, times):
		print(f"{self.name} was {self.weight} oz")
		self.weight = round((self.weight / times), 2)
		print(f"{self.name} was cut {times} times")
		print(f"{self.name} is now {self.weight} oz")

	def check_moldy(self):
		if self.age > self.moldy_after:
			print(f"{self.name} is moldy :(")
		else:
			print("No mold!")


# mark = Cheese("Mark", "Cheddar", 12, 15, 14)
# mark.age_cheese(3)
# mark.slice_cheese(3)
# mark.check_moldy()

sally = Cheese("Sally", "Pecorino", 3, 35, 6)
sally.slice_cheese(5)


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
