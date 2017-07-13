#!/usr/bin/env python
from bs4 import BeautifulSoup
from unicodedata import normalize
import datetime
import dateutil.parser as parser
import re
#import team 
import sys


def parse_date(soup):
    return "1977-01-01 00:00:01"

def parse_bounties(soup):
    return -1

def parse_games(player, soup):
    player["spp"] =  {"interception":0, "td":0, "casualty": 0, "completion": 0, "mvp": 0} 
    return player

def parse_playername(soup):
    return soup.select("input[name=name]")[0]["value"]
    return "Playername"

def parse_position(soup):
    return "the Position"

def parse_skills(soup):
    return ["Skill"]

def parse_spp(soup):
    return ["spp"]
def parse_player(playerid, soup):
    player_date = parse_date(soup)
    if not player_date:
        return None
    player = {"playerid": playerid,
                    "date": player_date, 
                    "playername": parse_playername(soup),
                    "position": parse_position(soup),
                    "skills": parse_skills(soup),
                    "points": parse_spp(soup)
                    }
    return player

def parse_matchdata(data):
    coach = re.findall('coach[12]: \d*', data)
    matchdata = {
            "coach1": int(coach[0][7:]),
            "coach2": int(coach[1][7:])}
    return matchdata

def main():
    import player.load
    if len(sys.argv) != 2 :
            sys.exit("filename required")
    filename = sys.argv[1]
    playerid = filename[filename.find("adminplayer-")+6:filename.rfind(".html")]

    player = parse_player(playerid, soup=player.load.from_file(filename))
    #player = parse_games(player, load.from_file(spp))
    print(player)

if __name__ == "__main__":
    main()
