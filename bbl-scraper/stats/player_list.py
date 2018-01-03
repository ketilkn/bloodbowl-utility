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


def filter_invalid(players):
    """Filter players used to record team stats"""
    return filter(lambda p: p["position"].strip() != "-", players)


def filter_nospp(players):
    """Filter players with no star player points"""
    return filter(lambda p: p["spp"]["total"].strip() != "" and int(p["spp"]["total"]) > 0, players)


def flatten_players(players):
    """Flatten list of players"""
    for p in players:
        yield flatten_player(p)


def flatten_player(p):
    return {"playerid": p["playerid"],
            "playername": p["playername"],
            "team": p["team"],
            "teamname": p["teamname"],
            "MA": 6,
            "ST": 3,
            "AG": 3,
            "AV": 8,
            "skills": ",".join(p["upgrade"]["normal"] + p["upgrade"]["extra"]),
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

    players = order_by_spp(data["player"].values())
    players = filter_invalid(players)
    players = filter_nospp(players)

    if not include_journeymen:
        LOG.debug("Filter journeymen")
        return list(filter(lambda p: not p["journeyman"], players))
    return players


def main():
    import player.display
    log_format = "[%(levelname)s:%(filename)s:%(lineno)s - %(funcName)20s ] %(message)s"
    logging.basicConfig(level=logging.DEBUG, format=log_format)

    data = stats.collate.collate(False, BASEPATH)
    players = all_players(data)
    LOG.debug("Player count is %s", len(players))

    for idx, p in enumerate(players):
        print("{:>4}".format(idx + 1), player.display.plformat(p))
        flatten_player(p)
    list(flatten_players(players))


if __name__ == "__main__":
    main()