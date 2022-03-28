import requests
import json

"""
MusicBrainz API root url
https://musicbrainz.org/ws/2/

Query parameter "?fmt=json"
"""

ARTIST = "HONNE"
ALBUM = "Warm On A Cold Night"

album_request = requests.get(f"https://musicbrainz.org/ws/2/artist?query={ARTIST}&limit=<LIMIT>&offset=<OFFSET>?fmt=json")
print(album_request)

json_return = album_request.json()
print(json_return)