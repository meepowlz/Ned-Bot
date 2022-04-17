from discord.ext import commands
import requests
import dotenv
import os
import discord

"""
Commands to quickly look up the definition of a word from Discord!
"""

dotenv.load_dotenv()


def search_word(query):
	# Looks up the word
	search_request = requests.get(f"https://www.dictionaryapi.com/api/v3/references/collegiate/json/{query}?key={os.environ['MW_DICTIONARY']}")
	if 200 <= search_request.status_code < 300:
		results = search_request.json()
		if not results:
			return f"No words were found which matched the search query '{query}'"
		else:
			return format_results(results)
	else:
		return "Search failed"


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
	for word in words:
		embed = base_embed.copy()
		terms = ", ".join(word['terms'])
		definitions = "\n\u2022 ".join(word['def'])
		definitions = "\u2022 " + definitions
		embed.title = f"Definition for \"{terms}\""
		embed.description = f"Pronounced: {word['pronunciation']}\n" \
							f"Part of speech: {word['part']}"
		embed.add_field(name="Definition", value=definitions)
		yield embed


@commands.command()
async def define(ctx: commands.Context, *, word: str):
	await ctx.send("learning english...")
	results = search_word(word)
	base_embed = discord.Embed(color=ctx.author.color)
	base_embed.set_author(name=f"{ctx.author.display_name} searched for \"{word}\"", icon_url=ctx.author.avatar.url)
	embeds = list(display_results(results, base_embed))
	view = discord.ui.View()
	previous_btn = discord.ui.Button(label="Previous")
	next_btn = discord.ui.Button(label="Next")
	view.add_item(previous_btn)
	view.add_item(next_btn)
	await ctx.send(embed=embeds[0], view=view)


async def setup(bot):
	bot.add_command(define)

