# Adds lyrics to a json file
# Randomly selects a lyric to display

import json
import random
from collections import deque


# Create deque for storing recent lyrics
lyrics_id_deque = deque([], 10)

# Opens json file to read
with open("lyrics.json", "r") as file:
    lyrics = json.load(file)


# Adds new lyrics to the file
def add_lyrics():
    while True:
        try:
            lyric = input("Enter song lyric: ")
            lyrics.append({"lyric": lyric})
        except KeyboardInterrupt:
            write_changes(lyrics)
            break
    add_ids()


# Updates lyric ids
def add_ids():
    for i, lyric in enumerate(lyrics):
        lyric["id"] = i
    write_changes(lyrics)


def check_deque(lyric):
    if lyric["id"] in lyrics_id_deque:
        return False
    else:
        return True


# Generates a random lyric
def random_lyric(lyrics_list):
    filtered_lyrics = list(filter(check_deque, lyrics_list))
    selected_lyric = random.choice(filtered_lyrics)
    print(selected_lyric["lyric"])
    lyrics_id_deque.append(selected_lyric["id"])
    return selected_lyric["lyric"]


# Writes any changes to the file
def write_changes(changes):
    # Open json file to write
    with open("lyrics.json", "w") as f:
        json.dump(changes, f, indent=4)
