#!/usr/bin/env python3
import dateutil
import datetime
from datetime import date
from operator import itemgetter
from copy import deepcopy

from match import match
from team import team
from coach import coach

from stats.match_list import list_all_matches
from stats.team_list import list_all_teams_by_year
from stats.team_list import list_all_teams_by_points
from stats.match_list import games_for_year, we_are_coach, sum_game, resultstreak, playstreak, favorite_day, eventstreak


def list_all_games_by_coach2(data, the_coach):
    coach_id = data["coach"][the_coach]["uid"]
    return [g for g in data["game"].values() if g["home"]["coachid"] == coach_id or g["away"]["coachid"] == coach_id]


def list_all_games_by_coach():
    return list_all_matches()

def coach_data(coach, coach_games):
    coach["last_game"] = coach_games[0]["date"] if len(coach_games) > 0 else "Never"
    coach["first_game"] = coach_games[-1]["date"] if len(coach_games) > 0 else None
    games_played = len(coach_games)
    coach["game_frequency"] ="Never"
    coach["gamesplayed_time"] = 0
    coach["favorite_day"] = favorite_day(coach_games)

    coach["gamestreak"] = playstreak(coach_games)
    coach["winstreak"] = eventstreak(coach_games, event = lambda x: x["us"]["result"] == "W", minimum=2)
    coach["losstreak"] = eventstreak(coach_games, event = lambda x: x["us"]["result"] == "L", minimum=2) 
    coach["tiestreak"] = eventstreak(coach_games, event = lambda x: x["us"]["result"] == "T", minimum=2)
    coach["nolosstreak"] = eventstreak(coach_games, event = lambda x: x["us"]["result"] == "T" or x["us"]["result"] == "W", minimum=coach["winstreak"]+1) 
    coach["killstreak"] = eventstreak(coach_games, event = lambda x: x["us"]["casualties"]["dead"] > 0, minimum=1) 
    coach["wonby2"] = eventstreak(coach_games, event = lambda x: x["us"]["td"] - x["them"]["td"] > 1, minimum=3) 
    coach["lostby2"] = eventstreak(coach_games, event = lambda x: x["us"]["td"] - x["them"]["td"] < -1, minimum=3) 
    coach["didnotscore"] = eventstreak(coach_games, event = lambda x: x["us"]["td"] == 0, minimum=2) 
    coach["shutoutstreak"] = eventstreak(coach_games, event = lambda x: x["them"]["td"] == 0, minimum=2) 

    coach["anbbl_rating"] = "N/A"
    if "elo" in coach:
        coach["anbbl_rating"] = "{:.1f}".format(150 + coach["elo"]["rating"])
    #coach["anbbl_rating"] = coach["elo"]["rating"]
    
    if(coach["first_game"]):
        first_game = dateutil.parser.parse(coach["first_game"])
        last_game = dateutil.parser.parse(coach["last_game"])
        

        days_since_first_game = (datetime.datetime.now() - first_game).days
        days_active = (last_game - first_game).days
        if (datetime.datetime.now() - last_game).days > 730:
            coach["game_frequency"] = "Stopped playing"
        elif (datetime.datetime.now() - last_game).days > 365:
            coach["game_frequency"] = "Rare"
        else:
            coach["game_frequency"] = "every {} days".format(round(abs(days_since_first_game)/games_played))
        if len(coach_games) > 1 and days_active > len(coach_games):
            coach["gamesplayed_time"] = len(coach_games) / days_active
        if len(coach_games) >= days_active:
            coach["gamesplayed_time"] = 1

    coach["gp"] = len(coach_games)
    
    return coach

def calculate_performance(gamesplayed, win, tie):
    if gamesplayed == 0:
        return 0
    return (((win*2)+(tie*1))/ (gamesplayed*2))*100

def calculate_points(the_team):
    return (the_team["win"]*5) + (the_team["tie"]*3) + (the_team["loss"]*1)
    

def format_for_coachlist(coachdata):
    return {"coachid": coachdata["nick"],
            "coachlink": coachdata["nick"].replace(" ", "-"),
            "login": coachdata["login"].split("T")[0],
            "first_game": coachdata["first_game"],
            "last_game": coachdata["last_game"],
            "name": coachdata["nick"],
            "gamesplayed": coachdata["gamesplayed"],
            "game_frequency": coachdata["game_frequency"],
            "gamesplayed_time": coachdata["gamesplayed_time"],
            "win": coachdata["win"],
            "tie": coachdata["tie"],
            "loss": coachdata["loss"],
            "td": coachdata["td"],
            "td_for": coachdata["td_for"],
            "td_against": coachdata["td_against"],
            "cas": coachdata["cas"],
            "cas_for": coachdata["cas_for"],
            "cas_against": coachdata["cas_against"],
            "performance": coachdata["performance"],
            "points": coachdata["points"],
            "winratio": coachdata["winratio"]
    }



