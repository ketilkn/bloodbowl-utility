#!/usr/bin/env python3
""" Python libraries for Dr.Tide"""
import sys
import os
import os.path
import collections
import logging
import json
import player.load


def load_fromjson(path="input/json/players.json"):
    with open(path, "r") as infile:
        return json.load(infile)



def dict_players():
    if os.path.isfile("input/json/players.json"):
        return load_fromjson()
    players = {}
    for p in list(player.load.load_all()):
        players[p["playerid"]] = p
    
    with open("input/json/players.json", "w") as outfile:
        json.dump(players, outfile)

    return players


def main():
    import pprint
    interested = sys.argv[1:] if len(sys.argv) > 1 else []
    for p in dict_players().values():
        if len(interested) == 0 or p["playerid"] in interested:
            pprint.pprint(p, indent=4)

if __name__ == "__main__":
    main()
