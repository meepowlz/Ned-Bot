import asyncio
import datetime
import os
import random
import platform

import aiohttp
import discord
import dotenv
from bs4 import BeautifulSoup
from discord.ext import commands

dotenv.load_dotenv()

# https://beautiful-soup-4.readthedocs.io/en/latest/#searching-the-tree

"""
- Raise error if no uid found?
Should work consistently; determine if the UID shifts places at any point depending on the responses
identities
800008 (gay train)
390119 (full wrap train)
800320 (random train for testing)
"""


class ServiceException(Exception):
	pass


async def get_service(identity):
	"""
	Looks up train by identity
	Parses the returned html to extract the current service UID
	Once UID is retrieved, service information is requested
	If no UID found, ServiceException is raised
	:param identity: str
	:return: str, json
	"""
	url=f"https://www.realtimetrains.co.uk/search/handler?qsearch={identity}&type=detailed"
	# Get the html of resultant page after search
	async with aiohttp.ClientSession() as session:
		async with session.get(url) as response:
			r = await response.text()

		# Find service uid
		soup = BeautifulSoup(r, 'html.parser')
		li = soup.find_all("li")
		uid = None
		for item in li:
			text = str(item)
			if "UID" in text:
				# print(text)
				uid_index = text.find("UID")
				uid = text[uid_index + 4:].split(",", 1)[0]
				print(f"UID: {uid}")

		if uid:
			c_datetime = await get_current_datetime()
			url = f"https://api.rtt.io/api/v1/json/service/{uid}/{c_datetime['year']}/{c_datetime['month']}/{c_datetime['day']}"
			# Request service information
			async with session.get(url, auth=aiohttp.BasicAuth(os.environ['RTT_USER'], os.environ['RTT_PASS'])) as response:
				return uid, await response.json()
		else:
			print("OBJECTION")
			raise ServiceException(f"No service found associated with identity {identity}")


async def get_current_datetime():
	"""
	Gets current date & time, splits into usable format
	:return: dict
	"""
	current_datetime = str(datetime.datetime.today())
	split_date = current_datetime.split("-")
	split_time = split_date[2][3:len(split_date[2])].split(":")
	split_datetime = {
		"year": split_date[0],
		"month": split_date[1],
		"day": split_date[2][0:2],
		"hour": split_time[0],
		"min": split_time[1],
		"sec": split_time[2][0:2],
		"ms": split_time[2][3:len(split_time[2])]
	}
	return split_datetime


async def build_embed(ctx, data, identity, uid, embed):
	"""
	Requests service information
	Displays information in an embed
	:param uid: str
	:param embed: discord.Embed
	:return: discord.Embed
	"""
	# Organize returned data
	operator = data['atocName']
	service_uid = data['serviceUid']
	origin = data['origin'][0]
	destination = data['destination'][0]
	depart_time = origin.get('publicTime', origin['workingTime'])
	arrive_time = destination.get('publicTime', destination['workingTime'])
	await ctx.send(origin)

	# Format information in an embed
	embed.title = f"{operator} - Service UID {service_uid}"
	embed.add_field(name="Departure",
					value=f"Departing {origin['description']} station\n"
						  f"Time: {depart_time[0:2]}:{depart_time[2:4]}")
	embed.add_field(name="Arrival",
					value=f"Arriving at {destination['description']} station\n"
						  f"Time: {arrive_time[0:2]}:{arrive_time[2:4]}")
	if identity == "800008":
		temp = random.randint(1, 3)  # Randomly select image to display
		embed.set_image(url=os.environ[f'SECRET_IMG_{temp}'])
	embed.timestamp = datetime.datetime.today()

	return embed


@commands.command()
async def secret(ctx: commands.Context, *, identity: str):
	# Displays embed with service information
	try:
		uid, data = await get_service(identity)
		await ctx.send(uid)
		await ctx.send(data)
	except ServiceException as error:
		return await ctx.send(str(error))
	base_embed = discord.Embed(color=ctx.author.color)
	base_embed.set_author(name=f"{ctx.author.display_name}", icon_url=ctx.author.avatar.url)
	embed = await build_embed(ctx, data, identity, uid, base_embed)
	await ctx.send(embed=embed)


async def setup(bot):
	if platform.system() == "Windows":
		asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
	bot.add_command(secret)

