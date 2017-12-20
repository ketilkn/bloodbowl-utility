#!/usr/bin/env python
"""  Create list of coaches from team list for use when actual coach list is missing. """
import sys
import logging

from . import parse
import team.parse

LOG = logging.getLogger(__package__)

def create_coach(nick, uid):
    coach = {'nick': nick,
             'email': nick,
             'naf': "no naf",
             'role': "unknown",
             'phone': "no phone",
             'location': "Old World",
             'login': parse.NEVER_LOGGED_IN,
             'loggedin': True,
             'uid': uid}

    if(coach["login"] != parse.NEVER_LOGGED_IN):
        coach["loggedin"] = True

    return coach


def parse_teams(teams):
    coaches = set()

    for team in teams:
        LOG.debug("{}:: ".format(team["name"]), team["coach"], team["co-coach"])
        if team["coach"]:
            coaches.add(team["coach"])
        if team["co-coach"]:
            coaches.add(team["co-coach"])

    return [create_coach(coach, index+10000) for index, coach in enumerate(coaches)]


def list_coaches():
    LOG.debug("Retrieving coaches from team list")
    teams = team.parse.list_teams()
    LOG.debug("Found {} teams".format(len(teams)))
    coaches = parse_teams(teams)

    return coaches



def main():
    from pprint import pprint
    log_format = "[%(levelname)s:%(filename)s:%(lineno)s - %(funcName)20s ] %(message)s"
    logging.basicConfig(level=logging.DEBUG, format=log_format)
    LOG.info("Parsing teamlist for coaches")

    coaches = list_coaches()

    pprint(coaches, indent=2)




if __name__ == "__main__":
    main()