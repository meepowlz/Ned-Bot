import asyncio
import datetime
import os
import random

import aiohttp
import discord
import dotenv
import requests
from bs4 import BeautifulSoup
from discord.ext import commands

dotenv.load_dotenv()

"""
API Information
train: 800008
https://www.realtimetrains.co.uk/about/developer/pull/docs/
api.rtt.io/api/v1/
"""

# Gay train service uid
service_uid = "L16286"


# https://beautiful-soup-4.readthedocs.io/en/latest/#searching-the-tree

train_headcode = 800320

"""
- Raise error if no uid found?
Should work consistently; determine if the UID shifts places at any point depending on the responses
headcodes
800008 (gay train)
390119 (full wrap train)
800320 (random train for testing)
"""


class ServiceException(Exception):
	pass


async def get_service_uid(headcode):
	"""
	Looks up train by headcode
	Parses the returned html to extract the current service uid
	Once UID is retrieved, service information is requested
	Otherwise, ServiceException raised
	:param headcode:
	:return:
	"""
	url=f"https://www.realtimetrains.co.uk/search/handler?qsearch={headcode}&type=detailed"
	# Get the html of resultant page after search
	async with aiohttp.ClientSession() as session:
		async with session.get(url) as response:
			r = await response.text()

		print(r)
		# Find service uid
		soup = BeautifulSoup(r, 'html.parser')
		li = soup.find_all("li")
		uid = -1
		for item in li:
			text = str(item)
			if "UID" in text:
				# print(text)
				uid_index = text.find("UID")
				uid = text[uid_index + 4:].split(",", 1)[0]
				print(f"UID: {uid}")
		if uid:
			return session, uid
		else:
			raise ServiceException(f"No service found associated with headcode {headcode}")


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


async def make_request(session, uid, embed):
	"""
	Requests service information
	Displays information in an embed
	:param uid: str
	:param embed: discord.Embed
	:return: discord.Embed
	"""
	# Get datetime for url
	c_datetime = await get_current_datetime()
	url = f"https://api.rtt.io/api/v1/json/service/{uid}/{c_datetime['year']}/{c_datetime['month']}/{c_datetime['day']}"
	# Request service information
	async with session.get(url, auth=aiohttp.BasicAuth(os.environ['RTT_USER'], os.environ['RTT_PASS'])) as response:
		data = await response.json()

	# Organize returned data
	operator = data['atocName']
	origin = data['origin'][0]
	destination = data['destination'][0]

	# Format information in an embed
	embed.title = f"{operator} - {uid}"
	embed.add_field(name="Departure",
					value=f"Departing {origin['description']} station\n"
						  f"Time: {origin['publicTime'][0:2]}:{origin['publicTime'][2:4]}")
	embed.add_field(name="Arrival",
					value=f"Arriving at {destination['description']} station\n"
						  f"Time: {destination['publicTime'][0:2]}:{destination['publicTime'][2:4]}")
	temp = random.randint(1, 3)  # Randomly select image to display
	embed.set_image(url=os.environ[f'SECRET_IMG_{temp}'])
	embed.timestamp = datetime.datetime.today()

	return embed

asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
asyncio.run(get_service_uid(train_headcode))



@commands.command()
async def secret(ctx: commands.Context, *, train_headcode: str):
	# Displays embed with service information
	session, uid = await get_service_uid(train_headcode)
	base_embed = discord.Embed(color=ctx.author.color)
	base_embed.set_author(name=f"{ctx.author.display_name} is gay", icon_url=ctx.author.avatar.url)
	embed = await make_request(session, uid, base_embed)
	await ctx.send(embed=embed)


async def setup(bot):
	bot.add_command(secret)

