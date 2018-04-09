#!/usr/bin/env python
"""  Create new team """
import sys
import logging
import scrape.session

LOG = logging.getLogger(__package__)


def create_team(team_name, race, coach, co_coach, session):
    LOG.debug("Creating team '%s' '%s' '%s' '%s'", team_name, race, coach, co_coach)
    team_form = {"coach": coach,
            "coach2": co_coach,
            "race": race,
            "navn": team_name,
            "rr": 0,
            "ff": 0}

    response = session.post("http://test.bloodbowlleague.com/default.asp?p=nt", data=team_form)


def main():
    log_format = "[%(levelname)s:%(filename)s:%(lineno)s - %(funcName)20s ] %(message)s"
    logging.basicConfig(level=logging.DEBUG, format=log_format)

    if len(sys.argv) < 3:
        sys.exit("username password team_name")
    s = scrape.session.login("http://test.bloodbowlleague.com/login.asp", username=sys.argv[1], password=sys.argv[2])
    team_name=" ".join(sys.argv[3:])
    team_race="5"
    coach="Ketil"
    co_coach=""

    if s:
        LOG.debug("Session seems OK")
    else:
        sys.exit("session not ok?")

    create_team(team_name, team_race, coach, co_coach, s)


if __name__ == "__main__":
    main()