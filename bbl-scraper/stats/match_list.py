#!/usr/bin/env python3
import dateutil
import datetime
from datetime import date
from operator import itemgetter
from copy import deepcopy, copy

from match import match
from team import team
from coach import coach

def game_streaks(games):
    streaks = {}
    streaks["gamestreak"] = playstreak(games)
    streaks["winstreak"] = eventstreak(games, 
            event = lambda x: x["us"]["result"] == "W", minimum=2)
    streaks["losstreak"] = eventstreak(games, 
            event = lambda x: x["us"]["result"] == "L", minimum=2) 
    streaks["tiestreak"] = eventstreak(games, 
            event = lambda x: x["us"]["result"] == "T", minimum=2)
    streaks["nolosstreak"] = eventstreak(games, 
            event = lambda x: x["us"]["result"] == "T" or x["us"]["result"] == "W", 
            minimum=streaks["winstreak"]+1) 
    streaks["killstreak"] = eventstreak(games, 
            event = lambda x: x["us"]["casualties"]["dead"] > 0, minimum=1) 
    streaks["wonby2"] = eventstreak(games, 
            event = lambda x: x["us"]["td"] - x["them"]["td"] > 1, minimum=3) 
    streaks["lostby2"] = eventstreak(games, 
            event = lambda x: x["us"]["td"] - x["them"]["td"] < -1, minimum=3) 
    streaks["didnotscore"] = eventstreak(games, 
            event = lambda x: x["us"]["td"] == 0, minimum=2) 
    streaks["shutoutstreak"] = eventstreak(games, 
            event = lambda x: x["them"]["td"] == 0, minimum=2) 

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
            "home": match["home"]["team"]["name"],
            "away": match["away"]["team"]["name"],
            "td_home": match["home"]["td"],
            "td_away": match["away"]["td"],
            "cas_home": match["home"]["casualties"]["total"],
            "cas_away": match["away"]["casualties"]["total"],
            "season": match["season"]["season"]
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
        if "us" not in g: continue
        teamid = g["us"]["team"]["teamid"]
        if teamid not in teams:
            teams[teamid] = data["team"][teamid]
            teams[teamid]["games"] = list(filter(lambda x: x["us"]["team"]["teamid"] == teamid, games))
            total = sum_game(teams[teamid]["games"])
            teams[teamid]["total"] = total["total"]
            teams[teamid]["average"] = total["average"]
             
    return teams
    
def sum_game(games):
    total = {"gamesplayed": 0, "win":0, "tie":0, "loss": 0, 
                "td": 0,"td_for": 0, "td_against": 0, 
                "cas": 0, "cas_for": 0, "cas_against": 0, "dead_for": 0, "dead_against": 0,
                "points": 0, "performance": 0 } 
    average = copy(total)
    for g in games:
        if "us" not in g: continue
        total["gamesplayed"] = total["gamesplayed"] + 1
        total["td_for"] = total["td_for"] + g["us"]["td"]
        total["td_against"] = total["td_against"] + g["them"]["td"]
        total["cas_for"] = total["cas_for"] + g["us"]["casualties"]["total"]
        total["cas_against"] = total["cas_against"] + g["them"]["casualties"]["total"]
        total["dead_for"] = total["dead_for"] + g["us"]["casualties"]["dead"]
        total["dead_against"] = total["dead_against"] + g["them"]["casualties"]["dead"]

        if g["us"]["result"] == "W": total["win"] = total["win"] + 1
        if g["us"]["result"] == "T": total["tie"] = total["tie"] + 1
        if g["us"]["result"] == "L": total["loss"] = total["loss"] + 1
    
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


def we_are_team(games, team):
    result = []
    for g in games:
        if g["home"]["team"]["teamid"] == team["id"]:
            g["us"] = g["home"]
            g["them"] = g["away"]
            result.append(g)
        elif g["away"]["team"]["teamid"] == team["id"]:
            g["us"] = g["away"]
            g["them"] = g["home"]
            result.append(g)

    return result


def we_are_coach(games, coach):
    result = []
    for g in games:
        if g["home"]["coachid"] == coach["uid"]:
            g["us"] = g["home"]
            g["them"] = g["away"]
            result.append(g)
        elif g["away"]["coachid"] == coach["uid"]:
            g["us"] = g["away"]
            g["them"] = g["home"]
            result.append(g)

    return result


def list_all_matches():

    matches = match.match_list()
    formatted_matches = list(map(format_for_matchlist, matches))
    
    return sorted(formatted_matches, key=itemgetter("date"), reverse=True)

def list_all_games_by_year(year):
    start_date = "{}-99-99".format(year-1)
    end_date = "{}-00-00".format(int(year)+1)
    return list(filter(lambda x: x["date"] > start_date and x["date"] < end_date, list_all_matches())) 


def main():
    for t in list_all_matches():
        print(t)


if __name__ == "__main__":
    main()
