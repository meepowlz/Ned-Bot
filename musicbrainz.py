import requests
import json
import time

"""
MusicBrainz API root url
https://musicbrainz.org/ws/2/

Query parameter "?fmt=json"
"""

HONNE_MBID = "58b599cd-b1de-45e3-863a-3b54194a0f20"
NSWY_MBID = "874c3636-81db-468b-a0cb-a82ace2ab6af"

artist_request = requests.get(f"https://musicbrainz.org/ws/2/artist/{HONNE_MBID}?inc=release-groups&fmt=json")
release_request = requests.get(f"https://musicbrainz.org/ws/2/release-group/{NSWY_MBID}?inc=releases&fmt=json")
print(artist_request)
print(release_request)

artist_json = artist_request.json()
release_json = release_request.json()
print(artist_json)
print(release_json)

print(artist_json["release-groups"][0]["id"])

# Retrieve all release groups
for i, release in enumerate(artist_json["release-groups"]):
    print(artist_json["release-groups"][i]["title"])
    print(f"MBID: {artist_json['release-groups'][i]['id']}")
    release_group_mbid = artist_json['release-groups'][i]['id']
    time.sleep(1)
    release_request = requests.get(f"https://musicbrainz.org/ws/2/release-group/{release_group_mbid}?inc=releases&fmt=json")
    release_request.json()
    print(release_request)


