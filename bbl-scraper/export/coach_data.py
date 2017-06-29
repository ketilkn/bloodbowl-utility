#!/usr/bin/env python3
from copy import deepcopy

from match import match
from team import team
from coach import coach

from stats import coach_list
from stats import team_list
from stats import match_list
import stats.elo

from export import export
import dateutil.parser
from datetime import date
from stats.collate import collate
import datetime


def all_teams_for_coach(data, coach, coach_teams, coach_games):
    game_total = match_list.sum_game(coach_games) 
    streaks = match_list.game_streaks(coach_games)
    streaks.update(coach_list.coach_streaks(coach_games))
    games_by_race = match_list.sum_game_by_group(coach_games, match_list.group_games_by_race)
    games_by_coach = match_list.sum_game_by_group(coach_games, match_list.group_games_by_coach)

    #FIXME. group_games_by_coach should return proper coach
    for c in games_by_coach:
        if c["title"] in data["_coachid"]:
            c["title"] = data["_coachid"][c["title"]]["nick"] 
            c["link"] = "/coach/{}.html".format(c["title"].replace(" ","-"))
        else:
            c["title"] = "Unknown {}".format(c["title"])
            c["link"] = "/coaches.html"


    return export.get_template("coach/coach.html").render(
        coach_name = coach["nick"],
        coach = coach_list.coach_data(coach, coach_games),
        streaks = streaks,
        games_by_race = games_by_race,
        games_by_coach = games_by_coach,
        more_games = len(coach_games) - 10,
        teams = coach_teams,
        stats_average = game_total["average"],
        stats_total = game_total["total"], 
        games = coach_games[:10],
        title="{}".format(coach["nick"]) 
        )

def teams_by_coach(data):
    coaches = coach.list_coaches()    
    teams =  sorted(team_list.list_all_teams_by_points(data["game"].values()), key=lambda x: x["gamesplayed"], reverse=True)
    
    add_elo(data)
    #games = list_all_games_by_coach()


    for c in coaches:
        name = c["nick"]

        if name in data["coach"] and "elo" in data["coach"][name]:
            c["elo"] = data["coach"][name]["elo"]
           
        cgames = list( sorted( coach_list.list_all_games_by_coach2(data, name), key=lambda x: int(x["matchid"]), reverse=True))
        cgames = list( sorted( cgames, key=lambda x: x["date"], reverse=True))
        cgames = deepcopy(match_list.we_are_coach(cgames, c))

        team_coach = list(sorted(match_list.games_for_teams(data, cgames).values(), key=lambda x: x["name"]))
        team_coach = sorted(team_coach, key=lambda x: x["total"]["performance"], reverse = True)
        team_coach = sorted(team_coach, key=lambda x: x["total"]["gamesplayed"], reverse = True)

        with open("output/coach/{}.html".format(name.replace(" ","-")), "w") as fp:
            fp.write(all_teams_for_coach(data, c, team_coach, cgames))

        with open("output/coach/{}-games.html".format(name.replace(" ","-")), "w") as fp:
            fp.write(export.get_template("coach/coach-games.html").render(
                coach = c,
                games = cgames,
                title = "All games by {}".format(name)))

def all_coaches_by_year(data, start = 2007, end = datetime.datetime.now().year+1):
    import stats.collate
    #data = stats.collate.collate()
    for year in range(2007, end):
        coaches = coach_list.list_all_coaches2(data = data, year=year)
        #print( "{} coaches {} ".format(year, len(coaches)))
        coaches = [c for c in coaches if c["games"]["total"]["gamesplayed"] > 0]
        coaches = sorted(coaches, key=lambda x: x["nick"])
        coaches = sorted(coaches, key=lambda x: x["games"]["total"]["cas"], reverse=True)
        coaches = sorted(coaches, key=lambda x: x["games"]["total"]["td"], reverse=True)
        coaches = sorted(coaches, key=lambda x: x["games"]["total"]["gamesplayed"], reverse=True)
        coaches = sorted(coaches, key=lambda x: x["games"]["total"]["performance"], reverse=True)
        coaches = sorted(coaches, key=lambda x: x["games"]["total"]["points"], reverse=True)
        #print( "{} coaches {} ".format(year, len(coaches)))
        with open("output/coaches-{}.html".format(year), "w") as fp:
            fp.write(export.get_template("coach/all_coaches2.html").render(
                coaches=coaches, title="All coaches in {}".format(year)))

def add_elo(data):
    rating = stats.elo.rate_all(data)
    coaches_by_uid = data["_coachid"]()

    for rate in rating.values():
        if rate["cid"] in coaches_by_uid:
            nick = coaches_by_uid[rate["cid"]]["nick"]
            if nick in data["coach"]:
                data["coach"][nick]["elo"] = rate
    return data

def all_coaches(data):
    coaches = coach_list.list_all_coaches2(data)
    add_elo(data)
    coaches = [c for c in coaches if c["games"]["total"]["gamesplayed"] > 0]
    coaches = sorted(coaches, key=lambda x: x["games"]["total"]["td"], reverse=True)
    coaches = sorted(coaches, key=lambda x: x["games"]["total"]["performance"], reverse=True)
    coaches = sorted(coaches, key=lambda x: x["games"]["total"]["points"], reverse=True)
    #coaches = sorted(coaches, key=lambda x: x["elo"]["rating"], reverse=True)

    with open("output/coaches.html", "w") as fp:
        fp.write(export.get_template("coach/all_coaches2.html").render(
            display_rating=True, coaches=coaches, title="All AnBBL coaches through all time"))


def doExport():
    import stats.collate
    collated_data = stats.collate.collate()

    print("Exporting all coaches")
    all_coaches(collated_data)
    print("Exporting teams by coach")
    teams_by_coach(collated_data)
    print("Export year by coach")
    all_coaches_by_year(collated_data)

def main():
    doExport()
if __name__ == "__main__":
    main()
