#!/usr/bin/env python3
import logging
from coach import coach

LOG = logging.getLogger(__package__)


def add_team_race(data):
    for g in data["game"].values():
        g["home"]["team"]["race"] = data["team"][g["home"]["team"]["teamid"]]["race"]
        g["away"]["team"]["race"] = data["team"][g["away"]["team"]["teamid"]]["race"]
    return data["game"]


def add_coach_nick(data):
    lookup = {c["uid"]:c["nick"] for c in data["coach"].values()}
    for match in data["game"].values():
        match["away"]["coach"] = lookup[match["away"]["coachid"]]
        match["home"]["coach"] = lookup[match["home"]["coachid"]]
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


def collate_match(data):
    games2 = fix_missing_coaches(data)
    games2 = add_coach_nick(data)
    games2 = add_team_race(data)
    return games2


