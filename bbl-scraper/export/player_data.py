#!/usr/bin/env python3
import logging
import export.filter
import stats.player_list
from . import export
from importer.bbleague.defaults import BASEPATH
LOG = logging.getLogger(__package__)


def top_players(data=None):
    LOG.debug("%s players in data", len(data["player"]) if "player" in data else "No")
    players = stats.player_list.all_players(data)
    top_by_touchdown = {"name": "TDs", "key": "td", "heading": "Top scorers",
                        "players": list(stats.player_list.flatten_players(stats.player_list.order_by_touchdowns(players)))[:5]}

    top_by_completion = {"name": "passes", "key": "cmp", "heading": "Top throwers",
                         "players": list(stats.player_list.flatten_players(stats.player_list.order_by_completion(players)))[:5]}

    top_by_casualties = {"name": "cas", "key": "cas", "heading": "Top hitters",
                         "players": list(stats.player_list.flatten_players(stats.player_list.order_by_casualties(players)))[:5]}

    toplists = [top_by_touchdown, top_by_completion, top_by_casualties]

    return export.get_template("player/players.html").render(
        toplists = toplists,
        title="Player performance",
        subtitle="sorted by spp")


def all_player(data=None):
    LOG.debug("%s players in data", len(data["player"]) if "player" in data else "No")
    players = stats.player_list.flatten_players(stats.player_list.all_players(data))
    return export.get_template("player/all_player.html").render(
        players = list(players),
        hide_position = False, 
        hide_team = False, 
        title="All players",
        subtitle="sorted by spp")


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



def main():
    import stats.collate
    collated_data = stats.collate.collate()

    log_format = "[%(levelname)s:%(filename)s:%(lineno)s - %(funcName)20s ] %(message)s"
    logging.basicConfig(level=logging.DEBUG, format=log_format)

    all_players(collated_data)


if __name__ == "__main__":
    main()
