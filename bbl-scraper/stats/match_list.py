#!/usr/bin/env python3
import dateutil
from operator import itemgetter
from copy import  copy
import logging

from match import match

LOG = logging.getLogger(__package__)


def game_streaks(games):
    streaks = {}
    streaks["gamestreak"] = playstreak(games)
    streaks["winstreak"] = eventstreak(games, 
            event = lambda x: x["home_result"] == "W", minimum=2)
    streaks["losstreak"] = eventstreak(games, 
            event = lambda x: x["home_result"] == "L", minimum=2)
    streaks["tiestreak"] = eventstreak(games, 
            event = lambda x: x["home_result"] == "T", minimum=2)
    streaks["nolosstreak"] = eventstreak(games, 
            event = lambda x: x["home_result"] == "T" or x["home_result"] == "W",
            minimum=streaks["winstreak"]+1) 
    streaks["killstreak"] = eventstreak(games, 
            event = lambda x: x["home_dead"] > 0, minimum=1)
    streaks["wonby2"] = eventstreak(games, 
            event = lambda x: x["home_td"] - x["away_td"] > 1, minimum=3)
    streaks["lostby2"] = eventstreak(games, 
            event = lambda x: x["home_td"] - x["away_td"] < -1, minimum=3)
    streaks["didnotscore"] = eventstreak(games, 
            event = lambda x: x["home_td"] == 0, minimum=2)
    streaks["shutoutstreak"] = eventstreak(games, 
            event = lambda x: x["away_td"] == 0, minimum=2)

    return streaks

def eventstreak(games, event, minimum=0):
    longest_streak = 0
    current_streak = 0
    for g in games:
        if event(g):
            current_streak = current_streak + 1
            if current_streak > longest_streak:
                longest_streak = current_streak
        else: 
            current_streak = 0
    if longest_streak < minimum:
        return 0
    return longest_streak

def favorite_day(games):
    days = [0,0,0,0,0,0,0]
    for g in games:
        date = dateutil.parser.parse(g['date'])
        days[date.weekday()] = days[date.weekday()] + 1

    best_day = days.index(max(days))
    days_of_week = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
    return "{}".format(days_of_week[best_day]) 

def playstreak(games):
    if len(games) < 1:
        return None

    best_score = {"count": 0, "days": 0 }
    current_score = {"count": 1, "days": 1}
    current_date = dateutil.parser.parse(games[0]["date"])

    for g in games[1:]:
        game_date = dateutil.parser.parse(g["date"])
        days_between_games = (current_date - game_date).days
        if days_between_games <= 1:
            current_score["count"] = current_score["count"] + 1
            if days_between_games == 1:
                current_score["days"] = current_score["days"] + 1
            if current_score["count"] > best_score["count"]:
                best_score = current_score
                if best_score["days"] == 0:
                    best_score["days"] = 1
        else:
            current_score = {"count": 1, "days": 1}
        current_date=game_date

    if best_score["count"] == 0 and best_score["days"] == 0:
        return None
    return best_score


def format_for_matchlist(match):
    return {"matchid": match["matchid"],
            "date": match["date"].split("T")[0],
            "repeated_date": False,
            "home": match["home_team"],
            "away": match["away_team"],
            "td_home": match["home_td"],
            "td_away": match["away_td"],
            "cas_home": match["home_cas"],
            "cas_away": match["away_cas"],
            "season": match["tournament_name"],
            "home_coach": match["home_coach"],
            "away_coach": match["away_coach"]
    }


def games_for_year(games, year=None):
    if not year:
        return games
    result = []
    start = "{}-00-00".format(year)
    end = "{}-99-99".format(year)

    result = list(
        filter(
            lambda x: x["date"] > start and end > x["date"], 
            games))
    #print("{} games".format(len(games)))
    return result


def games_for_teams(data, games):
    teams = {} 
    for g in games:
        teamid = g["home_teamid"]
        if teamid not in teams:
            teams[teamid] = data["team"][teamid]
            teams[teamid]["games"] = list(filter(lambda x: x["home_teamid"] == teamid, games))
            total = sum_game(teams[teamid]["games"])
            teams[teamid]["total"] = total["total"]
            teams[teamid]["average"] = total["average"]
             
    return teams

def sort_group_by_points(groups):
    games_for_team = sorted(groups, key=lambda g: g["title"])
    games_for_team = sorted(games_for_team, key=lambda g: g["data"]["total"]["cas_for"]+g["data"]["total"]["cas_against"], reverse=True)
    games_for_team = sorted(games_for_team, key=lambda g: g["data"]["total"]["td_for"]+g["data"]["total"]["td_against"], reverse=True)
    games_for_team = sorted(games_for_team, key=lambda g: g["data"]["total"]["win"], reverse=True)
    games_for_team = sorted(games_for_team, key=lambda g: g["data"]["total"]["gamesplayed"])
    games_for_team = sorted(games_for_team, key=lambda g: g["data"]["total"]["points"], reverse=True)
    
    return games_for_team


def games_by_weekday(games):
    games_by_weekday = sum_game_by_group(games, group_games_by_weekday)
    for w in games_by_weekday:
        w["order"] = w["title"]
        w["title"] = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"][w["title"]-1]
        w["link"] = None
    return sorted(games_by_weekday, key=lambda x: x["order"])

def group_games_by_weekday(games):
    return group_games(lambda x: dateutil.parser.parse(x["date"]).isoweekday(), games)

def group_games_by_coach(games, who="away"):
    return group_games(lambda x: x[who+"_coachid"], games)

def group_games_by_our_coach(games):
    return group_games_by_coach(games, who="home")

