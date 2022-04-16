import discord
from discord.ext import commands
import requests
import datetime
import dotenv
import os

dotenv.load_dotenv()

#train: 800008
#https://www.realtimetrains.co.uk/about/developer/pull/docs/
#api.rtt.io/api/v1/

serviceUid = "L16286"


def get_current_datetime():
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


def make_request(serviceUid, embed):
	c_datetime = get_current_datetime()
	url = f"https://api.rtt.io/api/v1/json/service/{serviceUid}/{c_datetime['year']}/{c_datetime['month']}/{c_datetime['day']}"
	request = requests.get(
		url,
		auth=(os.environ['RTT_USER'], os.environ['RTT_PASS'])
	)
	data = request.json()
	operator = data['atocName']
	origin = data['origin'][0]
	destination = data['destination'][0]
	embed.title = f"{operator} - {serviceUid}"
	embed.add_field(name="Departure", value=f"Departing {origin['description']} station\nTime: {origin['publicTime'][0:2]}:{origin['publicTime'][2:4]}")
	embed.add_field(name="Arrival", value=f"Arriving at {destination['description']} station\nTime: {destination['publicTime'][0:2]}:{destination['publicTime'][2:4]}")
	embed.set_image(url="https://cdn.discordapp.com/attachments/557309470963924993/964945261937983548/PDTRBF_Pride.png")
	embed.timestamp = datetime.datetime.today()
	return embed


@commands.command()
async def secret(ctx: commands.Context):
	base_embed = discord.Embed(color=ctx.author.color)
	base_embed.set_author(name=f"{ctx.author.display_name} is gay", icon_url=ctx.author.avatar.url)
	embed = make_request(serviceUid, base_embed)
	await ctx.send(embed=embed)


async def setup(bot):
	bot.add_command(secret)
