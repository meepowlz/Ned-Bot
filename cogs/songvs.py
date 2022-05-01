import json
import os.path
import random
from collections import deque

import discord
from discord.ext import commands

"""
Randomly selects two songs from datafile
Displays basic song information in an embed
Adds reactions for users to vote for their preferred song
Opens a thread for song discussion

issue - fix pathing somehow so it can be dynamic
"""

server_files = {521178844128870413: "top_data.json", 868961460607389778: "honne_data.json"}
root = r"C:\Users\Meep\PycharmProjects\Ned-Bot"
recent_songs_deque = deque([], 20)


class Songvs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def check_id(self, data):
        if data['id'] in recent_songs_deque:
            return False
        else:
            return True

    # https://stackoverflow.com/questions/1724693/find-a-file-in-python
    def find(self, name, path):
        for root, dirs, files in os.walk(path):
            if name in files:
                return os.path.join(root, name)

    def load_file(self, file_path):
        # loads file data
        with open(file_path, "r") as file:
            data = json.load(file)
        return data

    def random_song(self, data):
        # filters out all recently used songs
        filtered_songs = list(filter(self.check_id, data))
        # randomly picks a song
        selected_song = random.choice(filtered_songs)
        # adds it to the recently used songs
        recent_songs_deque.append(selected_song['id'])

        return selected_song

    def build_embed(self, embed, song):
        embed.add_field(name=song['title'],
                        value=f"Album: {song['release']}\n"
                              f"Length: {song['length']}\n"
                              f"Released on: {song['release_date']}")
        return embed

    @commands.command()
    async def songvs(self, ctx: commands.Context):
        file_path = self.find(server_files[ctx.guild.id], root)
        data = self.load_file(file_path)
        song_1 = self.random_song(data)
        song_2 = self.random_song(data)
        base_embed = discord.Embed(color=ctx.author.color)
        base_embed.title = f"\"{song_1['title']}\" vs. \"{song_2['title']}\""
        embed = self.build_embed(base_embed, song_1)
        embed = self.build_embed(embed, song_2)
        message = await ctx.send(embed=embed)
        await message.add_reaction("<:ottershy:896849222459064320>")
        await message.add_reaction("<:foreheadkiss:945336297826975835>")


async def setup(bot):
    await bot.add_cog(Songvs(bot))
