#!/usr/bin/env python
"""  Functions to list and filter league players """
import sys
import logging
import stats.collate
from importer.bbleague.defaults import BASEPATH
LOG = logging.getLogger(__package__)


def order_by_team(players):
    """order list of players by player.team"""
    return sorted(players,
                  key=lambda p: p["teamname"])


def order_by_playername(players):
    """order list of players by player.name"""
    return sorted(players,
                  key=lambda p: p["playername"])


def order_by_position(players):
    """order list of players by player.position"""
    return sorted(players,
                  key=lambda p: p["position"],
                  reverse=False)


def order_by_spp(players):
    """order list of players by player.spp.total"""
    return sorted(players,
                  key=lambda p: int(p["spp"]["total"]) if p["spp"]["total"] else 0,
                  reverse=True)


def order_by_completion(players):
    """order list of players by player.spp.cmp"""
    return sorted(players,
                  key=lambda p: int(p["spp"]["completion"]) if p["spp"]["completion"] else 0,
                  reverse=True)


def order_by_casualties(players):
    """order list of players by player.spp.cas"""
    return sorted(players,
                  key=lambda p: int(p["spp"]["casualty"]) if p["spp"]["casualty"] else 0,
                  reverse=True)


def order_by_touchdowns(players):
    """order list of players by player.spp.td"""
    return sorted(players,
                  key=lambda p: int(p["spp"]["td"]) if p["spp"]["td"] else 0,
                  reverse=True)


def order_by(players, order):
    ordering = order
    if type(order) is not list:
        ordering=list(order)
    ordered = players
    if type(players) is not list:
        ordered=list(players)

    LOG.debug("Ordering %s players by %s", len(ordered), order)
    for o in ordering:
        LOG.debug("Order by %s", o)
        if o == "spp":
            ordered = order_by_spp(ordered)
        elif o == "position":
            ordered = order_by_position(ordered)
        elif o == "name" or o == "playername":
            ordered = order_by_playername(ordered)
        elif o == "team":
            ordered = order_by_team(ordered)
        else:
            LOG.warning("No such ordering %s", o)
    return ordered
        


def filter_invalid(players):
    """Filter players used to record team stats"""
    return filter(lambda p: p["team"] and 
           ("invalid" not in p or not p["invalid"]), players)


def filter_position(players, position):
    """Filter players by position"""
    return filter(lambda p: p["position"] == position, players)


def filter_nospp(players):
    """Filter players with no star player points"""
    return filter(lambda p: p["spp"]["total"].strip() != "" and int(p["spp"]["total"]) > 0, players)

def filter_team(players, team):
    """Filter players by teams"""
    teams = team
    if type(team) is not list:
        teams = list(team)

    return filter(lambda p: p["team"] in teams, players) 

def flatten_players(players):
    """Flatten list of players"""
    for p in players:
        yield flatten_player(p)


def flatten_player(p):
    return {"playerid": p["playerid"],
            "playername": p["playername"],
            "position": p["position"],
            "team": p["team"],
            "teamname": p["teamname"],
            "ma": p["ma"],
            "st": p["st"],
            "ag": p["ag"],
            "av": p["av"],
            "skills": ",".join(p["skills"]),
            "injuries": p["status"]["injury"],
            "int": p["spp"]["interception"],
            "cmp": p["spp"]["completion"],
            "td": p["spp"]["td"],
            "cas": p["spp"]["casualty"],
            "mvp": p["spp"]["mvp"],
            "spp": p["spp"]["total"]}


def all_players(data, include_journeymen=False):
    """Convert players in collated data to list"""
    LOG.debug("Player count is %s", len(data["player"]) if "player" in data else "No 'player' in data")
    if "player" not in data:
        LOG.warning("No 'player' in data")
    if "player" in data and len(data["player"]) == 0:
        LOG.warning("Zero players in data")

    players = data["player"].values()
    players = filter_invalid(players)
    players = order_by_spp(players)
    players = order_by_position(players)

    if not include_journeymen:
        LOG.debug("Filter journeymen")
        return list(filter(lambda p: not p["journeyman"], players))
    return players


def main():
    import argparse
    import player.display
    log_format = "[%(levelname)s:%(filename)s:%(lineno)s - %(funcName)20s ] %(message)s"
    logging.basicConfig(level=logging.WARNING, format=log_format)

    argparser=argparse.ArgumentParser()
    argparser.add_argument("--player", help="Filter players by player id", nargs="*")
    argparser.add_argument("--team", help="Filter players by team", nargs="*")
    argparser.add_argument("--pid", help="Show pid only", action="store_true")
    argparser.add_argument("--journeymen", help="Include journeymen", action="store_true")
    argparser.add_argument("--inactive", help="Include inactive players", action="store_true")
    argparser.add_argument("--position", help="Filter by position", nargs="*")
    argparser.add_argument("--sort", help="Sort players", nargs="*")

    arguments=argparser.parse_args()

    data = stats.collate.collate(False, BASEPATH)
    players = all_players(data, include_journeymen=arguments.journeymen)
    LOG.debug("Player count is %s", len(players))

    if arguments.team:
        players = filter_team(players, arguments.team)
    if arguments.position:
        players = filter_position(players, " ".join(arguments.position))
    if arguments.sort:
        players = order_by(players, arguments.sort)

    for idx, p in enumerate(players):
        if arguments.pid:
            print(p["playerid"])
        else:
            print("{:>4}".format(idx + 1), player.display.plformat(p))
            flatten_player(p)


if __name__ == "__main__":
    main()
