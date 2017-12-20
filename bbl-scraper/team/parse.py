#!/usr/bin/env python
from bs4 import BeautifulSoup
from unicodedata import normalize
import re
import logging

LOG = logging.getLogger(__package__)


def find_rows(soup):
    teams = []
    rows = soup.find_all("tr")
    for row in rows:
        if row.has_attr("height") and row['height'] == "30":
            teams.append(row)

    return teams


def id_from_onclick(el):
    if el.has_attr("onclick") and el["onclick"].startswith("self.location.href='default.asp?p=tm&t="):
        oncl = el["onclick"]
        return re.sub(r'\W+', '', oncl[el["onclick"].rfind("=") + 1:])
    return None


def parse_id(row):
    id_from_row = id_from_onclick(row)
    if id_from_row:
        return id_from_row
    columns = row.find_all("td")
    for column in columns:
        teamid = id_from_onclick(column)
        if teamid != None:
            return teamid


def parse_name(row):
    return row.find("b").text


def parse_race(row):
    return row.find_all(lambda tag: tag.name == "td" and tag.get('class') == ['td10'])[0].text


def parse_teamvalue(row):
    teamvalue = row.find_all(lambda tag: tag.name == "td" and tag.get('class') == ['td10'])[2].text.replace('\xa0',
                                                                                                            '').replace(
        "k", "000")
    try:
        return int(teamvalue)  # if teamvalue !="" else None
    except ValueError:
        return None


def parse_cocoach(row):
    coach = row.find_all(lambda tag: tag.name == "td" and tag.get('class') == ['td10'])[1].text
    return coach.split("&")[1] if len(coach.split("&")) == 2 else None


def parse_coach(row):
    coach = row.find_all(lambda tag: tag.name == "td" and tag.get('class') == ['td10'])[1].text
    return coach.split("&")[0] if coach != "?" else None


def parse_team_row(row):
    team = {"id": parse_id(row),
            "name": parse_name(row),
            "coach": parse_coach(row),
            "co-coach": parse_cocoach(row),
            "race": parse_race(row),
            "teamvalue": parse_teamvalue(row)}
    return team


def parse_rows(rows_of_teams):
    teams = []
    for row in rows_of_teams:
        teams.append(parse_team_row(row))
    return teams


def dict_teams():
    teams = list_teams()
    result = {}
    for team in teams:
        result[team["id"]] = team
    return result


def list_teams():
    LOG.info("list teams from input/html/team/teams-8.html")
    html = open("input/html/team/teams-8.html", "r").read()
    soup = BeautifulSoup(normalize("NFC", html), "html.parser")

    teams = parse_rows(find_rows(soup))
    return teams


def main():
    import pprint
    log_format = "[%(levelname)s:%(filename)s:%(lineno)s - %(funcName)20s ] %(message)s"
    logging.basicConfig(level=logging.DEBUG, format=log_format)
    LOG.info("Parsing teamlist")

    pprint.PrettyPrinter().pprint(list_teams())


if __name__ == "__main__":
    main()
