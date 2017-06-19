#!/usr/bin/env python3
"""Run the entire process of generating stats and exporting to HTML. Run from commandline or as an import.
Progess is written to stdout using print"""
import datetime

from export import game_data, coach_data, race_data, index, team_data

def export_all_data():
    """Export all data to HTML"""
    import stats.collate
    collated_data = stats.collate.collate()

    print("Exporting all data")
    print("Exporting teams by points")
    team_data.export_all_teams()

    print("Exporting teams by year")
    team_data.teams_by_year(2007, datetime.datetime.now().year+1)

    print("Exporting games by date")
    game_data.export_games_by_date()

    print("Exporting games by year")
    game_data.games_by_year(2007, datetime.datetime.now().year+1)

    print("Exporting games by team")
    team_data.all_games_by_team()

    print("Exporting races by performance")
    race_data.export_race_by_performance()

    print("Exporting teams by race")
    race_data.teams_by_race()

    print("Exporting coach")
    coach_data.teams_by_coach(collated_data)

    print("Exporting coaches")
    coach_data.all_coaches(collated_data)
    print("Exporting coaches by year")
    coach_data.all_coaches_by_year(collated_data)

    print("Exporting index")
    index.index()

def main():
    """Run from commandline. Add --rsync to copy data to server"""
    import sys
    export_all_data()


if __name__ == "__main__":
    main()
