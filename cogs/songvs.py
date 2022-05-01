import os.path

from discord.ext import commands
import json
from collections import deque
import random
import time
from os import path

"""
Todo
fix file path stuff

Randomly selects two songs from datafile
Displays basic song information in an embed
Adds reactions for users to vote for their preferred song
Opens a thread for song discussion
"""

server_files = {521178844128870413: "top_data.json", 868961460607389778: "honne_data.json" }

recent_songs_deque = deque([], 10)

file_path = os.path.abspath(server_files[521178844128870413])
print(file_path)


def check_id(data):
    if data['id'] in recent_songs_deque:
        return False
    else:
        return True


def load_file(file_path=rf"{file_path}"):
    # loads file data
    with open(file_path, "r") as file:
        data = json.load(file)
    return data


def random_song(data):

    # filters out all recently used songs
    filtered_songs = list(filter(check_id, data))
    # randomly picks a song
    selected_song = random.choice(filtered_songs)
    # adds it to the recently used songs
    recent_songs_deque.append(selected_song['id'])


song_data = load_file()
random_song(song_data)