def group_games_by_race(games, who="away"):
    by_race = group_games(lambda x: x[who+"_race"], games)
    return by_race

def group_games(group, games):
    result = {}
    for g in games:
        grp = group(g)
        if grp not in result:
            result[grp] = []
        result[grp].append(g)

    return result

def sum_game_by_group(games, grouping):
    result = []
    for rac, g in grouping(games).items():
        result.append({"title": rac, "data": sum_game(g)})
    return sort_group_by_points(result)


def sum_game(games):
    total = {"gamesplayed": 0, "win":0, "tie":0, "loss": 0, 
                "td": 0,"td_for": 0, "td_against": 0, 
                "cas": 0, "cas_for": 0, "cas_against": 0, "dead_for": 0, "dead_against": 0,
                "points": 0, "performance": 0 } 
    average = copy(total)
    for g in games:
        total["gamesplayed"] = total["gamesplayed"] + 1
        total["td_for"] = total["td_for"] + g["home_td"]
        total["td_against"] = total["td_against"] + g["away_td"]
        total["cas_for"] = total["cas_for"] + g["home_cas"]
        total["cas_against"] = total["cas_against"] + g["away_cas"]
        total["dead_for"] = total["dead_for"] + g["home_dead"]
        total["dead_against"] = total["dead_against"] + g["away_dead"]

        if g["home_result"] == "W": total["win"] = total["win"] + 1
        if g["home_result"] == "T": total["tie"] = total["tie"] + 1
        if g["home_result"] == "L": total["loss"] = total["loss"] + 1
    
    total["points"] = total["win"]*5 + total["tie"]*3 + total["loss"]
    total["performance"] = 100 * ((total["win"]*2)+total["tie"])/(total["gamesplayed"]*2) if total["gamesplayed"] > 0 else 0
    total["td"] = total["td_for"] - total["td_against"]
    total["cas"] = total["cas_for"] - total["cas_against"]

    if total["gamesplayed"] > 0: 
        average = {"gamesplayed": len(games)/total["gamesplayed"], 
            "win":total["win"] / total["gamesplayed"], 
            "tie":total["tie"] / total["gamesplayed"], 
            "loss": total["loss"] / total["gamesplayed"], 
            "td_for": total["td_for"] / total["gamesplayed"], "td_against":  total["td_against"] / total["gamesplayed"], 
            "cas_for": total["cas_for"] / total["gamesplayed"], "cas_against": total["cas_against"] / total["gamesplayed"], 
            "dead_for": total["dead_for"] / total["gamesplayed"], "dead_against": total["dead_against"] / total["gamesplayed"], 
            "points": total["points"]/total["gamesplayed"], "performance": total["performance"] } 

    return {"total": total, "average": average}


def switch_homeaway(g):
    result = {}
    for k, v in g.items():
        if k.startswith("home_"):
            result["away"+k[4:]] = v
        elif k.startswith("away_"):
            result["home"+k[4:]] = v
        else:
            result[k] = v
    return result


#TODO Fix we_are_team for flat
def we_are_team(games, team):
    result = []
    for g in games:
        if g["home_teamid"] == team["id"]:
            result.append(g)
        elif g["away_teamid"] == team["id"]:
            result.append(switch_homeaway(g))

    return result


def we_are(games, what, what_away):
    result = []
    for g in games:
        if what(g):
            result.append(g)
        elif what_away(g):
            result.append(switch_homeaway(g))
    return result


def we_are_race(games, race):
    return we_are(games, lambda x: x["home_race"] == race, lambda x: x["away_race"] == race)


def we_are_coach(games, coach):
    result = []
    for g in games:
        if g["home_coachid"] == coach["uid"]:
            result.append(g)
        elif g["away_coachid"] == coach["uid"]:
            result.append(switch_homeaway(g))
    return result


def list_all_matches(data=None):
    matches = data["game"].values() if data else match.match_list()
    formatted_matches = list(map(format_for_matchlist, matches))
    
    return sorted(formatted_matches, key=itemgetter("date"), reverse=True)


def list_all_games_by_year(data, year):
    start_date = "{}-99-99".format(year-1)
    end_date = "{}-00-00".format(int(year)+1)
    return list(filter(lambda x: x["date"] > start_date and x["date"] < end_date, data["game"].values())) 


def print_list_all_matches():
    for t in list_all_matches():
        print(t)


def test_we_are_race():
    from . import collate
    all_matches = collate.collate()["game"].values()
    matches = we_are_team(all_matches, {"id":"mot"})

    LOG.debug("all_matches: %s, matches: %s", len(all_matches), len(matches))
    for m in matches:
        LOG.debug("print match %s", m["matchid"])
        print("{} {}({}) {}({}) {}".format( m["home_td"], m["home_team"], m["home_race"], m["away_team"], m["away_race"], m["away_td"]))


def test_we_are_coach():
    from . import collate
    all_matches = collate.collate()["game"].values()
    matches = we_are_coach(all_matches, {"uid": "71", "nick": "Kyrre"})

    LOG.debug("all_matches: %s, matches: %s", len(all_matches), len(matches))
    for m in matches:
        LOG.debug("print match %s", m["matchid"])
        print("{} {} {} {}".format( m["home_td"], m["home_team"], m["away_team"], m["away_td"]))


def main():
    import sys
    log_format = "[%(levelname)s:%(filename)s:%(lineno)s - %(funcName)20s ] %(message)s"
    logging.basicConfig(level=logging.DEBUG, format=log_format)

    if "--we-are-coach" in sys.argv:
        test_we_are_coach()
    elif "--we-are-race" in sys.argv:
        test_we_are_race()
    else:
        print_list_all_matches()



if __name__ == "__main__":
    main()
