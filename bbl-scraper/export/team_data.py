#!/usr/bin/env python3
from match import match
from stats import team_list 
from stats import match_list
from stats import coach_list
from export import export, coach_data, race_data
from team import team

from export import index
import datetime


#coach = coach_list.coach_data(coach, coach_games),

def team_stats(data, teams, games, the_team):
    #team_data = coach_list.coach_data(the_team, data)


    games_for_team = match_list.we_are_team(list(data["game"].values()), the_team)

    games_for_team = sorted(games_for_team, key=lambda g: int(g["matchid"]), reverse=True)
    games_for_team = sorted(games_for_team, key=lambda g: g["date"], reverse=True)

    game_total = match_list.sum_game(games_for_team)
    streaks = match_list.game_streaks(games_for_team)
    

    games_by_race = match_list.sum_game_by_group(games_for_team, match_list.group_games_by_race)

    games_by_our_coach = match_list.sum_game_by_group(games_for_team, match_list.group_games_by_our_coach) 
    #FIXME, improve nick lookup
    for c in games_by_our_coach:
        if c["title"] in data["_coachid"]:
            c["title"] = data["_coachid"][c["title"]]["nick"] 
            c["link"] = "/coach/{}.html".format(c["title"].replace(" ","-"))
        else:
            c["title"] = "Unknown {}".format(c["title"])
            c["link"] = "/coaches.html"

    export.write_html(export.get_template("team/team.html").render(
            stats_average = game_total["average"],
            stats_total = game_total["total"], 
            matches=games_for_team,
            games_by_race = games_by_race,
            games_by_our_coach = games_by_our_coach,
            show_coaches = len(games_by_our_coach) > 1,
            coaches=data["coach"],
            streaks = streaks,
            teamname = the_team["name"], 
            teamid = the_team["id"], 
            title="{}".format(the_team["name"],
            subtitle="sorted by date")), 
        "team/{}".format(the_team["id"]))


def all_games_by_team(data):
    teams = team.list_teams()
    games = match_list.list_all_matches() 
    for t in teams:
        team_stats(data, teams, games, t)

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
    all_games_by_team(collated_data)

    print("Exporting teams by points")
    with open("output/team.html", "w") as teams:
        teams.write(all_teams())

    print("Exporting teams by year")
    teams_by_year(2007, datetime.datetime.now().year+1)

    index.index()
if __name__ == "__main__":
    main()
