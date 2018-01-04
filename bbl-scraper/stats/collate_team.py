#!/usr/bin/env python3
import os
import json
import logging
from match import match
from coach import coach
from team import team
from player import player
from importer.bbleague.defaults import BASEPATH

LOG = logging.getLogger(__package__)

def collate_team(data):
    for team in data["team"].values():
        team["games"]=[]

    for match in data["game"].values():
        if match["matchid"] in data["team"][match["home"]["team"]["teamid"]]["games"]:
            print("Warning {} already exists in {}".format(match["matchid"], match["home"]["team"]))
        data["team"][match["home"]["team"]["teamid"]]["games"].append(match["matchid"])

        if match["matchid"] in data["team"][match["away"]["team"]["teamid"]]["games"]:
            print("Warning {} already exists in {}".format(match["matchid"], match["away"]["team"]))
        data["team"][match["away"]["team"]["teamid"]]["games"].append(match["matchid"])

    return data["team"]




