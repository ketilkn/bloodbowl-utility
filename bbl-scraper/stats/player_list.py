#!/usr/bin/env python
"""  Functions to list and filter league players """
import sys
import logging
import stats.collate
from importer.bbleague.defaults import BASEPATH
LOG = logging.getLogger(__package__)


def order_by_spp(players):
    """order list of players by player.spp.total"""
    return sorted(players,
                  key=lambda p: int(p["spp"]["total"]) if p["spp"]["total"] else 0,
                  reverse=True)


def all_players(data, include_journeymen=False):
    """Convert players in collated data to list"""
    LOG.debug("Player count is %s", len(data["player"]) if "player" in data else "No 'player' in data")
    if "player" not in data:
        LOG.warning("No 'player' in data")
    if "player" in data and len(data["player"]) == 0:
        LOG.warning("Zero players in data")

    players = order_by_spp(data["player"].values())

    if not include_journeymen:
        LOG.debug("Filter journeymen")
        return list(filter(lambda p: not p["journeyman"], players))
    return players


def main():
    from pprint import pprint
    log_format = "[%(levelname)s:%(filename)s:%(lineno)s - %(funcName)20s ] %(message)s"
    logging.basicConfig(level=logging.DEBUG, format=log_format)

    data = stats.collate.collate(False, BASEPATH)
    players = all_players(data)
    LOG.debug("Player count is %s", len(players))

    for p in players[0:1]:
        pprint(p, indent=4)




if __name__ == "__main__":
    main()