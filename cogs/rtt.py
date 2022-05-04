import asyncio
from datetime import datetime, timezone, timedelta
import os
import random
import platform

import aiohttp
import discord
import dotenv
from bs4 import BeautifulSoup
from discord.ext import commands

dotenv.load_dotenv()


"""
800008 (gay train)
390119 (full wrap train)
800320 (random train for testing)
"""


class ServiceException(Exception):
	pass


class SearchException(Exception):
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
	search_url = f"https://www.realtimetrains.co.uk/search/handler?qsearch={identity}&type=detailed"
	# Get the html of resultant page after search

	async with aiohttp.ClientSession() as session:
		async with session.get(search_url) as response:
			r = await response.text()

		# Find service UID
		soup = BeautifulSoup(r, 'html.parser')
		li = soup.find_all('li')
		uid = None
		for item in li:
			text = str(item)
			if "UID" in text:
				uid_index = text.find("UID")
				uid = text[uid_index + 4:].split(",", 1)[0]

		# Use UID for lookup
		if uid:
			c_datetime = await get_current_datetime()
			api_url = f"https://api.rtt.io/api/v1/json/service/{uid}/{c_datetime['year']}/{c_datetime['month']}/{c_datetime['day']}"
			# Request service information
			async with session.get(api_url, auth=aiohttp.BasicAuth(os.environ['RTT_USER'], os.environ['RTT_PASS'])) as response:
				# Find coach A image for embed display
				coach_img = str(soup.select('div[coach="A"]')[0].select('img'))
				coach_img = coach_img[11:].split("\"")[0]
				coach_img = f"https://www.realtimetrains.co.uk{coach_img}"
				return search_url, uid, coach_img, await response.json()
		else:
			raise ServiceException(f"No service found associated with identity {identity}")


async def get_current_datetime():
	"""
	Gets current date & time, splits into usable format
	:return: dict
	"""
	timedelta = datetime.timedelta()
	timezone = datetime.timezone(timedelta)
	current_datetime = str(datetime.now(timezone.utc))
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


async def build_embed(data, identity, img, embed):
	"""
	Requests service information
	Displays information in an embed
	:param data: dict
	:param identity: str
	:param img: str
	:param embed: discord.Embed
	:return: discord.Embed
	"""
	# Organize returned data
	operator = data['atocName']
	service_uid = data['serviceUid']
	is_passenger = data['isPassenger']
	origin = data['origin'][0]
	destination = data['destination'][0]
	depart_time = origin.get('publicTime', origin['workingTime'])
	arrive_time = destination.get('publicTime', destination['workingTime'])

	# Format information in an embed
	embed.title = f"{operator} {service_uid} - {origin['tiploc']} to {destination['tiploc']}"

	embed.description = f"**Passenger-carrying service**: {is_passenger}"
	embed.add_field(name="Departure",
					value=f"Departing {origin['description']} station\n"
						  f"Time: {depart_time[0:2]}:{depart_time[2:4]}")
	embed.add_field(name="Arrival",
					value=f"Arriving at {destination['description']} station\n"
						  f"Time: {arrive_time[0:2]}:{arrive_time[2:4]}")
	if identity == "800008":
		temp = random.randint(1, 3)  # Randomly select image to display
		embed.set_image(url=os.environ[f'SECRET_IMG_{temp}'])
	else:
		embed.set_image(url=img)
	embed.set_footer(text=f"{operator} - Service {service_uid} for {identity}")
	embed.timestamp = datetime.utcnow()

	return embed


@commands.command()
async def rtt(ctx: commands.Context, *, identity: str):
	# Displays embed with service information
	try:
		url, uid, img, data = await get_service(identity)
	except ServiceException as error:
		return await ctx.send(str(error))
	base_embed = discord.Embed(color=ctx.author.color, url=url)
	base_embed.set_author(name=f"{ctx.author.display_name} searched for identity {identity}",
						icon_url=ctx.author.avatar.url)
	embed = await build_embed(data, identity, img, base_embed)
	await ctx.send(embed=embed)


async def setup(bot):
	if platform.system() == "Windows":
		asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
	bot.add_command(rtt)