def link_coach_to_games(the_coach, coaches, teams, games):
    name = the_coach["nick"]
    #print("{} {} {}".format(name, len(teams), len(list(games))))
    team_coach = list(filter(lambda x: x["coach"] == name, teams))
    teams_of_coach = list(map(lambda x: x["name"], team_coach))
    coach_games = list(
        filter(
            lambda x: x["home"] in teams_of_coach or x["away"] in teams_of_coach, 
            games))
    #print("{} {} {} {}".format(name, len(list(teams)), len(list(games)), len(list(coach_games))))

    the_coach["gamesplayed"] = sum(map(lambda x: x["gamesplayed"], team_coach))
    the_coach = coach_data(the_coach, coach_games)
    the_coach["win"] = sum(map(lambda x: x["win"], team_coach))
    the_coach["loss"] = sum(map(lambda x: x["loss"], team_coach))
    the_coach["tie"] = sum(map(lambda x: x["tie"], team_coach))
    the_coach["performance"] = calculate_performance( the_coach["gamesplayed"], the_coach["win"], the_coach["tie"])


    the_coach["td"]=sum(map(lambda x: x["td"], team_coach))
    the_coach["td_for"]=sum(map(lambda x: x["td_for"], team_coach))
    the_coach["td_against"]=sum(map(lambda x: x["td_against"], team_coach))
    the_coach["cas"]=sum(map(lambda x: x["cas"], team_coach))
    the_coach["cas_for"]=sum(map(lambda x: x["cas_for"], team_coach))
    the_coach["cas_against"]=sum(map(lambda x: x["cas_against"], team_coach))
    the_coach["points"] =sum(map(calculate_points, team_coach))
    the_coach["winratio"] = the_coach["win"] / the_coach["gamesplayed"] if the_coach["gamesplayed"] > 0 else 0


    #print(the_coach) 
    return the_coach

def link_coach_team_game(coaches, teams, games):
    all_coaches = []
    for c in coaches:
        the_coach = link_coach_to_games(c, coaches, teams, games)
        all_coaches.append(the_coach)

    return all_coaches

def list_all_coaches2(data = None, year = None):
    all_data = data
    if all_data == None:
        import stats.collate
        all_data = stats.collate.collate()

    result = []

    for the_coach in all_data["coach"].values():
        games = deepcopy(we_are_coach(all_data["game"].values(), the_coach))
        games = games_for_year(games, year)
        total = sum_game(games)
        the_coach["games"] = {"all": games, 
                "total": total["total"], 
                "average": total["average"]}
        the_coach["coachlink"] = the_coach["nick"].replace(" ","-")

        result.append(the_coach)
    return result
        



def list_all_coaches(coaches = None, games = None, teams = None):
    if games == None:
        games = list_all_matches()
    if coaches == None:
        coaches = coach.list_coaches()
    if teams == None:
        teams = list_all_teams_by_points()

    coaches = link_coach_team_game(coaches, teams, games)
    formatted_coaches = list(map(format_for_coachlist, coaches))
    
    sorted_coaches = sorted(formatted_coaches, key=itemgetter("gamesplayed"), reverse=True)  
    sorted_coaches = filter(lambda x: x["gamesplayed"] > 0, sorted(sorted_coaches, key=itemgetter("points"), reverse=True))
    return sorted(sorted_coaches, key=lambda x: x["gamesplayed"] >= 10, reverse = True)

def list_all_coaches_year(year):
    start = "{}-00-00".format(year)
    end = "{}-99-99".format(year)
    games = list(
        filter(
            lambda x: x["date"] > start and end > x["date"], 
            list_all_matches()))

    teams_by_year = list_all_teams_by_year(year)
    return list_all_coaches(teams=teams_by_year, games=games)


def main():
    import stats.collate
    data = stats.collate.collate()
    games = list_all_games_by_coach2(data, "Tango")
    for g in games:
        print("{} - {}".format(g["home"]["name"], g["away"]["name"]))
    #for coach in list_all_coaches():
        #print(coach)



