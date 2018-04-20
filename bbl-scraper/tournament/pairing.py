#!/usr/bin/env python
"""  Match teams for round """
import sys
import logging

LOG = logging.getLogger(__package__)


def pairing(standings, matches, type="swiss"):
    if not standings:
        raise ValueError("standings are None or empty")
    return swiss_pairing(standings, matches)


def match_played(home_team, away_team, matches):
    for match in matches:
        print("match played {}-{} {}".format(home_team["teamid"], away_team["teamid"], match))
        if match["home_team"]["teamid"] == home_team["teamid"] and match["away_team"]["teamid"] == away_team["teamid"]:
            print("TRUE")
            return True
        if match["away_team"]["teamid"] == home_team["teamid"] and match["home_team"]["teamid"] == away_team["teamid"]:
            print("TRUE")
            return True
        print("FALSE")
        return False


def find_opponent(home_team, teams, matches):
    if not matches:
        return teams.pop(0)
    for index, team in enumerate(teams):
        if not match_played(home_team, teams[index], matches):
            return teams.pop(index)
    return None


def swiss_pairing(standings, played_matches):
    matches = []
    teams = standings[:]

    while len(teams):
        home_team = teams.pop(0)
        away_team = find_opponent(home_team, teams, played_matches)

        matches.append({"home_team": home_team,
                        "away_team": away_team})

    import pprint
    pprint.pprint(matches)
    return matches


def main():
    log_format = "[%(levelname)s:%(filename)s:%(lineno)s - %(funcName)20s ] %(message)s"
    logging.basicConfig(level=logging.DEBUG, format=log_format)


if __name__ == "__main__":
    main()