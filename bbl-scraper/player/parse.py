#!/usr/bin/env python
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

def parse_games(player, soup):
    player["spp"] =  {"interception":0, "td":0, "casualty": 0, "completion": 0, "mvp": 0} 
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

def parse_permanent(soup):
    return soup.select_one("input[name=inj]")["value"]

def parse_injury(soup): 
    return  {"niggle": parse_niggle(soup),
            "permanent": parse_permanent(soup)}

def parse_niggle(soup):
    return int(soup.select_one("select[name=n] option[selected]")["value"])

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
                    "upgrade": parse_upgrade(soup),
                    "injury": parse_injury(soup),
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
