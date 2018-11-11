#!/usr/bin/env python
""" Parse player from HTML file """
import sys
import re
import dateutil.parser as parser
import logging

from bs4 import BeautifulSoup
from bs4.element import NavigableString

from player import parse_admin
from . import parse_profile

LOG = logging.getLogger(__package__)


def parse_fromfile(path, playerid):
    LOG.debug("%s %s", path, playerid)
    import player.load

    try:
        parsed_player = parse_admin.parse_player(playerid, soup=player.load.from_file("{}/admin-player-{}.html".format(path, playerid)))
        parsed_player = parse_profile.parse_games(parsed_player, soup=player.load.from_file("{}/player-{}.html".format(path, playerid)))
        parsed_player = parse_profile.parse_team(parsed_player, soup=player.load.from_file("{}/player-{}.html".format(path, playerid)))

        if not parsed_player["journeyman"] and parsed_player["status"]["active"]["reason"] == "no status":
            LOG.warning("%s %s %s %s has no status", parsed_player["team"], playerid, parsed_player["playername"],
                     parsed_player["position"])
        return parsed_player
    except:
        LOG.exception("Exception while parsing %s in %s", playerid, path)




def main():
    log_format = "[%(levelname)s:%(filename)s:%(lineno)s - %(funcName)20s ] %(message)s"
    #logging.basicConfig(level=logging.DEBUG, format=log_format)
    logging.basicConfig(level=logging.DEBUG)
    import pprint
    if len(sys.argv) < 2:
        sys.exit("path and playerid required")
    path = sys.argv[1] if not sys.argv[1].isdigit() else "input/html/player"
    players = sys.argv[1:] if sys.argv[1].isdigit() else sys.argv[2:]

    for player_id in players:
        if player_id.isdigit():
            parsed_player = parse_fromfile(path, player_id)
            pprint.PrettyPrinter(indent=4).pprint(parsed_player)


if __name__ == "__main__":
    main()
