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
	#try:
		search_request = requests.get(f"https://www.dictionaryapi.com/api/v3/references/collegiate/json/{query}?key={os.environ['MW_DICTIONARY']}")
		results = search_request.json()
		print(search_request.status_code)
		print(results)
		format_results(results)
		if not results:
			print(f"No words were found which matched the search query '{query}'")
	#except:
		# what error should this be?
		print("Search failed")


def format_results(results):

	words = []
	for i, word in enumerate(results):
		terms = word['meta']['stems']
		hwi = word.get("hwi", {})
		prs = hwi.get("prs", {})
		prs = prs.get(0, {})
		pronunciation = prs.get("mw")
		#pronunciation = word.get(['hwi']['prs'][0]['mw'])
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
		print(word_data)
		words.append(word_data)
	return words


search_word()


@commands.command()
async def define(ctx: commands.Context, *, word: str):
	await ctx.send("learning english...")


def setup(bot):
	bot.add_command(define)

