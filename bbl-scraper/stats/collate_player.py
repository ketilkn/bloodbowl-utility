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

def hide_invalid_players(players):
    for p in players.values():
    	p["invalid"] = p["position"].strip() in ["-", "Skaven Bookie", "Undead High Liche Priest", "Human Referee"]
    return players


def collate_players(data):
    players =  data["player"]
    players = hide_invalid_players(players)

    return players


