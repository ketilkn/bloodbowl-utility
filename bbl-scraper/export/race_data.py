#!/usr/bin/env python3
import logging
from team import team
from stats.team_list import list_all_teams_by_points, list_all_games_by_race
from stats.match_list import list_all_matches, list_all_games_by_year
from stats.team_list import format_for_total, format_for_average
from stats import match_list
import stats.elo
import export.filter
from . import export
LOG = logging.getLogger(__package__)


def add_title(races):
    LOG.debug("add_title")
    for race in races:
        group={}
        group["data"] = race
        group["data"]["total"] = race
        group["title"] = race["race"]
        group["link"] = export.filter.race_link(race["teamid"])
        yield group


def all_games_by_race(data=None):
    LOG.debug("all_games_by_race")

    elo_rating = stats.elo.rate_all(data, lambda v, y: v[y+"_race"])
    rated_race = list(add_title(list_all_games_by_race(data, no_mirror=True)))
    for r in rated_race:
        race_name = r["title"][0:r["title"].find("(")].strip()
        r["data"]["elo"] = "{:.2f}".format(150+elo_rating[race_name]["games"][-1]["rating"])

    return export.get_template("race/races.html").render(
        show_elo = True,
        teams = rated_race,
        teams_in_need = rated_race,
        title="All races",
        subtitle="sorted by performance")


def all_teams_for_race(race, race_teams, performance_by_race):
    LOG.debug("All %s teams %s", race, len(race_teams))
    return export.get_template("race/teams-for-race.html").render(
        teams_average = format_for_average(race_teams),
        teams_total = format_for_total(race_teams),
        teams = race_teams,
        games_by_race = performance_by_race,
        title="All {} teams".format(race),
        subtitle="sorted by points")


def teams_by_race(data):
    LOG.debug("teams_by_race")
    race = team.list_race(data)    
    teams =  list_all_teams_by_points(data)
    for r in race:
        team_race = filter(lambda x: x["race"] == r, teams)
        
        race_games = match_list.we_are_race(data["game"].values(), r)
        race_games = list(filter(lambda m: m["away_race"] != r, race_games))

        LOG.debug("race_games length is %s", len(race_games))
        performance_by_race = match_list.sum_game_by_group(race_games, match_list.group_games_by_race)

        with open("output/race/{}.html".format(r.replace(" ","-")), "w") as fp:
            fp.write(all_teams_for_race(r, list(team_race), performance_by_race))


def export_race_by_performance(data = None):
    with open("output/races.html", "w") as matches:
        matches.write(all_games_by_race(data))


def main():
    import stats.collate
    collated_data = stats.collate.collate()

    log_format = "[%(levelname)s:%(filename)s:%(lineno)s - %(funcName)20s ] %(message)s"
    logging.basicConfig(level=logging.DEBUG, format=log_format)

    LOG.info("Exporting races by performance")
    with open("output/races.html", "w") as matches:
        matches.write(all_games_by_race(collated_data))

    print("Exporting teams by race")
    teams_by_race(collated_data)
    

if __name__ == "__main__":
    main()
