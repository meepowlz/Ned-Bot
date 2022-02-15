"""
API URL: https://api.listenbrainz.org
DOCS: https://listenbrainz.readthedocs.io/en/latest/users/api/#reference

GOAL: Display Gabi's top recordings
username: twitch0001
/1/user/username_here/listen-count
/1/stats/user/(user_name)/recordings
"""

import requests

response_listen_count = requests.get("https://api.listenbrainz.org/1/user/twitch0001/listen-count")
response_recordings = requests.get("https://api.listenbrainz.org/1/stats/user/twitch0001/recordings")

listencount = response_listen_count.json()

print(listencount["payload"]["count"])