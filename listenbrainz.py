"""
API URL: https://api.listenbrainz.org
DOCS: https://listenbrainz.readthedocs.io/en/latest/users/api/#reference

GOAL: Display Gabi's top recordings
username: twitch0001
/1/user/username_here/listen-count
/1/stats/user/(user_name)/recordings
"""

import requests


# Gets the response objects..?
response_listen_count = requests.get("https://api.listenbrainz.org/1/user/twitch0001/listen-count")
response_recordings = requests.get("https://api.listenbrainz.org/1/stats/user/twitch0001/recordings")
response_np = requests.get("https://api.listenbrainz.org/1/user/twitch0001/playing-now")
response_recent = requests.get("https://api.listenbrainz.org/1/users/twitch0001/recent-listens")

print(response_recent.status_code)

# Converts to json format
listen_count = response_listen_count.json()["payload"]["count"]
recordings = response_recordings.json()["payload"]["recordings"]
now_playing = response_np.json()["payload"]["listens"]
recent_listens = response_recent.json()["payload"]["listens"][0]["track_metadata"]

print(now_playing)
print(recent_listens)


def user_recent_activity():
    try:
        current = str(f"Now listening to: \"{now_playing['track_name']}\" by {now_playing['artist_name']} on {now_playing['listening_from']}")
    except TypeError:
        current = str("User is not listening to anything right now")
    try:
        recent = str(f"Recently played: \"{recent_listens['track_name']}\"")
    except TypeError:
        recent = str("No recent track data found")
    return current, recent


# Prints total listens and top songs
def user_stats():
    print(f"Total listens: {listen_count}")
    for i, recording in enumerate(recordings):
        print(f"{i}. \"{recording['track_name']}\" by {recording['artist_name']} on \"{recording['release_name']}\"")
        print(f"Listen count: {recording['listen_count']}")


user_recent_activity()
