from discord.ext import commands
import json
from collections import deque
import random
import time

"""
Todo
fix file path stuff

Randomly selects two songs from datafile
Displays basic song information in an embed
Adds reactions for users to vote for their preferred song
Opens a thread for song discussion
"""

recent_songs_deque = deque([], 10)


def check_id(id):
    if id in recent_songs_deque:
        print("Found in deque")
        return False
    else:
        # print("Not in deque")
        return True


def random_song():
    with open("honne_data.json", "r") as file:
        songs = json.load(file)

    while True:
        filtered_songs = list(filter(check_id, songs))
        selected_song = random.choice(filtered_songs)
        print(selected_song['title'])
        recent_songs_deque.append(selected_song['id'])
        time.sleep(1)

    # for i, song in enumerate(songs):
    #     print(song['id'])




"""
def random_lyric(lyrics_list):
    filtered_lyrics = list(filter(check_deque, lyrics_list))
    selected_lyric = random.choice(filtered_lyrics)
    print(selected_lyric["lyric"])
    lyrics_id_deque.append(selected_lyric["id"])
    return selected_lyric["lyric"]
"""


random_song()