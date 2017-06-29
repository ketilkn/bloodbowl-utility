#!/usr/bin/env python3
import sys
from match import match
from coach import coach
from team import team

def collate():
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
        if gam[home_or_away]["coachid"] == 0:
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
    from sys import argv
    import pprint
    pp = pprint.PrettyPrinter(indent=4)
    the_coach = argv[1] if len(argv) > 1 else "Kyrre"
    the_team = argv[2] if len(argv) > 2 else "tea2"
    the_game = argv[3] if len(argv) > 3 else "1061"

    data = collate()
    print("Coach {}".format(the_coach))
    pp.pprint(data["coach"][the_coach])
    print("Team {}".format(the_team))
    pp.pprint(data["team"][the_team])
    print("Game {}".format(the_game))
    pp.pprint(data["game"][the_game])

if __name__ == "__main__":
    main()
