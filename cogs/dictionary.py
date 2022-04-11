from discord.ext import commands
import requests
import dotenv
import os

"""
Commands to quickly look up the definition of a word from Discord!
"""

dotenv.load_dotenv()

"""
query = input("word to search for pls")

search_request = requests.get(f"https://www.dictionaryapi.com/api/v3/references/collegiate/json/{query}?key={os.environ['MW_DICTIONARY']}")
print(search_request.status_code)
print(search_request)
results = search_request.json()
print(results)

for i, word in enumerate(results):
	terms = word['meta']['stems']
	pronunciation = word['hwi']['prs'][0]['mw']
	part_of_speech = word['fl']
	definitions = word['shortdef']

	print()
	print(terms, pronunciation, part_of_speech, definitions)
"""



@commands.command()
async def define(ctx: commands.Context, *, word: str):
	await ctx.send("learning english...")


def setup(bot):
	bot.add_command(define)

