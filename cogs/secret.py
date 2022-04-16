import datetime
import os
import random

import discord
import dotenv
import requests
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


def get_current_datetime():
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


def make_request(uid, embed):
	"""
	Requests service information
	Displays information in an embed
	:param uid: str
	:param embed: discord.Embed
	:return: discord.Embed
	"""
	# Get datetime for url
	c_datetime = get_current_datetime()
	url = f"https://api.rtt.io/api/v1/json/service/{uid}/{c_datetime['year']}/{c_datetime['month']}/{c_datetime['day']}"
	# Request service information
	request = requests.get(
		url,
		auth=(os.environ['RTT_USER'], os.environ['RTT_PASS'])
	)
	data = request.json()

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


@commands.command()
async def secret(ctx: commands.Context):
	# Displays embed with service information
	base_embed = discord.Embed(color=ctx.author.color)
	base_embed.set_author(name=f"{ctx.author.display_name} is gay", icon_url=ctx.author.avatar.url)
	embed = make_request(service_uid, base_embed)
	await ctx.send(embed=embed)


async def setup(bot):
	bot.add_command(secret)
