#!/usr/bin/env python3
import logging
import export.filter
import stats.player_list
from . import export
from importer.bbleague.defaults import BASEPATH
LOG = logging.getLogger(__package__)


def all_player(data=None):
    LOG.debug("%s players in data", len(data["player"]) if "player" in data else "No")
    players = stats.player_list.flatten_players(stats.player_list.all_players(data))
    return export.get_template("player/all_player.html").render(
        players = list(players),
        title="All players",
        subtitle="sorted by spp")


def export_race_by_performance(data = None):
    with open("output/races.html", "w") as matches:
        matches.write(stats.player_list.all_games_by_race(data))


def main():
    import stats.collate
    collated_data = stats.collate.collate()

    log_format = "[%(levelname)s:%(filename)s:%(lineno)s - %(funcName)20s ] %(message)s"
    logging.basicConfig(level=logging.DEBUG, format=log_format)

    LOG.info("Exporting players")
    with open("output/races.html", "w") as all_players_file:
        all_players_file.write(all_player(collated_data))



if __name__ == "__main__":
    main()