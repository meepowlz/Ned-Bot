import os

import discord
import dotenv
import requests
from discord.ext import commands

from .utils import paginator

"""
Commands to quickly look up the definition of a word
Paginates to show multiple definitions
Uses Merriam-Webster API
"""

dotenv.load_dotenv()


class SearchException(Exception):
	pass


def search_word(query):
	# Looks up the word
	search_request = requests.get(f"https://www.dictionaryapi.com/api/v3/references/collegiate/json/{query}?key={os.environ['MW_DICTIONARY']}")

	if 200 <= search_request.status_code < 300:
		results = search_request.json()
		if type(results[0]) is dict:
			# Formats if words are found
			return format_results(results)
		else:
			# Raises error if no words found
			raise SearchException(f"No words were found which matched the search query '{query}'")
	else:
		# Error if search failed
		raise SearchException("Search failed")


def format_results(results):
	"""
	Sorts API response data for use in embeds
	:param results: list
	:return: list
	"""
	words = []
	for i, word in enumerate(results):
		terms = word['meta']['stems']
		hwi = word.get("hwi", {})
		prs = hwi.get("prs", [{}])[0]
		pronunciation = prs.get("mw", )
		part_of_speech = word.get("fl")
		definitions = word.get("shortdef")
		word_data = {
			'terms': terms,
			'pronunciation': pronunciation,
			'part': part_of_speech,
			'def': definitions
		}
		words.append(word_data)
	return words


def display_results(words, base_embed):
	"""
	Creates embeds with each word
	:param words: list
	:param base_embed: discord.Embed
	:return: discord.Embed
	"""
	for i, word in enumerate(words):
		embed = base_embed.copy()
		terms = ", ".join(word['terms'])
		definitions = "\n\u2022 ".join(word['def'])
		definitions = "\u2022 " + definitions
		embed.title = f"Definition for \"{terms}\""
		embed.description = f"Pronounced: {word['pronunciation']}\n" \
			f"Part of speech: {word['part']}"
		embed.add_field(name="Definition", value=definitions)
		embed.set_footer(text=f"Definition #{i+1}")
		yield embed


@commands.command()
async def define(ctx: commands.Context, *, word: str):
	# Get words from API
	try:
		results = search_word(word)
	except SearchException as error:
		return await ctx.send(str(error))

	# Build embed
	base_embed = discord.Embed(color=ctx.author.color)
	base_embed.set_author(name=f"{ctx.author.display_name} searched for \"{word}\"", icon_url=ctx.author.avatar.url)
	embeds = list(display_results(results, base_embed))

	# Set view for pagination
	view = paginator.View(embeds)

	# Send embed to discord
	await ctx.send(embed=embeds[0], view=view)


async def setup(bot):
	bot.add_command(define)
