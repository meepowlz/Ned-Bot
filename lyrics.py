# Adds lyrics to a json file
# Randomly selects a lyric to display

import json


lyrics = []

lyrics.append({})

# Open json file
with open("lyrics.json", "w") as file:
    json.dumps(lyrics)