#!/usr/bin/env python3
from collections import Counter
import copy
from operator import itemgetter
import logging
from match import match
from team import team
from coach import coach

LOG = logging.getLogger(__package__)


def team_data(the_team, team_matches):
    data_for_team = {}
    data_for_team["head_coach"] = the_team["coach"]
    data_for_team["co_coach"] = the_team["co-coach"]
    data_for_team["retired_coach"] = set([match["home_coach"] for match in team_matches if match["home_coach"] not in [the_team["coach"], the_team["co-coach"]]])

    data_for_team["last_game"] = team_matches[0]["date"] if len(team_matches) > 0 else "Never"
    data_for_team["first_game"] = team_matches[-1]["date"] if len(team_matches) > 0 else None
    data_for_team["gamesplayed"] = len(team_matches)
    data_for_team["teamvalue"] = the_team["teamvalue"]

    return data_for_team

def matchresult(match, team1, team2):
    return {"teamid": match[team1+"_teamid"],
            'td_for': match[team1+"_td"],
            'td_against': match[team2+"_td"],
            'cas_for': match[team1+"_cas"],
            'cas_against': match[team2+"_cas"],
            'matchid': match["matchid"],
            'date': match["date"],
            "result": match[team1+"_result"],
            "coach": match[team1+"_coachid"],
            "coach_against": match[team2+"_coachid"]
            }

def add_result(result, match):
    #import pprint
    #pprint.pprint(match, indent=4, width=200)
    teamid = match["teamid"]
    if not teamid in result:
        result[teamid] = { "teamid": teamid,
            "W": 0, "L": 0, "T": 0 , 
            'td_for': 0,
            'td_against': 0,
            'cas_for': 0,
            'cas_against': 0,

            'matches': [],
            'coaches': Counter(),
            'first_match': None,
            'last_match': None}
    result[teamid][match["result"]] = result[teamid][match["result"]] + 1
    result[teamid]["td_for"] = result[teamid]["td_for"] + match["td_for"]
    result[teamid]["td_against"] = result[teamid]["td_against"] + match["td_against"]
    result[teamid]["cas_for"] = result[teamid]["cas_for"] + match["cas_for"]
    result[teamid]["cas_against"] = result[teamid]["cas_against"] + match["cas_against"]
    result[teamid]["matches"].append(match["matchid"])
    if result[teamid]["first_match"] == None or result[teamid]["first_match"] > match["date"]:
        result[teamid]["first_match"] = match["date"] 
    if result[teamid]["last_match"] == None or result[teamid]["last_match"] < match["date"]:
        result[teamid]["last_match"] = match["date"] 
    result[teamid]["coaches"][match["coach"]] += 1


def rank(matches):
    result = {} 
    
    for match in matches:
        add_result(result, matchresult(match, "home", "away"))
        add_result(result, matchresult(match, "away", "home"))

    return result

def add_teamdata(ranking):
    all_teams = team.dict_teams()
    all_coaches = coach.dict_coaches()

    result = []
    for rankedteam in ranking.values():
        rankedteam["team"] = all_teams[rankedteam["teamid"]]
        rankedteam["coach"] = all_coaches[rankedteam["team"]["coach"]] if rankedteam["team"]["coach"] else ""
        #Retired team can have coach==None
        rankedteam["coaches"] = rankedteam["coaches"].items()

    return ranking

def format_for_teamlist(ranked_team):
    #import pprint
    #pprint.pprint(ranked_team, indent=4, width=200)
    return {"teamid": ranked_team["teamid"],
            "name": ranked_team["team"]["name"],
            "race": ranked_team["team"]["race"],
            "coach": ranked_team["team"]["coach"],
            "teamvalue": ranked_team["team"]["teamvalue"]/1000 if ranked_team["team"]["teamvalue"] else 0,
            "gamesplayed": len(ranked_team["matches"]),
            "first_match": ranked_team["first_match"],
            "last_match": ranked_team["last_match"],
            "coach_count": len(ranked_team["coaches"]),
            "coaches": ranked_team["coaches"],
            "win": ranked_team["W"],
            "tie": ranked_team["T"],
            "loss": ranked_team["L"],
            "performance": (((ranked_team["W"]*2)+(ranked_team["T"]*1))/ (len(ranked_team["matches"])*2))*100,
            "td": ranked_team["td_for"] - ranked_team["td_against"],
            "td_for": ranked_team["td_for"],
            "td_against": ranked_team["td_against"],
            "cas": ranked_team["cas_for"] - ranked_team["cas_against"],
            "cas_for": ranked_team["cas_for"],
            "cas_against": ranked_team["cas_against"],
            "points": (ranked_team["W"]*5)+(ranked_team["T"]*3)+ranked_team["L"]
    }

