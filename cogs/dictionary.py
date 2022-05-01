from discord.ext import commands
import requests
import dotenv
import os
import discord
from .utils import paginator


"""
Commands to quickly look up the definition of a word from Discord!
"""

dotenv.load_dotenv()


class SearchException(Exception):
	pass


def search_word(query):
	# Looks up the word
	search_request = requests.get(f"https://www.dictionaryapi.com/api/v3/references/collegiate/json/{query}?key={os.environ['MW_DICTIONARY']}")
	if 200 <= search_request.status_code < 300:
		results = search_request.json()
		if not results:
			raise SearchException(f"No words were found which matched the search query '{query}'")
		else:
			return format_results(results)
	else:
		raise SearchException("Search failed")


def format_results(results):

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
	for i, word in enumerate(words):
		embed = base_embed.copy()
		print("Word: ", word)
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
	# get words
	try:
		results = search_word(word)
	except SearchException as error:
		return await ctx.send(str(error))

	# embed stuff
	base_embed = discord.Embed(color=ctx.author.color)
	base_embed.set_author(name=f"{ctx.author.display_name} searched for \"{word}\"", icon_url=ctx.author.avatar.url)
	embeds = list(display_results(results, base_embed))

	# view stuff
	view = paginator.View(embeds)

	# display embed
	await ctx.send(embed=embeds[0], view=view)


async def setup(bot):
	bot.add_command(define)
