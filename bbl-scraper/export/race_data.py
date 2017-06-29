#!/usr/bin/env python3
from team import team
from stats.team_list import list_all_teams_by_points, list_all_games_by_race
from stats.match_list import list_all_matches, list_all_games_by_year
from stats.team_list import format_for_total, format_for_average
from stats import match_list
import datetime
from export import export


def all_games_by_race():
    return export.get_template("race/races.html").render(
        teams = filter(lambda x: x["gamesplayed"] > 25, list_all_games_by_race()),
        teams_in_need = filter(lambda x: x["gamesplayed"] <= 25, list_all_games_by_race()),
        title="All races",
        subtitle="sorted by performance")

def all_teams_for_race(race, race_teams, performance_by_race):
    return export.get_template("race/teams-for-race.html").render(
        teams_average = format_for_average(race_teams),
        teams_total = format_for_total(race_teams),
        teams = race_teams,
        games_by_race = performance_by_race,
        title="All {} teams".format(race),
        subtitle="sorted by points")

def teams_by_race(data):
    race = team.list_race()    
    teams =  list_all_teams_by_points()
    for r in race:
        team_race = filter(lambda x: x["race"] == r, teams)
        
        race_games = match_list.we_are_race(data["game"].values(), r)
        performance_by_race = match_list.sum_game_by_group(race_games, match_list.group_games_by_race)

        with open("output/race/{}.html".format(r.replace(" ","-")), "w") as fp:
            fp.write(all_teams_for_race(r, list(team_race), performance_by_race))

def export_race_by_performance(data = None):
    with open("output/races.html", "w") as matches:
        matches.write(all_games_by_race())

def main():
    import stats.collate
    collated_data = stats.collate.collate()

    print("Exporting races by performance")
    with open("output/races.html", "w") as matches:
        matches.write(all_games_by_race())

    print("Exporting teams by race")
    teams_by_race(collated_data)
    

if __name__ == "__main__":
    main()
