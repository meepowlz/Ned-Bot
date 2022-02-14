# Adds lyrics to a json file
# Randomly selects a lyric to display

import json

# Opens json file to read
with open("lyrics.json", "r") as file:
    lyrics = json.load(file)


def add_lyrics():
    while True:
        try:
            lyric = input("Enter song lyric: ")
            lyrics.append({"lyric": lyric})
        except KeyboardInterrupt:
            write_changes(lyrics)
            break
    add_ids()

def add_ids():
    for i, lyric in enumerate(lyrics):
        lyric["id"] = i
    write_changes(lyrics)


def write_changes(changes):
    # Open json file to write
    with open("lyrics.json", "w") as file:
        json.dump(changes, file, indent=4)


add_lyrics()