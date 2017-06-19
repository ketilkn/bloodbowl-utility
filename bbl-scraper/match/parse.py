#!/usr/bin/env python
from bs4 import BeautifulSoup
from unicodedata import normalize
import datetime
import dateutil.parser as parser
import re
#import team 
import sys

def id_from_a(el):
    a = el.parent.parent.parent
    if a.has_attr("href"):
        return a["href"][a["href"].rfind("=")+1:]
    if a.parent and a.parent.has_attr("href"):
        return a.parent["href"][a.parent["href"].rfind("=")+1:]
#    print(el)
#    print("===")
#    print(a)
    return "teamid not found {}".format(a.name)

def parse_team(team):
        team = { "name": team.text,
                 "teamid": id_from_a(team) }
        return team
def convert_to_isodate(text):
        return parser.parse(text).isoformat()

def parse_date(soup):
        found = soup.find_all("div")
        for div in found:
                if div.has_attr("align") and div.text.startswith("Result added"):
                        return convert_to_isodate(div.text.strip()[13:])
        return None

def parse_score(scoreboard):
    touchdowns = scoreboard.select("br")
    return len(touchdowns) 


def find_score(soup):
    scoreboard = soup.select('tr[style="background-color:#f4fff4"]')[0]
    #print("\n{}\n".format(scoreboard.select(".td10")[0].prettify()))
    #print("\n{}\n".format(scoreboard.select(".td10")[1].prettify()))
    return {"home": parse_score(scoreboard.select(".td10")[0]), "away": parse_score(scoreboard.select(".td10")[1])}
def parse_casualty(soup):
    home = len(soup.select(".td10")[0].select("br")) 
    away = len(soup.select(".td10")[1].select("br")) 
    return {"home": home, "away": away} 
def find_casualties(soup):
    bh = parse_casualty(soup.select('tr[style="background-color:#fcfcf0"]')[0])
    si = parse_casualty(soup.select('tr[style="background-color:#fff9f0"]')[0])
    de = parse_casualty(soup.select('tr[style="background-color:#fff4f4"]')[0])
    home = bh["home"] + si["home"] + de["home"]
    away = bh["away"] + si["away"] + de["away"]

    return {"home": {"total": home,"bh": bh["home"], "si": si["home"], "dead": de["home"]},
            "away": {"total": away, "bh": bh["away"], "si": si["away"], "dead": de["away"]}}

def find_hometeam(soup):
    return parse_team(soup.find_all("b")[2])

def find_awayteam(soup):
        el = soup.find_all("b")[6] 
        if el.text == "overtime" :
            if soup.find_all("b")[7].text == "shoot-out":
                return parse_team(soup.find_all("b")[8])
            return parse_team(soup.find_all("b")[7])
        return parse_team(el)

def parse_season(soup):
    season = soup.select_one("div[align=right] b")
    season_name , round_name = season.text.split(",", 1)
    season_id = season.select_one("a")["href"].split("=")[-1] if season.select_one("a") else None

    return {"id": season_id, "season": season_name.strip(), "round": round_name.strip()}

def parse_match(matchid, soup):
    def calculate_result(us, them):
        if us > them:
            return "W"
        elif us < them:
            return "L"
        return "T"

    game_date = parse_date(soup)
    if not game_date:
        return None
    td_home = find_score(soup)["home"]
    td_away = find_score(soup)["away"]
    match = {"matchid": matchid,
                    "date": game_date, 
                    "season": parse_season(soup),
                    "approved": False,
                    "home":  {
                        "team": find_hometeam(soup),
                        "td": find_score(soup)["home"],
                        "result": calculate_result(td_home, td_away),
                        "casualties": find_casualties(soup)["home"]
                    },
                    "away": {
                        "team": find_awayteam(soup),
                        "td": td_away,
                        "result": calculate_result(td_away, td_home),
                        "casualties": find_casualties(soup)["away"]
                    }}
    return match

def parse_matchdata(data):
    coach = re.findall('coach[12]: \d*', data)
    matchdata = {
            "coach1": int(coach[0][7:]),
            "coach2": int(coach[1][7:])}
    return matchdata

def main():
        import match.load
        if len(sys.argv) != 2 :
                sys.exit("filename required")
        filename = sys.argv[1]
        matchid = filename[filename.find("match-")+6:filename.rfind(".html")]

        match = parse_match(matchid, load.from_file(filename))
        print(match)

if __name__ == "__main__":
    main()
