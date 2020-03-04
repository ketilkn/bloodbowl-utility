#!/usr/bin/env python
"""  Create new team """
import sys
import logging
import scrape.session

LOG = logging.getLogger(__package__)


def create_match(session, tournament_id, home_id, away_id, tround, mdate=None, tournament_match=True):
    LOG.debug("Creating match '%s' '%s' '%s' '%s' '%s' '%s'", tournament_id, home_id, away_id, tround, mdate, tournament_match)
    match_form = {
            "m0team1": home_id,
            "m0team2": away_id,
            "dato": mdate,
            "puljekamp": 1 if tournament_match else 0,
            "runde": tround,
            "retid": 0}

    response = session.post("http://test.bloodbowlleague.com/addmatch.asp?s={}&ret=0".format(tournament_id), data=match_form)
    return response


def main():
    log_format = "[%(levelname)s:%(filename)s:%(lineno)s - %(funcName)20s ] %(message)s"
    logging.basicConfig(level=logging.DEBUG, format=log_format)

    if len(sys.argv) < 4:
        sys.exit("username password home_id away_id")
    s = scrape.session.login("http://test.bloodbowlleague.com/login.asp", username=sys.argv[1], password=sys.argv[2])
    home_id = sys.argv[3]
    away_id = sys.argv[4]

    if s:
        LOG.debug("Session seems OK")
    else:
        sys.exit("session not ok?")

    response=create_match(s, 2, home_id, away_id, "runde 1", mdate="7/21/2018")

    print(response)
    print(response.text)


if __name__ == "__main__":
    main()
