import json
import random
from collections import deque, defaultdict
from pathlib import Path
import datetime

import discord
from discord.ext import commands, tasks

"""
Randomly selects two songs from datafile
Displays basic song information in an embed
Adds reactions for users to vote for their preferred song
Opens a thread for song discussion
"""

server_files = {521178844128870413: "top_data.json", 868961460607389778: "honne_data.json"}
SONGVS_TIME = datetime.time(hour=12)


class Songvs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.deques = defaultdict(deque)
        self.songvs_loop.start()

    def check_id(self, data, guild):
        # Creates song deque for each server
        if data['id'] in self.deques[guild]:
            return False
        else:
            return True

    def load_file(self, file_path):
        # Loads file data
        with open(file_path, "r") as file:
            data = json.load(file)
        return data

    def random_song(self, data, guild):
        # Filters out all recently used songs
        filtered_songs = list(filter(lambda d: self.check_id(d, guild), data))
        # Randomly picks a song
        selected_song = random.choice(filtered_songs)
        # Adds it to the recently used songs
        self.deques[guild].append(selected_song['id'])

        return selected_song

    def build_embed(self, embed, song, num):
        """
        Develops embed with song information
        :param embed: discord.Embed
        :param song: dict
        :return: discord.Embed
        """
        embed.add_field(name=f"{num}\N{COMBINING ENCLOSING KEYCAP} {song['title']}",
                        value=f"Album: {song['release']}\n"
                              f"Length: {song['length']}\n"
                              f"Released on: {song['release_date']}")
        return embed

    async def create_matchup(self, channel, guild, color=None):
        """
        Sends Song vs. Song embed with random song matchups
        Attaches reactions and thread for discussion
        :param channel: ctx.Channel
        :param guild: ctx.Guild
        :param color: ctx.author.color
        :return: None
        """
        # Opens song data
        file_path = Path(f"data/{server_files[guild.id]}")
        data = self.load_file(file_path)

        # Randomly selects songs
        song_1 = self.random_song(data, guild)
        song_2 = self.random_song(data, guild)

        # Builds an embed with song data
        base_embed = discord.Embed(color=color or guild.me.color)
        base_embed.title = f"\"{song_1['title']}\" vs. \"{song_2['title']}\""
        embed = self.build_embed(base_embed, song_1, 1)
        embed = self.build_embed(embed, song_2, 2)

        # Sends embed, attaches reactions & creates thread
        message = await channel.send(embed=embed)
        await message.add_reaction("1\N{COMBINING ENCLOSING KEYCAP}")
        await message.add_reaction("2\N{COMBINING ENCLOSING KEYCAP}")
        await message.create_thread(name=f"\"{song_1['title']}\" vs. \"{song_2['title']}\"")

    @commands.command()
    @commands.is_owner()
    async def songvs(self, ctx: commands.Context):
        # Command version of Song vs. Song
        await self.create_matchup(ctx.channel, ctx.guild, ctx.author.color)

    @tasks.loop(time=SONGVS_TIME)
    async def songvs_loop(self):
        # Loop version of Song vs. Song
        channel = self.bot.get_channel(self.bot.songvs_channel_id)
        await self.create_matchup(channel, channel.guild)


async def setup(bot):
    await bot.add_cog(Songvs(bot))
