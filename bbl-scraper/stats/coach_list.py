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
from stats.match_list import games_for_year, we_are_coach, sum_game, favorite_day
from stats.match_list import playstreak
from stats import match_list

def eventstreak(games, event, minimum=0):
    if len(games) < 1:
        return 0
    longest_streak = 0
    current_streak = 0
    previous_game = games[0]
    for g in games[1:]:
        #if g["us"]["coachid"] == 74:
            #print("\n====")
            #print(g["date"])
            #print(g["us"])
            #print(g["them"])
            #print("\n")
        if event(g, previous_game):
            if longest_streak == 0 and current_streak == 0:
                current_streak = 1
            current_streak = current_streak + 1 
            if current_streak > longest_streak:
                longest_streak = current_streak
        else: 
            current_streak = 0
        previous_game = g
    if longest_streak < minimum:
        return 0
    return longest_streak

def coach_streaks(games):
    streaks = {}

    streaks["sameteam"] = eventstreak(games,
            event = lambda x, y: y["home_teamid"] == x["home_teamid"],
            minimum=2)
    streaks["differentteam"] = eventstreak(games, 
            event = lambda x, y : y["home_teamid"] != x["home_teamid"],
            minimum=2)

    streaks["sameopponent"] = eventstreak(games, 
            event = lambda x, y: y["away_teamid"]== x["away_teamid"],
            minimum=2)
    streaks["differentopponent"] = eventstreak(games, 
            event = lambda x, y : y["away_teamid"] != x["away_teamid"],
            minimum=2)

    streaks["sameopponentcoach"] = eventstreak(games, 
            event = lambda x, y: x["away_coachid"]== y["away_coachid"],
            minimum=2)
    streaks["differentopponentcoach"] = eventstreak(games, 
            event = lambda x, y : x["away_coachid"]!= y["away_coachid"],
            minimum=2)


    return streaks

def list_all_games_by_coach2(data, the_coach):
    coach_id = data["coach"][the_coach]["uid"]
    return [g for g in data["game"].values() if g["home_coachid"] == coach_id or g["away_coachid"] == coach_id]

def coach_data(coach, coach_games):
    coach["last_game"] = coach_games[0]["date"] if len(coach_games) > 0 else "Never"
    coach["first_game"] = coach_games[-1]["date"] if len(coach_games) > 0 else None
    games_played = len(coach_games)
    coach["game_frequency"] ="Never"
    coach["gamesplayed_time"] = 0
    coach["favorite_day"] = favorite_day(coach_games)

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

def main():
    import stats.collate
    data = stats.collate.collate()
    games = list_all_games_by_coach2(data, "Tango")
    for g in games:
        print("{} - {}".format(g["home_name"], g["away_name"]))
    #for coach in list_all_coaches():
        #print(coach)



