#!/usr/bin/env python3
import os
import sys
import json
from match import match
from coach import coach
from team import team

def load_from_json():
    data = open("input/json/data.json", "rb").read()
    return json.loads(data.decode())


def save_to_json(collated_data):
    data = json.dumps(collated_data)
    json_file = open("input/json/data.json", "wb")
    json_file.write(data.encode())
    json_file.close()
    

def collate(reload=False):
    if reload or not os.path.isfile("input/json/data.json") or os.stat("input/json/data.json").st_mtime < os.stat("input/coaches-8.html").st_mtime:
        collated_data = collate_data(coach.dict_coaches(), team.dict_teams(), match.dict_games())
        save_to_json(collated_data)
        return collated_data
    return load_from_json()


def collate2():
    coaches = coach.dict_coaches()
    teams = team.dict_teams()
    games = match.dict_games()

    return collate_data(coaches, teams, games)

def collate_team(data):
    return data["team"]

def add_team_race(data):
    for g in data["game"].values():
        g["home"]["team"]["race"] = data["team"][g["home"]["team"]["teamid"]]["race"]
        g["away"]["team"]["race"] = data["team"][g["away"]["team"]["teamid"]]["race"]
    return data["game"]

def fix_missing_coaches(data):
    def fix_coach(home_or_away, gam, coaches, teams):
        if gam[home_or_away]["coachid"] in ["0", None]:
            team_coachnick = teams[gam[home_or_away]['team']['teamid']]['coach']
            uid = coach.find_uid_for_nick(data["coach"], team_coachnick) 
            gam[home_or_away]["coachid"] = uid if uid else -1

    for matchid, g in data["game"].items():
        fix_coach("home", g, data["coach"], data["team"])
        fix_coach("away", g, data["coach"], data["team"])
        
    return data["game"]

def collate_gamecoach(data):
    games2 = fix_missing_coaches(data)
    games2 = add_team_race(data)
    return games2

def collate_data(coaches, teams, games):
    data = {"coach": coaches,
            "team": teams,
            "game": games}

    return {"coach": coaches,
            "_coachid": coach.dict_coaches_by_uid(), 
            "team": collate_team(data),
            "game": collate_gamecoach(data)}

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

    force_reload = True if "--force" in sys.argv else False
    search_terms = list(filter(lambda x: not x.startswith("--"), sys.argv[1:]))

    data = collate(force_reload)

    for found in search(data, search_terms if len(search_terms) > 0 else ["Kyrre", "tea2", "1061"]):
        pretty(found)

    print("Data count: {}".format([[key, len(data[key])] for key in data.keys()]))

if __name__ == "__main__":
    main()
