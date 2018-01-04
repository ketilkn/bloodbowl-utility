#!/usr/bin/env python3
import os
import sys
import json
from match import match
from coach import coach
from team import team
from player import player
from . import collate_coach
from . import collate_match
from . import collate_team
from . import collate_player

from importer.bbleague.defaults import BASEPATH


def load_from_json(basepath = BASEPATH):
    path = os.path.join(basepath, "json/data.json")
    data = open(path, "rb").read()
    return json.loads(data.decode())


def save_to_json(collated_data, basepath = BASEPATH):
    path = os.path.join(basepath, "json/data.json")
    data = json.dumps(collated_data)
    json_file = open(path, "wb")
    json_file.write(data.encode())
    json_file.close()
    

def collate(reload=False, basepath = BASEPATH):
    path = os.path.join(basepath, "json/data.json")
    coaches8 = os.path.join(basepath, "html/coach/coaches-8.html")
    if reload or not os.path.isfile(path) or os.stat(path).st_mtime < os.stat(coaches8).st_mtime:
        collated_data = collate_data(coach.dict_coaches(), team.dict_teams(), match.dict_games(), player.dict_players())
        save_to_json(collated_data)
        return collated_data
    return load_from_json()


def collate_from_disk():
    return collate(True)

def collate_data(coaches, teams, games, players):
    data = {"coach": coaches,
            "team": teams,
            "game": games,
	    "player": players}

    return {"game": collate_match.collate_match(data),
            "coach": collate_coach.collate_coach(data),
            "team": collate_team.collate_team(data),
            "player": collate_player.collate_players(data),
            "_coachid": coach.dict_coaches_by_uid() 
            }

def main():
    import pprint
    import sys
    def pretty(value):
        pprint.pprint(value, indent=2)

    def search(data, display):
        for t in data["team"].values():
            if t["id"] in display:
                yield t
        for c in data["coach"].values():
            if c["nick"] in display:
                yield c
        for g in data["game"].values():
            if g["matchid"] in display:
                yield g
        for p in data["player"].values():
            if "p"+p["playerid"] in display:
                yield p

    force_reload = True if "--force" in sys.argv else False
    search_terms = list(filter(lambda x: not x.startswith("--"), sys.argv[1:]))

    data = collate(force_reload)

    for found in search(data, search_terms if len(search_terms) > 0 else ["Kyrre", "tea2", "1061", "p2804"]):
        pretty(found)

    print("Data count: {}".format([[key, type(data[key]), len(data[key])] for key in data.keys()]))

if __name__ == "__main__":
    main()
