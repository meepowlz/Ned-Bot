import asyncio
import datetime
import os
import platform
import random
import zoneinfo

import aiohttp
import discord
import dotenv
from bs4 import BeautifulSoup
from discord.ext import commands

dotenv.load_dotenv()

# Special images of identity 800008
PRIDE_IMGS = {1: "https://cdn.discordapp.com/attachments/557309470963924993/964945261937983548/PDTRBF_Pride.png",
			2: "https://cdn.discordapp.com/attachments/557309470963924993/964955998961954947/PDTRBF_Pride_kiss.png",
			3: "https://cdn.discordapp.com/attachments/557309470963924993/964958651834073168/PDTRBF_Pride_kissy.png"}


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
			async with session.get(api_url,
									auth=aiohttp.BasicAuth(os.environ['RTT_USER'], os.environ['RTT_PASS'])) as response:
				await response.json()
				# Find coach A image for embed display
				try:
					coach_img = str(soup.select('div[coach="A"]')[0].select('img'))
				except IndexError:
					coach_img = str(soup.select('div[coach="1"]')[0].select('img'))

				coach_img = coach_img[11:].split("\"")[0]
				coach_img = f"https://www.realtimetrains.co.uk{coach_img}"
				try:
					return search_url, uid, coach_img, await response.json()
				except Exception:
					raise ServiceException(
						f"**Identity {identity}** is scheduled for **Service {uid}**, but not currently running")
		else:
			raise ServiceException(f"No service found associated with **Identity {identity}**")


async def get_current_datetime():
	"""
	Gets current date & time, splits into usable format
	Used for making API requests
	:return: dict
	"""
	current_dt = str(datetime.datetime.now(tz=zoneinfo.ZoneInfo("Europe/London")))
	split_date = current_dt.split("-")
	split_datetime = {
		"year": split_date[0],
		"month": split_date[1],
		"day": split_date[2][0:2],
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
	print(data)
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
		rand = random.randint(1, 3)  # Randomly select image to display
		embed.set_image(url=PRIDE_IMGS[rand])
	else:
		embed.set_image(url=img)
	embed.set_footer(text=f"{operator} - Service {service_uid} for {identity}")
	embed.timestamp = datetime.datetime.now(tz=zoneinfo.ZoneInfo("Europe/London"))

	return embed


@commands.command()
async def rtt(ctx: commands.Context, *, identity: str):
	# Gathers data from requests
	try:
		url, uid, img, data = await get_service(identity)
		print(data)
	except ServiceException as error:
		return await ctx.send(str(error))

	# Builds embed
	base_embed = discord.Embed(color=ctx.author.color, url=url)
	if identity in {"800008", "390119"}:
		base_embed.set_author(name=f"{ctx.author.display_name} is gay!", icon_url=ctx.author.avatar.url)
	else:
		base_embed.set_author(name=f"{ctx.author.display_name} searched for identity {identity}",
							icon_url=ctx.author.avatar.url)
	embed = await build_embed(data, identity, img, base_embed)
	await ctx.send(embed=embed)


async def setup(bot):
	if platform.system() == "Windows":
		asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
	bot.add_command(rtt)
