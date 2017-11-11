#!/usr/bin/env python
""" Python libraries for Dr.Tide"""
import logging
LOG = logging.getLogger(__package__)
from bs4 import BeautifulSoup
from unicodedata import normalize
import datetime
import dateutil.parser as parser
import re
#import team 
import sys

def parse_date(soup):
    return parser.parse(soup.select("input[name=indate]")[0]["value"]).isoformat()

def parse_bounties(soup):
    return {"total": int(soup.select("input[name=bounty]")[0]["value"])*1000}

def parse_touchdown(achievements):
    return achievements[2].text

def parse_casualties(achievements):
    return achievements[3].text

def parse_completions(achievements):
    return achievements[1].text

def parse_interception(achievements):
    return achievements[0].text

def parse_total(achievements):
    return achievements[5].text

def parse_mvp(achievements):
    return achievements[4].text

def parse_games(player, soup):
    achievements = soup.select("table[style='background-color:#F0F0F0;border:1px solid #808080'] td[align=center]")
    player["spp"] =  {"interception": parse_interception(achievements), 
            "td":parse_touchdown(achievements), 
            "casualty": parse_casualties(achievements), 
            "completion": parse_completions(achievements), 
            "mvp": parse_mvp(achievements),
            "total": parse_total(achievements)} 
    return player

def parse_playername(soup):
    return soup.select("input[name=name]")[0]["value"]

def parse_position(soup):
    return soup.select("select option[selected]")[0]["value"]

def parse_normal(soup):
    normal = soup.find_all("input", {"name": lambda x: x and x.startswith("upgr") and x!= "upgr7"})
    return  [x["value"] for x in normal if x["value"]]
def parse_extra(soup):
    extra = soup.select("input[name=upgr7]")[0]
    return  [x for x in extra["value"].split(',') if len(extra["value"]) > 0] 

def parse_modifier(soup):
    return { "ma": parse_characteristic(soup, "ma"), 
            "st": parse_characteristic(soup, "st"), 
            "ag": parse_characteristic(soup, "ag"), 
            "av": parse_characteristic(soup, "av")}

    
def parse_upgrade(soup):
    extra = soup.select("input[name=upgr7]")[0]
    return {"normal": parse_normal(soup),
            "extra": parse_extra(soup), 
            "modifier": parse_modifier(soup)}
def parse_characteristic(soup, characteristic): 
    return int(soup.select_one("select[name={}] option[selected]".format(characteristic))["value"])

def parse_halloffame(soup):
    hall_of_famer= soup.select_one("select[name=hof] option[selected]")
    #print(hall_of_famer)
    hall_of_famer_reason = soup.select_one("textarea[name=hofreason]")
    return {"hall_of_famer": True if hall_of_famer and hall_of_famer["value"]!=0 else False,
            "season": hall_of_famer["value"] if hall_of_famer else 0,
            "reason": hall_of_famer_reason.string if hall_of_famer_reason else ""} 

def parse_permanent(soup):
    return list(filter(lambda x: len(x) > 0, soup.select_one("input[name=inj]")["value"].split(",")))

def parse_active(soup):
    status = soup.select_one("select[name=status] option[selected]")
    return {"active": True if status["value"] == "a" else False,
            "reason": status.string if status["value"] != "a" else ""}

def parse_status(soup): 
    return  {"entered_league": parse_date(soup),
            "niggle": parse_niggle(soup),
            "injury": parse_permanent(soup),
            "active": parse_active(soup)}

def parse_niggle(soup):
    return int(soup.select_one("select[name=n] option[selected]")["value"])

def parse_spp(soup):
    return ["spp"]

def parse_team(player, soup):
    team = soup.select_one("a[style=font-size:11px]")
    team_id = team["href"].split("=")[-1] if team and team.has_attr("href") else None
    team_name = team.text if team else ""
    player["team"] = team_id
    player["teamname"] = team_name

    return player



def parse_player(playerid, soup):
    player_date = parse_date(soup)
    if not player_date:
        return None
    player = {"playerid": playerid,
                    "playername": parse_playername(soup),
                    "position": parse_position(soup),
                    "upgrade": parse_upgrade(soup),
                    "status": parse_status(soup),
                    "hall_of_fame": parse_halloffame(soup)
                    }
    return player

def parse_matchdata(data):
    coach = re.findall('coach[12]: \d*', data)
    matchdata = {
            "coach1": int(coach[0][7:]),
            "coach2": int(coach[1][7:])}
    return matchdata

def parse_fromfile(path, playerid):
    print("parse_from_file")
    LOG.debug(path, playerid)
    import player.load
    parsed_player = parse_player(playerid, soup=player.load.from_file("{}/admin-player-{}.html".format(path, playerid)))
    parsed_player = parse_games(parsed_player, soup=player.load.from_file("{}/player-{}.html".format(path, playerid)))
    parsed_player = parse_team(parsed_player, soup=player.load.from_file("{}/player-{}.html".format(path, playerid)))
    return parsed_player


def main():
    logging.basicConfig(level=logging.DEBUG)
    import pprint
    if len(sys.argv) != 3 :
            sys.exit("path and playerid required")
    path = sys.argv[1]
    playerid = sys.argv[2]

    parsed_player = parse_fromfile(path, playerid)

    pprint.PrettyPrinter(indent=4).pprint(parsed_player)

if __name__ == "__main__":
    main()
