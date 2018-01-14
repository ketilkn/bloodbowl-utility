#!/usr/bin/env python
""" Parse player from HTML file """
import sys
import re
import dateutil.parser as parser
import logging

from bs4 import BeautifulSoup
from bs4.element import NavigableString

LOG = logging.getLogger(__package__)


def parse_date(soup):
    LOG.debug("CREATION DATE >==-")
    indates = soup.select("input[name=indate]")
    LOG.debug("Search len %s", len(indates))
    indate = indates[0]
    LOG.debug("indate el %s", "{}".format(indate))
    return parser.parse(indate["value"]).isoformat()


def parse_bounties(soup):
    LOG.debug("-==< Parsing BOUNTY >==-")
    bounties = soup.select("input[name=bounty]")
    LOG.debug("Search len %s", len(bounties))
    bounty = bounties[0]
    Log.debug("bounty el: %s", bounty)
    return {"total": int(bounty["value"]) * 1000}



def parse_journeyman(soup):
    LOG.debug("JOURNEYMAN >=========-")
    return parse_playername(soup).strip() == "journeyman"


def parse_playername(soup):
    LOG.debug("PLAYER NAME >=========-")
    search = soup.select("input[name=name]")
    LOG.debug("Search len %s", len(search))
    playername = search[0]
    LOG.debug("playername el %s", playername)
    return playername["value"]


def parse_position(soup):
    LOG.debug("POSITION >=========-")
    search = soup.select("select option[selected]")
    LOG.debug("Search len %s", len(search))
    position = search[0]
    LOG.debug("position el %s", position)
    return position["value"]


def parse_normal(soup):
    LOG.debug("NORMAL >=========-")
    normal = soup.find_all("input", {"name": lambda x: x and x.startswith("upgr") and x != "upgr7"})
    LOG.debug("search len %s", len(normal))
    for el in normal:
        LOG.debug("normal el %s", el)
    return [x["value"] for x in normal if x["value"]]


def parse_extra(soup):
    LOG.debug("EXTRA >=========-")
    extra = soup.select_one("input[name=upgr7]")
    LOG.debug("extra el %s", extra)

    return [x for x in extra["value"].split(',') if len(extra["value"]) > 0]


def parse_modifier(soup):
    LOG.debug("MODIFIER >=========-")
    return {"ma": parse_characteristic(soup, "ma"),
            "st": parse_characteristic(soup, "st"),
            "ag": parse_characteristic(soup, "ag"),
            "av": parse_characteristic(soup, "av")}


def parse_upgrade(soup):
    LOG.debug("EXTRA UPGRADE >=========-")

    search = soup.select("input[name=upgr7]")
    LOG.debug("Search len %s", len(search))

    extra = search[0]
    LOG.debug("extra el %s", extra)

    return {"normal": parse_normal(soup),
            "extra": parse_extra(soup),
            "modifier": parse_modifier(soup)}


def parse_characteristic(soup, characteristic):
    LOG.debug("CHARACTERISTIC %s >=========-", characteristic)
    element = soup.select_one("select[name={}] option[selected]".format(characteristic))
    LOG.debug("characteristic el %s", element)
    return int(element["value"])


def parse_halloffame(soup):
    LOG.debug("HALL_OF_FAME >=========-")
    hall_of_famer = soup.select_one("select[name=hof] option[selected]")
    LOG.debug("h-o-f el  %s", hall_of_famer)
    # print(hall_of_famer)
    hall_of_famer_reason = soup.select_one("textarea[name=hofreason]")
    return {"hall_of_famer": True if hall_of_famer and hall_of_famer["value"] != 0 else False,
            "season": hall_of_famer["value"] if hall_of_famer else 0,
            "reason": hall_of_famer_reason.string if hall_of_famer_reason else ""}

def parse_note(soup):
    LOG.debug("NOTE >========>")
    note = soup.select_one("textarea[name=remarks]")
    LOG.debug("Note len %s", len(note.text))

    return note.text.replace('\xa0', ' ')

def parse_permanent(soup):
    LOG.debug("PERMANENT injuries >=========-")
    permanent = soup.select_one("input[name=inj]")
    LOG.debug("permanent el %s", permanent)
    return list(filter(lambda x: len(x) > 0, permanent["value"].split(",")))


def parse_active(soup, pid=None):
    LOG.debug("ACTIVE >=========-")
    status = soup.select_one("select[name=status]")
    LOG.debug("status len %s", len(status))
    for el in status:
        LOG.debug("option el {}".format(el).strip())

    selected_option = status.select_one("option[selected]")
    LOG.debug("option->selected {}".format(selected_option))

    active = True if selected_option and selected_option["value"] == "a" else False
    reason = selected_option.text if not active and selected_option else ""

    if not selected_option:
        LOG.debug("No selected_option for %s", pid)
    LOG.debug("active: %s %s", active, reason)
    return {"active": active,
            "reason": reason if selected_option else ""}


def parse_status(soup, pid="Unknown"):
    LOG.debug("PARSE STATUS")
    return {"entered_league": parse_date(soup),
            "niggle": parse_niggle(soup),
            "injury": parse_permanent(soup),
            "active": parse_active(soup, pid=pid)}


def parse_niggle(soup):
    LOG.debug("NIGGLE >=========-")
    niggle =soup.select_one("select[name=n] option[selected]")
    LOG.debug("niggle el %s", niggle)
    return int(niggle["value"])


def parse_player(playerid, soup):
    LOG.debug("parse player-admin with id %s", playerid)
    player_date = parse_date(soup)
    if not player_date:
        return None
    player = {"playerid": playerid,
              "playername": parse_playername(soup),
              "position": parse_position(soup),
              "upgrade": parse_upgrade(soup),
              "status": parse_status(soup, pid=playerid),
              "hall_of_fame": parse_halloffame(soup),
              "journeyman": parse_journeyman(soup),
              "note": parse_note(soup)
              }
    return player


def parse_fromfile(path, playerid):
    LOG.debug("%s %s", path, playerid)
    import player.load
    parsed_player = parse_player(playerid, soup=player.load.from_file("{}/admin-player-{}.html".format(path, playerid)))
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
