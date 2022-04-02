import requests
import json
import time


"""
MusicBrainz API root url
https://musicbrainz.org/ws/2/

Query parameter "?fmt=json"
"""

selected = []

# Get artist data w/ releases
HONNE_MBID = "58b599cd-b1de-45e3-863a-3b54194a0f20"
artist_request = requests.get(f"https://musicbrainz.org/ws/2/artist/{HONNE_MBID}?inc=releases&fmt=json")
print(artist_request.status_code)
artist_json = artist_request.json()
#print(artist_json)


def create_newfile(filename):
    try:
        with open(f"{filename}.json", "r") as file:
            print(f"{file.name} was found!")
    except FileNotFoundError:
        with open(f"{filename}.json", "x") as file:
            print(f"{file.name} was created successfully!")
    return filename


def write_changes(filename, changes):
    with open(f"{filename}.json", "w") as file:
        json.dump(changes, file, indent=4)


def convert_length(milliseconds):
    seconds = int(milliseconds / 1000)
    minutes, seconds = divmod(seconds, 60)
    return f"{minutes}:{seconds:02}"


def traverse_tracks(tracks):
    for i, track in enumerate(tracks):
        # Print the track number, name and length
        # title, number, length, id, release date
        title = track['title']
        number = track['number']
        length = convert_length(tracks[i]['length'])
        id = track['recording']['id']
        release_date = track['recording']['first-release-date']
        print(f"{number}. {title} - {length}")


# Go through each release
def traverse_releases():
    for i, release in enumerate(artist_json["releases"]):
        # Print release title and MBID
        release_title = artist_json['releases'][i]['title']
        release_mbid = artist_json['releases'][i]['id']
        print(f"Release: {release_title}")
        print(f"MBID: {release_mbid}")

        # Pause so MB doesn't get upset
        time.sleep(1)

        # Gather tracks from each release
        release_request = requests.get(f"https://musicbrainz.org/ws/2/release/{release_mbid}?inc=recordings&fmt=json")
        # print(release_request.status_code)
        release_json = release_request.json()

        # Other information about the release
        print(f"Packaging: {release_json['packaging']}")
        print(f"Release Format: {release_json['media'][0]['format']}")
        tracks = release_json["media"][0]["tracks"]

        # Display tracks from release
        traverse_tracks(tracks)


        user_select = input("Select: 1-All tracks 2-Some tracks 3-No tracks")

        if user_select == "1":
            selected.append()
        print("")


def main():

    # Checks for or creates a data file
    filename = input("Enter the name of the file you wish to modify (ex. 'file.json'): ")
    create_newfile(filename)



main()