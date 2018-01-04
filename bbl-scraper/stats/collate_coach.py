#!/usr/bin/env python3
import os
import sys
import json
import logging
from match import match
from coach import coach
from team import team
from player import player
from importer.bbleague.defaults import BASEPATH

LOG = logging.getLogger(__package__)


def collate_coach(data):
    for coach in data["coach"].values():
        coach["games"]=[]
    for match in data["game"].values():
        if match["matchid"] in data["coach"][match["home"]["coach"]]["games"]:
            print("Warning {} already exists in {}".format(match["matchid"], match["home"]["coach"]))
        data["coach"][match["home"]["coach"]]["games"].append(match["matchid"])

        if match["matchid"] in data["coach"][match["away"]["coach"]]["games"]:
            print("Warning {} already exists in {}".format(match["matchid"], match["away"]["coach"]))
        data["coach"][match["away"]["coach"]]["games"].append(match["matchid"])

    return data["coach"]

