#!/usr/bin/env python3
import logging
from coach import coach

LOG = logging.getLogger(__package__)


def add_team_race(data):
    for g in data["game"].values():
        g["home_race"] = data["team"][g["home_teamid"]]["race"]
        g["away_race"] = data["team"][g["away_teamid"]]["race"]
    return data["game"]


def add_coach_nick(data):
    print("add_coach_nick, {} {}".format( type(data), len(data)))
    lookup = {c["uid"]:c["nick"] for c in data["coach"].values()}
    for match in data["game"].values():
        match["away_coach"] = lookup[match["away_coachid"]]
        match["home_coach"] = lookup[match["home_coachid"]]
    return data["game"]


def fix_missing_coaches(data):
    def fix_coach(gam, coaches, teams):
        if gam["home_coachid"] in ["0", None]:
            team_coachnick = teams[gam["home_teamid"]]['coach']
            uid = coach.find_uid_for_nick(data["coach"], team_coachnick)
            gam["home_coachid"] = uid if uid else -1
        if gam["away_coachid"] in ["0", None]:
            team_coachnick = teams[gam["away_teamid"]]['coach']
            uid = coach.find_uid_for_nick(data["coach"], team_coachnick)
            gam["away_coachid"] = uid if uid else -1

    for matchid, g in data["game"].items():
        fix_coach(g, data["coach"], data["team"])

    return data["game"]


def collate_match(data):
    games2 = fix_missing_coaches(data)
    games2 = add_coach_nick(data)
    games2 = add_team_race(data)
    return games2


