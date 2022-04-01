import requests
import json

"""
MusicBrainz API root url
https://musicbrainz.org/ws/2/

Query parameter "?fmt=json"
"""

HONNE_MBID = "58b599cd-b1de-45e3-863a-3b54194a0f20"
NSWY_MBID = "Warm On A Cold Night"

artist_request = requests.get(f"https://musicbrainz.org/ws/2/artist/{HONNE_MBID}?inc=releases&fmt=json")
print(artist_request)

json_return = artist_request.json()
print(json_return)