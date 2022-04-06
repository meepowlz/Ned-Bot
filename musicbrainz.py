import json
import os
import time

import requests

"""
MusicBrainz API root url
https://musicbrainz.org/ws/2/

Allows a user to search for an artist
and extract track data to a json file
"""


def create_newfile(filename):
    """
    Creates or opens file with the specified name
    :param filename: str
    :return: str
    """
    try:
        with open(f"data/{filename}.json", "r") as file:
            print(f"{file.name} was found!")
    except FileNotFoundError:
        with open(f"data/{filename}.json", "x") as file:
            print(f"{file.name} was created successfully!")
    return filename


def write_changes(filename, changes):
    """
    Updates file with the specified name
    :param filename: str
    :param changes: list
    :return: None
    """
    with open(f"data/{filename}.json", "w") as file:
        json.dump(changes, file, indent=4)


def convert_length(milliseconds=0):
    """
    Converts time from ms to minutes:seconds
    :param milliseconds: int
    :return: str
    """
    seconds = int(milliseconds / 1000)
    minutes, seconds = divmod(seconds, 60)
    return f"{minutes}:{seconds:02}"


def traverse_tracks(tracks, release, action, selected=None):
    """
    Separates release tracks
    Displays track information or
    returns list of selected tracks
    :param tracks: dict
    :param release: str
    :param action: str
    :param selected: int, list
    :return: None, list
    """
    return_tracks = []
    for i, track in enumerate(tracks):
        # Print the track number, name and length
        # title, number, length, id, release date
        title = track['title']
        position = track['number']
        length = convert_length(tracks[i]['length'])
        id = track['recording']['id']
        release_date = track['recording']['first-release-date']

        # Display or select track data
        if action == "display":
            print(f"{position}. {title} - {length}")
        elif action == "select":
            if isinstance(selected, list):
                if (i+1) not in selected:
                    continue
            return_tracks.append({
                "release": release,
                "title": title,
                "position": position,
                "length": length,
                "id": id,
                "release_date": release_date
            })
    return return_tracks


def traverse_releases(data, filename: str) -> None:
    """
    Goes through all artist releases
    Allows user to select what release tracks to save
    Calls write_changes() and saves selected tracks
    :param data: json
    :param filename: str
    """
    # Create list to store data to be added
    selected = []
    for i, release in enumerate(data['releases']):

        # Print release information
        release_title = data['releases'][i]['title']
        release_mbid = data['releases'][i]['id']
        print(f"Release: {release_title}")
        print(f"MBID: {release_mbid}")

        # Gather release tracks information
        time.sleep(1)
        release_request = requests.get(f"https://musicbrainz.org/ws/2/release/{release_mbid}?inc=recordings&fmt=json")
        release_json = release_request.json()

        # Other information about the release
        print(f"Packaging: {release_json['packaging']}")
        print(f"Release Format: {release_json['media'][0]['format']}")
        tracks = release_json['media'][0]['tracks']

        # Display tracks from release
        traverse_tracks(tracks, release_title, "display")

        # Select and save tracks to the json file
        try:
            user_select = int(input("Select: 0-All tracks 1-Some tracks 2-No tracks 3-Quit"))
        except (KeyboardInterrupt, ValueError):
            break
        if user_select == 0:
            selected.extend(traverse_tracks(tracks, release_title, "select", 0))
        elif user_select == 1:
            selections = input("Enter the track numbers to select, followed by spaces (ex. 1 2 3 11 12 13): ").split(" ")
            print(selections)
            selected.extend(traverse_tracks(tracks, release_title, "select", list(map(int, selections))))
        elif user_select == 2:
            print("No tracks selected. Continuing...")
        elif user_select == 3:
            print("Quitting...")
            break
        # Saves changes
        print()

    write_changes(filename, selected)


def search_artists():
    # Search for an artist
    artist_name = input("Enter an artist name to search for: ")
    artist_request = requests.get(
        f"https://musicbrainz.org/ws/2/artist/?query=sortname:{artist_name}&limit=10&fmt=json")
    print(artist_request.status_code)
    artist_json = artist_request.json()['artists']

    # Display all artists found
    for i, artist in enumerate(artist_json):
        print(f"{i + 1}. Artist: {artist['name']}")
        type = artist.get("type", "Unknown")
        print(f"Type: {type}")
        area = artist.get("area", {})
        area = area.get("name", "Unknown")
        print(f"Origin: {area}")
        print()

    # Select an artist to use
    artist_selected = int(input("Enter the artist number you would like to select: "))
    artist_selected = artist_json[(artist_selected - 1)]
    print(f"Artist {artist_selected['name']} was selected.")
    print(f"Looking up data for {artist_selected['name']}...")
    time.sleep(1)
    artist_request = requests.get(f"https://musicbrainz.org/ws/2/artist/{artist_selected['id']}?inc=releases&fmt=json")
    artist_json = artist_request.json()
    print(f"Data found!")
    print()

    return artist_json


def main():
    """
    Guides user through file modification process
    """
    while True:
        # Checks for or creates a data file
        filename = input("Enter the name of the json file you wish to modify: ")
        create_newfile(filename)

        # Begins file modification
        try:
            action = int(input("0-Add data to file 1-Clear file 2-Delete file"))
        except ValueError:
            print("Invalid selection. Aborting...")
            break
        if action == 0:
            artist_json = search_artists()
            traverse_releases(artist_json, filename)
        elif action == 1:
            confirm = input("Are you sure? This cannot be undone. Y/N: ")
            if confirm.lower() == "y":
                write_changes(filename, [])
                print(f"File {filename}.json was cleared!")
            else:
                print("Clearing file cancelled.")
        elif action == 2:
            confirm = input("Are you sure? This cannot be undone. Y/N: ")
            if confirm.lower() == "y":
                os.remove(f"{filename}.json")
                print(f"File {filename}.json was deleted!")
            else:
                print("Deleting file canceled.")


        print()
        action = input("Continue file modification? Y/N: ")
        if action.lower() == "y":
            continue
        else:
            break


main()

