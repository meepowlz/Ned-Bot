from discord.ext import commands
import asyncio

"""
Practice and implementation of various Python and Discord features to learn how things work
Commands are mostly for fun & serve limited use
"""

# Class stuff


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

# sally = Cheese("Sally", "Pecorino", 3, 35, 6)
# sally.slice_cheese(5)


# Inheritance with toast

# just makes a bread placeholder
main_bread = None


class Bread:

	def __init__(self, name, variety):
		self.name = name
		self.variety = variety

	def bread_info(self):
		return f"{self.name} is of variety {self.variety}"


class Toastable(Bread):

	def __init__(self, name="Bread", variety="White", is_toast_yet=False):
		super().__init__(name, variety)
		self.name = name
		self.variety = variety
		self.toast_status = is_toast_yet

	def toast_bread(self):
		if self.toast_status:
			return "Already toast"
		else:
			self.toast_status = True
			return "Toasted!"


# Commands


@commands.command()
async def bread(ctx: commands.Context):
	global main_bread
	main_bread = Toastable()
	await ctx.send(f"{ctx.author.display_name} just made bread")


@commands.command()
async def toast(ctx: commands.Context):
	global main_bread
	if main_bread:
		toasted = main_bread.toast_bread()
		await ctx.send(toasted)
	else:
		await ctx.send("Bread doesn't exist yet, silly goose")


@commands.command()
async def otter(ctx: commands.Context):
	await ctx.send(f"{ctx.author.display_name} is NOT an otter!")


@commands.command()
async def cheesetime(ctx: commands.Context):
	await ctx.send(f"{ctx.author.display_name}, it is ALWAYS cheese time.")


@commands.command()
async def cheeseyay(ctx: commands.Context, *, name: str = None):
	await ctx.send(f"yaycheese {ctx.author.nick} {name or ''}")


@commands.command()
@commands.is_owner()
async def del_all(ctx: commands.Context):
	async for message in ctx.channel.history(limit=200):
		await message.delete()
		await asyncio.sleep(0.25)


async def setup(bot):
	bot.add_command(bread)
	bot.add_command(toast)
	bot.add_command(otter)
	bot.add_command(cheesetime)
	bot.add_command(cheeseyay)
