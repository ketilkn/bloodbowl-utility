#!/usr/bin/env python3
import datetime
import os

import logging
import export.filter
import stats.player_list
from . import export
from importer.bbleague.defaults import BASEPATH
LOG = logging.getLogger(__package__)


def make_top_list(players, name, key, heading="Most experienced", order=stats.player_list.order_by_spp, limit=5):
    return {"name": name,
            "key": key,
            "heading": heading,
            "players": list(stats.player_list.flatten_players(order(players)))[:limit]}


def players_by_position(data, position):
    LOG.debug("%s players in data", len(data["player"]) if "player" in data else "No")

    players = [p for p in stats.player_list.all_players(data) if p["position"] == position]
    players = stats.player_list.flatten_players(players)

    return export.get_template("player/player_position.html").render(
        players = list(players),
        hide_position = False,
        hide_team = False,
        title=position,
        subtitle="")


def top_players(data=None):
    LOG.debug("%s players in data", len(data["player"]) if "player" in data else "No")
    players = stats.player_list.all_players(data)

    top_by_touchdown = make_top_list(players, "TDs", "td", "Top scorers", stats.player_list.order_by_touchdowns)
    top_by_completion = make_top_list(players, "passes", "cmp", "Top throwers", stats.player_list.order_by_completion)
    top_by_casualties = make_top_list(players, "cas", "cas", "Top hitters", stats.player_list.order_by_casualties)
    top_by_mvp = make_top_list(players, "mvp", "mvp", "Top MVPs", stats.player_list.order_by_mvp)
    top_by_interception = make_top_list(players, "int", "int", "Top interceptors", stats.player_list.order_by_interception)
    top_by_spp = make_top_list(players, "spp", "spp", "Top stars", stats.player_list.order_by_spp, limit=14)
    top_by_value = make_top_list(players, "gp", "value", "Most expensive", stats.player_list.order_by_value)

    toplists = [top_by_spp, top_by_value,
                top_by_touchdown,
                top_by_mvp,
                top_by_completion,
                top_by_interception,
                top_by_casualties]

    return export.get_template("player/players.html").render(
        toplists = toplists,
        title="All time top players",
        subtitle="")


def get_players_modification_date():
    try:
        return datetime.datetime.fromtimestamp(os.path.getmtime('input/anarchy.bloodbowlleague.com/json/players.json')).strftime("%Y-%m-%d")
    except:
        return "?"


def all_player(data=None):
    LOG.debug("%s players in data", len(data["player"]) if "player" in data else "No")
    players = stats.player_list.flatten_players(stats.player_list.all_players(data))
    players_updated = get_players_modification_date()
    return export.get_template("player/all_player.html").render(
        players = list(players),
        players_updated = players_updated,
        hide_position = False, 
        hide_team = False, 
        title="All players",
        subtitle="sorted by star player points")


def export_race_by_performance(data = None):
    with open("output/races.html", "w") as matches:
        matches.write(stats.player_list.all_games_by_race(data))

def all_players(collated_data):
    LOG.info("Exporting top players index")
    with open("output/players.html", "w") as all_players_file:
        all_players_file.write(top_players(collated_data))
    LOG.info("Exporting all players")
    with open("output/all_players.html", "w") as all_players_file:
        all_players_file.write(all_player(collated_data))

    all_position(collated_data)


def all_position(collated_data):
    LOG.info("Exporting all players by position")
    for position in stats.player_list.all_positions(collated_data):
        filename = position.replace(" ", "-")
        with open("output/player/{}.html".format(filename), "w") as all_players_file:
            all_players_file.write(players_by_position(collated_data, position))



def main():
    import stats.collate
    collated_data = stats.collate.collate()

    log_format = "[%(levelname)s:%(filename)s:%(lineno)s - %(funcName)20s ] %(message)s"
    logging.basicConfig(level=logging.DEBUG, format=log_format)

    all_players(collated_data)


if __name__ == "__main__":
    main()
