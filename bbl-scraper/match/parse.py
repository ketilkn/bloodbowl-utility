#!/usr/bin/env python
"""  Parse match from HTML """
import re
import sys
import logging
import dateutil.parser as parser
import bs4

LOG = logging.getLogger(__package__)


def id_from_a(a):
    if a.has_attr("href"):
        return a["href"][a["href"].rfind("=") + 1:]
    if a.parent and a.parent.has_attr("href"):
        return a.parent["href"][a.parent["href"].rfind("=") + 1:]
    return "teamid not found {}".format(a.name)


def parse_team(prefix, team):
    team = {prefix+"team": team.text,
            prefix+"teamid": id_from_a(team)}
    return team


def convert_to_isodate(text):
    return parser.parse(text).isoformat()


def parse_date(soup):
    LOG.debug("Parsing date")
    found = soup.find_all("div")
    LOG.debug("Found {} potential divs".format(len(found)))
    for div in found:
        if "Result added" in div.text:
            LOG.debug("Found Result added")
            found_date = convert_to_isodate(div.text.strip()[13:])
            LOG.debug("Match date is %s", found_date)
            return found_date
    LOG.debug("Did not find date location.")
    return None


def parse_score(scoreboard):
    touchdowns = scoreboard.select("br")
    return len(touchdowns)


def parse_scoreboardelement(el):
    if el == "mercenary / star":
        return "*"
    elif el.has_attr("href") and el["href"].startswith("default.asp?p=pl&pid="):
        return int(el["href"][el["href"].rfind("=") + 1:])
    return el.has_attr("href")


def parse_scoreboard(scoreboard):
    LOG.debug("Parsing scoreboard")
    td = []
    for c in list(scoreboard.children):
        LOG.debug("Found {}".format(c))
        if type(c) == bs4.NavigableString:
            LOG.debug("NavigatableString")
            continue
        el = parse_scoreboardelement(c)
        LOG.debug("scoreboard el {}".format(el))
        if el:
            td.append(el)
    return td


def parse_td(soup):
    scoreboard = soup.select('tr[style="background-color:#f4fff4"] td')

    return {"home": parse_scoreboard(scoreboard[0]),
            "away": parse_scoreboard(scoreboard[2])}


def parse_casualtyspp(soup):
    return {"home": [],
            "away": [],
            }


def parse_injury_column(column):
    LOG.debug("injury el {}".format(column))

    return parse_scoreboard(column)


def parse_injury_row(soup, search):
    LOG.debug("Searching for {}".format(search))
    found = soup.select(search)
    LOG.debug("found len %s", len(found))
    injuries = []
    for row in found:
        LOG.debug("row el %s", row)
        injuries.extend(parse_injury_column(row.select("td")[0]))
        LOG.debug("injury type: %s", row.select("td")[1].text)
        injuries.extend(parse_injury_column(row.select("td")[2]))

    return [injured for injured in injuries if injured]


def parse_injuries(soup):
    LOG.debug("INJURIES")

    dead = parse_injury_row(soup, "tr[style='background-color:#f4d2d2']")
    mng = parse_injury_row(soup, "tr[style='background-color:#f2e2da']")
    niggle = parse_injury_row(soup, "tr[style='background-color:#f0d8d4']")
    return {"dead": dead,
            "seriousinjuries": mng + niggle}


def parse_spp(soup):
    td = parse_td(soup)
    cas = parse_casualtyspp(soup)
    return {"td": td,
            "cas": cas, }


def find_score(soup):
    scoreboard = soup.select('tr[style="background-color:#f4fff4"]')[0]
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

    return {"home_cas": home, "home_bh": bh["home"], "home_si": si["home"], "home_dead": de["home"],
            "away_cas": away, "away_bh": bh["away"], "away_si": si["away"], "away_dead": de["away"]}


def find_hometeam(soup):
    # print("[[[{}]]]".format(soup.find_all("b")[2].parent))
    return parse_team("home_", soup.find_all("b")[2])


def find_awayteam(soup):
    el = soup.findAll("td", {"width": "180"})
    return parse_team("away_", el[1].select_one("a"))


def parse_season(soup):
    season = soup.select_one("td[valign=top] div[align=center] b")
    season_name, round_name = season.text.split(",", 1)
    season_id = season.select_one("a")["href"].split("=")[-1] if season.select_one("a") else None

    return {"tournament_id": season_id, "tournament_name": season_name.strip(), "round": round_name.strip()}


def parse_notes(soup):
    LOG.debug("parsing notes")

    notes = soup.select_one("td[style='width:460px;text-align:justify;']")
    LOG.debug("notes len %s", len(notes.text) if notes else "Not found!")

    return notes.text.replace('\xa0', ' ')


def parse_match(matchid, soup):
    def calculate_result(us, them):
        if us > them:
            return "W"
        elif us < them:
            return "L"
        return "T"
    LOG.debug("Parse match {}".format(matchid))
    if not soup.findAll("h1", text="Match result"):
        return False
    game_date = parse_date(soup)
    if not game_date:
        LOG.warning("No game_date in file with match id: %s", matchid)
        match = {"approved": False}
        match.update(find_hometeam(soup))
        match.update(find_awayteam(soup))
        return match

    td_home = find_score(soup)["home"]
    td_away = find_score(soup)["away"]
    match = {"matchid": matchid,
             "date": game_date,
             "approved": True,
             "home_td": find_score(soup)["home"],
             "home_result": calculate_result(td_home, td_away),
             "away_td": td_away,
             "away_result": calculate_result(td_away, td_home),
             "spp": parse_spp(soup),
             "injuries": parse_injuries(soup),
             "notes": parse_notes(soup)
             }

    match.update(find_hometeam(soup))
    match.update(find_awayteam(soup))
    match.update(find_casualties(soup))
    match.update(parse_season(soup))
    return match


def parse_matchdata(data):
    coach = re.findall('coach[12]: \d*', data)
    matchdata = {
        "coach1": coach[0][7:].strip(),
        "coach2": coach[1][7:].strip()}
    return matchdata


def load_from_file(filename):
    import match.load as loader
    LOG.info("Parsing {}".format(filename))
    match_id = filename[filename.find("match-") + 6:filename.rfind(".html")]
    LOG.debug("match_id: {}".format(match_id))

    match = parse_match(match_id, loader.from_file(filename))
    return match


def main():
    log_format = "[%(levelname)s:%(filename)s:%(lineno)s - %(funcName)20s ] %(message)s"
    logging.basicConfig(level=logging.DEBUG, format=log_format)

    import pprint
    pp = pprint.PrettyPrinter(indent=2)
    if len(sys.argv) != 2:
        sys.exit("filename required")
    filename = sys.argv[1]

    match = load_from_file(filename)
    pp.pprint(match)


if __name__ == "__main__":
    main()
