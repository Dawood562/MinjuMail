import os
import json


def add_vote(artist: str, gender: str, type: str):
    if os.path.isfile("suggestCards.json"):
        # Opens file and loads the data.
        with open("suggestCards.json", "r") as votes:
            data = json.load(votes)
        # Adds points if group already exists.
        try:
            data[f"{artist.upper()}"]["votes"] += 1
        # Creates a new group and adds points if group doesnt exist
        except KeyError:
            data[f"{artist.upper()}"] = {"artist":artist.upper(), "gender":gender, "atype":type, "votes": 1}
    else:
        data = {f"{artist}": {"points": 1}}
    # Saves file to store the data.
    with open("suggestCards.json", "w+") as votes:
        json.dump(data, votes, sort_keys=True, indent=4)


def get_votes(artist: str):
    with open("suggestCards.json", "r") as votes:
        data = json.load(votes)
    return data[f"{artist.upper()}"]["votes"]

def remove_artist(artist: str):
    if os.path.isfile("suggestCards.json"):
        # Opens file and loads the data.
        with open("suggestCards.json", "r") as votes:
            data = json.load(votes)
        try:
            for i in data:
                if data[i]["artist"].lower() == artist.lower():
                    # If found
                    data.pop(i)
                    print(data)
                    break
                else:
                    # If not found
                    pass
            json.dump(data, open("suggestCards.json", "w+"), indent=4)
        except KeyError:
            print(f"The group {artist} doesn't exist!")
        else:
            pass
