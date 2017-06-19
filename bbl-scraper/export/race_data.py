#!/usr/bin/env python3
from team import team
from stats.team_list import list_all_teams_by_points, list_all_games_by_race, list_all_teams_for_race, list_all_teams_by_year
from stats.match_list import list_all_matches, list_all_games_by_year
from stats.team_list import format_for_total, format_for_average
import datetime
from export import export


def all_games_by_race():
    return export.get_template("race/races.html").render(
        teams = filter(lambda x: x["gamesplayed"] > 25, list_all_games_by_race()),
        teams_in_need = filter(lambda x: x["gamesplayed"] <= 25, list_all_games_by_race()),
        title="All races",
        subtitle="sorted by performance")

def all_teams_for_race(race, race_teams):
    return export.get_template("race/teams-for-race.html").render(
        teams_average = format_for_average(race_teams),
        teams_total = format_for_total(race_teams),
        teams = race_teams, 
        title="All {} teams".format(race),
        subtitle="sorted by points")

def teams_by_race():
    race = team.list_race()    
    teams =  list_all_teams_by_points()
    for r in race:
        team_race = filter(lambda x: x["race"] == r, teams)
        with open("output/race/{}.html".format(r.replace(" ","-")), "w") as fp:
            fp.write(all_teams_for_race(r, list(team_race)))

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
    teams_by_race()
    

if __name__ == "__main__":
    main()