def format_for_average(teams):
    gamesplayed = sum(map(lambda x: x["gamesplayed"], teams))
    wins = sum(map(lambda x: x["win"], teams))
    ties = sum(map(lambda x: x["tie"], teams))
    formatted = {"win": sum(map(lambda x: x["win"], teams))/gamesplayed if gamesplayed > 0 else 0,
            "tie": sum(map(lambda x: x["tie"], teams))/gamesplayed if gamesplayed > 0 else 0, 
            "loss" : sum(map(lambda x: x["loss"], teams))/gamesplayed if gamesplayed > 0 else 0,
            "td": sum(map(lambda x: x["td_for"]/gamesplayed-x["td_against"], teams))/gamesplayed if gamesplayed > 0 else 0,
            "td_for": sum(map(lambda x: x["td_for"], teams))/gamesplayed if gamesplayed > 0 else 0,
            "td_against": sum(map(lambda x: x["td_against"], teams))/gamesplayed if gamesplayed > 0 else 0,
            "cas": sum(map(lambda x: x["cas_for"]/gamesplayed-x["cas_against"], teams))/gamesplayed if gamesplayed > 0 else 0,
            "cas_for": sum(map(lambda x: x["cas_for"], teams))/gamesplayed if gamesplayed > 0 else 0,
            "cas_against": sum(map(lambda x: x["cas_against"], teams))/gamesplayed if gamesplayed > 0 else 0,
            "performance" : sum(map(lambda x: x["performance"], teams)) / len(teams) if len(teams) > 0 else 0, #(wins*2+ties)/(gamesplayed*2)*100 if gamesplayed > 0 else 0,
            "gamesplayed": gamesplayed/len(teams) if len(teams) > 0 else 0,
            "points": sum(map(lambda x: x["points"], teams))/gamesplayed if gamesplayed > 0 else 0
            }
    return formatted

def format_for_total(teams):
    gamesplayed = sum(map(lambda x: x["gamesplayed"], teams))
    wins = sum(map(lambda x: x["win"], teams))
    ties = sum(map(lambda x: x["tie"], teams))
    return {"win": sum(map(lambda x: x["win"], teams)),
            "tie": sum(map(lambda x: x["tie"], teams)), 
            "loss" : sum(map(lambda x: x["loss"], teams)),
            "td": sum(map(lambda x: x["td_for"]-x["td_against"], teams)),
            "td_for": sum(map(lambda x: x["td_for"], teams)),
            "td_against": sum(map(lambda x: x["td_against"], teams)),
            "cas": sum(map(lambda x: x["cas_for"]-x["cas_against"], teams)),
            "cas_for": sum(map(lambda x: x["cas_for"], teams)),
            "cas_against": sum(map(lambda x: x["cas_against"], teams)),
            "performance" : (wins*2+ties)/(gamesplayed*2)*100 if gamesplayed > 0 else 0,
            "gamesplayed": gamesplayed,
            "points": sum(map(lambda x: x["points"], teams))
            }


def rank_teams(matches):
    teamlist = list(map(format_for_teamlist, matches))
    teams = sorted(teamlist, key=itemgetter("name"))
    teams = sorted(teams, key=lambda x: x["cas_for"]-x["cas_against"], reverse=True)
    teams = sorted(teams, key=lambda x: x["td_for"]-x["td_against"], reverse=True)
    teams = sorted(teams, key=itemgetter("points"), reverse=True)
    return teams


def list_all_teams_by_year(year):
    start_date = "{}-99-99".format(year-1)
    end_date = "{}-00-00".format(int(year)+1)
    return list_all_teams_by_period(start_date, end_date)


def list_all_teams_by_period(start_date, end_date):
    matches = filter(
                lambda x: x["date"] > start_date and x["date"] < end_date, 
                match.match_list())

    return list(rank_teams(add_teamdata(rank(matches)).values()))

def list_all_teams_by_points(games=None):
    gamesplayed = games
    if games == None:
        gamesplayed = match.match_list()
    return list(rank_teams(add_teamdata(rank(gamesplayed)).values()))

def team_count_by_race(teams):
    team_count = {}
    for t in teams:
        if t["race"] not in team_count:
            team_count[t["race"]] = 0
        team_count[t["race"]] = team_count[t["race"]] + 1
    return team_count


def list_all_games_by_race(data, no_mirror=False):
#    return list_all_teams_by_points()
    matches = copy.deepcopy(list(data["game"].values()))
    teams = data["team"]
    team_count = team_count_by_race(teams.values())
    for m in matches:
        m["home_teamid"] = teams[m["home_teamid"]]["race"]
        m["away_teamid"] = teams[m["away_teamid"]]["race"]
    
    matches = rank( filter(lambda m: m["home_teamid"] != m["away_teamid"], matches) if no_mirror else matches)

    for m in matches.values():
        m["team"] = {"coach": "-", "race": "{} ({})".format(m["teamid"], team_count[m["teamid"]]), "name": m["teamid"], "teamid": m["teamid"], "teamvalue": ""} 
        m["coach"] = "-"

    return sorted(
            sorted(
                rank_teams(
                    matches.values()), 
                key=itemgetter("performance"), 
                reverse=True), 
            key = lambda x: x["gamesplayed"] > 24, 
            reverse=True)


def main():
    import pprint
    import sys
    log_format = "[%(levelname)s:%(filename)s:%(lineno)s - %(funcName)20s ] %(message)s"
    logging.basicConfig(level=logging.DEBUG, format=log_format)

    for t in filter(lambda x: not "gamesplayed" in x or x["gamesplayed"] > 0, list_all_teams_by_year(int(sys.argv[1]) if len(sys.argv) > 1 else 2017)):
        print("{}:".format(t["name"] if "name" in t else t["team"]["name"]))
        pprint.pprint(t, indent=4, width=250)


if __name__ == "__main__":
    main()
