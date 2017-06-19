#!/usr/bin/env python3
from jinja2 import Template
import jinja2
from match import match
from team import team
from coach import coach
from stats.team_list import list_all_teams_by_points, list_all_games_by_race, list_all_teams_for_race, list_all_teams_by_year
from stats.match_list import list_all_matches, list_all_games_by_year
from stats.team_list import format_for_total, format_for_average
from . import coach_data
from . import index
import datetime

def get_template(template_name):
    template_dir = 'template/'
    loader = jinja2.FileSystemLoader(template_dir)
    environment = jinja2.Environment(loader=loader)
    return environment.get_template(template_name)

def write_html(data, filename):
    with open("output/{}.html".format(filename), "w") as fp:
        fp.write(data)

def write_data(data, filename):
    write_html(data, filename)

def main():
    import stats.collate
    collated_data = stats.collate.collate()


if __name__ == "__main__":
    main()
