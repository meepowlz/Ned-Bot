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
		pronunciation = word['hwi']['prs'][0]['mw']
		part_of_speech = word['fl']
		definitions = word['shortdef'][0]
		print(definitions)
		word_data = {
			'terms': terms,
			'prn' = pronun
		}
		"""
		word_data = {
			terms,
			pronunciation,
			part_of_speech,
			definitions
		}
		"""
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

