#!/usr/bin/env python
"""  Match teams for round """
import sys
import logging

LOG = logging.getLogger(__package__)


def pairing(standings, matches, type="swiss"):
    if not standings:
        raise ValueError("standings are None or empty")
    return swiss_pairing(standings, matches)


def swiss_pairing(standings, matches):
    matches = []
    teams = standings[:]

    while len(teams):
        matches.append({"home_team": teams.pop(0) , "away_team": teams.pop(0)})

    return matches


def main():
    log_format = "[%(levelname)s:%(filename)s:%(lineno)s - %(funcName)20s ] %(message)s"
    logging.basicConfig(level=logging.DEBUG, format=log_format)


if __name__ == "__main__":
    main()