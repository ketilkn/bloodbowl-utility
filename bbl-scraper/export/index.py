#!/usr/bin/env python3
"""Create index file for dataset. Require template index.html"""
import datetime

from team import team
from coach import coach
from stats.match_list import list_all_matches
from export import  export

def create_index(data):
    """Create and return a template containing site index"""
    games = list_all_matches(data)
    coaches = coach.list_coaches()
    teams = team.list_teams()
    time_of_update = '{0:%Y-%m-%d %H:%M}'.format(datetime.datetime.now())

    return export.get_template("index.html").render(
        time_of_update=time_of_update,
        number_of_coaches=len(coaches),
        number_of_teams=len(teams),
        number_of_games=len(games),
        latest_games=games[:10]
        )

def index():
    """create_index and write file to disk"""

    import stats.collate
    collated_data = stats.collate.collate()

    """create_index and write file to disk"""
    with open("output/index.html", "w") as filepointer:
        filepointer.write(create_index(collated_data))

if __name__ == "__main__":
    print("Exporting index")
    index()
