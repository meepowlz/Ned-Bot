from discord.ext import commands
import requests
import dotenv
import os

"""
Commands to quickly look up the definition of a word from Discord!
"""

dotenv.load_dotenv()


def search_word(query=None):
	if not query:
		query = input("Enter a word to look up: ")

	# Looks up the word
	search_request = requests.get(f"https://www.dictionaryapi.com/api/v3/references/collegiate/json/{query}?key={os.environ['MW_DICTIONARY']}")
	if 200 <= search_request.status_code < 300:
		results = search_request.json()
		# print(search_request.status_code)
		# print(results)
		if not results:
			print(f"No words were found which matched the search query '{query}'")
		else:
			words = format_results(results)
			display_results(words)
	else:
		print("Search failed")


def format_results(results):

	words = []
	for i, word in enumerate(results):
		terms = word['meta']['stems']
		hwi = word.get("hwi", {})
		prs = hwi.get("prs", [{}])[0]
		print(prs)
		pronunciation = prs.get("mw", )
		part_of_speech = word.get("fl")
		definitions = word.get("shortdef")
		print(definitions)
		word_data = {
			'terms': terms,
			'pronunciation': pronunciation,
			'part': part_of_speech,
			'def': definitions
		}
		print()
		#print(word_data)
		words.append(word_data)
	print(words)
	return words


def display_results(words):
	for word in words:
		print(word)


search_word()


@commands.command()
async def define(ctx: commands.Context, *, word: str):
	await ctx.send("learning english...")


def setup(bot):
	bot.add_command(define)

