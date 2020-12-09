#!/usr/bin/env python
""" Parse player from HTML file """
import sys
import re
import dateutil.parser as parser
import logging

from bs4 import BeautifulSoup
from bs4.element import NavigableString

LOG = logging.getLogger(__package__)

def row_with_heading(table, heading):
    LOG.debug("Searching for heading {}".format(heading))
    for row in table.select("tr"):
        if isinstance(row, NavigableString):
            continue
        LOG.debug("raden: {}".format(row))
        columns = list(row.select("td"))
        LOG.debug("{} children {}".format(len(columns), columns))
        if columns[0] and heading in columns[0].text:
            LOG.debug("Found {} with content '{}'".format(heading, columns[1].text))
            if columns[1].select_one("a"):
                return columns[1].select_one("a")["href"] if columns[1].select_one("a").has_attr("href") else columns[1].text
            return columns[1].text
    LOG.debug("{} not found".format(heading))
    return None


def parse_touchdown(achievements):
    LOG.debug("-==< parse TOUCHDOWN >==-")
    LOG.debug("achievement el %s", achievements[2])
    return achievements[2].text


def parse_casualties(achievements):
    LOG.debug("-==< parse CASUALTIES >==-")
    LOG.debug("achievement el %s", achievements[3])
    return achievements[3].text


def parse_completions(achievements):
    LOG.debug("-==< parse COMPLETIONS >==-")
    LOG.debug("achievement el %s", achievements[1])
    return achievements[1].text


def parse_interception(achievements):
    LOG.debug("-==< parse INTERCEPTION >==-")
    LOG.debug("achievement el %s", achievements[0])
    return achievements[0].text


def parse_total(achievements):
    LOG.debug("-==< parse TOTAL >==-")
    LOG.debug("achievement el %s", achievements[5])
    return achievements[-3].text.strip()



def parse_mvp(achievements):
    LOG.debug("MVP >=========-")
    LOG.debug("achievement el %s", achievements[4])
    return achievements[4].text

def parse_value(soup):
    spans = soup.find_all("span", style="font-size:10px")
    for span in spans:
        if " gp" in span.text:
            return int(span.text.strip()[:-3].replace(",",""))
    return ""


def find_achievements(soup):
    el = soup.select("table[style='background-color:#F0F0F0;border:1px solid #808080'] td[align=center]")
    if el:
        return el
    return soup.select('tr.trborder td table td[align=center]')


def parse_games(player, soup):
    LOG.debug("-==< parse player with id %s >==-", player["playerid"])

    achievements = find_achievements(soup)
    spp_table = soup.select_one("table[style='background-color:#F0F0F0;border:1px solid #808080'] table")

    LOG.debug("achievements len %s", len(achievements))
    
    player["spp"] =  {"interception": parse_interception(achievements), 
            "td":parse_touchdown(achievements), 
            "casualty": parse_casualties(achievements), 
            "completion": parse_completions(achievements), 
            "mvp": parse_mvp(achievements),
            "total": achievements[5].text}
    return player


def parse_playername(soup):
    return soup.select_one("h1").text


def parse_position(soup):
    for el in soup.select("td a"):
        if el.has_attr("href") and "default.asp?p=pt&typID=" in el["href"]:
            return el.text
    return "unknown"


def parse_spp(soup):
    return ["spp"]

def parse_profile(player, soup):
    profile = soup.select_one('div[style="vertical-align:top;background-color:#F0F0F0;font-size:10px;border:1px solid #808080;width:300px;min-height:80px;text-align:justify;padding:3px"]')
    LOG.debug("profile len %s", len(profile.text) if profile else "NOT FOUND!!")
    player["profile"] = profile.text.replace('\xa0', ' ') if profile and "----empty----" not in profile.text else ""
    return player

def column_with_heading(table, heading):
    LOG.debug("Looking for column with heading %s", heading)
    found = False
    rows = table.find_all("tr")
    LOG.debug("Table has %s rows", len(rows))
    headings = rows[0]
    LOG.debug(headings)
    values = rows[1]
    LOG.debug(values)
    for idx, h in enumerate(headings.find_all("td")):
        LOG.debug(h)
        if h.text == heading:
            return values.find_all("td")[idx]
    return False


def parse_abilities(soup, ability, playerid):
    table = soup.select_one("table[width='300']")
    if not table:
        LOG.debug("Ability table not found for player %s", playerid)
        return "0"

    column = column_with_heading(table, ability)
    return [s.strip() for s in column.find_all(text=True) if s.strip()!=","] if column else []


def parse_ability(soup, ability, playerid):
    table = soup.select_one("table[width='300']")
    if not table:
        LOG.debug("Ability table not found for player %s", playerid)
        return "0"

    column = column_with_heading(table, ability)
    return column.text if column else "-1"


def parse_team(player, soup):
    LOG.debug("parse player with id %s", player["playerid"])
    LOG.debug("TEAM >========-")
    team = soup.select_one("a[style='font-size:11px']")
    LOG.debug("team   el %s", "{}".format(team))

    player["playername"] = parse_playername(soup)
    player["position"] = parse_position(soup)
    player["value"] = parse_value(soup)

    team_id = team["href"].split("=")[-1] if team and team.has_attr("href") else None
    team_name = team.text if team else ""

    player["ma"] = int(parse_ability(soup, "MA", player["playerid"]))
    player["st"] = int(parse_ability(soup, "ST", player["playerid"]))
    player["ag"] = int(parse_ability(soup, "AG", player["playerid"]))
    player["av"] = int(parse_ability(soup, "AV", player["playerid"]))
    player["skills"] = parse_abilities(soup, "Skills", player["playerid"])


    number = soup.select_one('td[style="max-height:20px;font-size:10px"]')
    LOG.debug("number el %s", "{}".format(number))


    player["team"] = team_id
    player["teamname"] = team_name
    player["number"] = number.text.split('\xa0')[-1] if number else ""

    return parse_profile(player, soup)


def parse_fromfile(path, playerid):
    LOG.debug("%s %s", path, playerid)
    import player.load
    parsed_player = parse_games({"playerid": playerid}, soup=player.load.from_file("{}/player-{}.html".format(path, playerid)))
    parsed_player = parse_team(parsed_player, soup=player.load.from_file("{}/player-{}.html".format(path, playerid)))
    return parsed_player


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
