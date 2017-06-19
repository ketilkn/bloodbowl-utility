#!/usr/bin/env python3
from jinja2 import Template
import jinja2
from match import match
from stats import team_list 
from stats import match_list
from export import export, coach_data, race_data
from team import team

from export import index
import datetime

def all_games_by_team():
    teams = team.list_teams()
    games = match_list.list_all_matches() 
    for t in teams:
        team_games = list(filter(lambda x: x["home"] == t["name"] or x["away"] == t["name"] , games) )
        export.write_html(export.get_template("team/team.html").render(
            matches=team_games, teamname = t["name"], teamid = t["id"], title="All games by {}".format(t["name"],
            subtitle="sorted by date")), "team/{}".format(t["id"]))

def all_teams_by_year(year):
    teams = team_list.list_all_teams_by_year(year) 
    return export.get_template("team/all_team.html").render(
        teams_average = team_list.format_for_average(teams),
        teams_total = team_list.format_for_total(teams),
        teams =teams, 
        title="All teams in {}".format(year),
        subtitle="sorted by points")

def all_teams():
    teams = team_list.list_all_teams_by_points() 
    return export.get_template("team/all_team.html").render(
        teams_average = team_list.format_for_average(teams),
        teams_total = team_list.format_for_total(teams),
        teams = team_list.list_all_teams_by_points(), 
        title="All teams",
        subtitle="sorted by points")

def teams_by_year(start, end):
    for year in range(start, end): 
        with open("output/team-{}.html".format(year), "w") as teams:
            teams.write(all_teams_by_year(year))


def export_all_teams():
    with open("output/team.html", "w") as teams:
        teams.write(all_teams())



def main():
    import stats.collate
    collated_data = stats.collate.collate()

    print("Exporting all teams")
    all_games_by_team()

    print("Exporting teams by points")
    with open("output/team.html", "w") as teams:
        teams.write(all_teams())

    print("Exporting teams by year")
    teams_by_year(2007, datetime.datetime.now().year+1)

    index.index()
if __name__ == "__main__":
    main()
