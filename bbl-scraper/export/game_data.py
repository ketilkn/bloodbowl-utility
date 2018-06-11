#!/usr/bin/env python3
"""Write all game data to disk using jinja2 templates"""
import datetime
from team import team
from stats.team_list import list_all_teams_by_points, list_all_games_by_race
from stats.match_list import list_all_matches, list_all_games_by_year
from stats.team_list import format_for_total, format_for_average
from export import export, coach_data, race_data

from export import index

def all_games_by_year(data, year):
    return export.get_template("game/all_games.html").render(
        matches = list_all_games_by_year(data, year), 
        title="All games in {}".format(year),
        subtitle="sorted by date")

def all_games(data):
    games = list_all_matches(data)
    return export.get_template("game/all_games.html").render(
        matches = games, 
        title="All games",
        subtitle="sorted by date")


def games_by_year(data, start, end):
    games = list_all_matches(data)
    for year in range(start, end): 
        with open("output/games-{}.html".format(year), "w") as teams:
            teams.write(all_games_by_year(data, year))

def export_games_by_date(data):
    with open("output/games.html", "w") as matches:
        matches.write(all_games(data))

def main():
    import stats.collate
    collated_data = stats.collate.collate()

    print("Exporting games by date")
    with open("output/games.html", "w") as matches:
        matches.write(all_games(collated_data))

    print("Exporting games by year")
    games_by_year(collated_data, 2007, datetime.datetime.now().year+1)
    


if __name__ == "__main__":
    main()
