import requests
import json
import time

"""
MusicBrainz API root url
https://musicbrainz.org/ws/2/

Query parameter "?fmt=json"
"""

# Get artist data w/ releases
HONNE_MBID = "58b599cd-b1de-45e3-863a-3b54194a0f20"
artist_request = requests.get(f"https://musicbrainz.org/ws/2/artist/{HONNE_MBID}?inc=releases&fmt=json")
print(artist_request.status_code)
artist_json = artist_request.json()
#print(artist_json)


# Go through each release
for i, release in enumerate(artist_json["releases"]):
    # Print release data
    print(artist_json["releases"][i]["title"])
    release_mbid = artist_json['releases'][i]['id']
    print(f"MBID: {release_mbid}")

    # Pause so MB doesn't get upset
    time.sleep(1)

    # Gather tracks from each release
    release_request = requests.get(f"https://musicbrainz.org/ws/2/release/{release_mbid}?inc=recordings&fmt=json")
    print(release_request.status_code)
    release_json = release_request.json()

    #print(release_json)
    print(f"Packaging: {release_json['packaging']}")
    print(f"Release Format: {release_json['media'][0]['format']}")
    cheese = release_json["media"][0]["tracks"]
    for i, track in enumerate(cheese):
        print(f"{i}. {cheese[i]['title']}")
    print("")







# artist_request = requests.get(f"https://musicbrainz.org/ws/2/artist/{HONNE_MBID}?inc=releases&fmt=json")
# release_request = requests.get(f"https://musicbrainz.org/ws/2/release-group/{NSWY_MBID}?inc=releases&fmt=json")
# print(artist_request)
# print(release_request)
#
# artist_json = artist_request.json()
# release_json = release_request.json()
# print(artist_json)
# print(release_json)
#
# print(artist_json["release-groups"][0]["id"])
#
# # Retrieve all release groups
# for i, release in enumerate(artist_json["release-groups"]):
#     print(artist_json["release-groups"][i]["title"])
#     print(f"MBID: {artist_json['release-groups'][i]['id']}")
#     release_group_mbid = artist_json['release-groups'][i]['id']
#     time.sleep(1)
#     release_request = requests.get(f"https://musicbrainz.org/ws/2/release-group/{release_group_mbid}?inc=releases&fmt=json")
#     cheese = release_request.json()
#     print(cheese)
#

