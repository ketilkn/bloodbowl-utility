#!/usr/bin/env python3
from operator import itemgetter
from match import match
from team import team
from coach import coach



def all_teams():
    teams = team.dict_teams()
    return teams

def all_coaches():
    coaches = coach.dict_coaches()
    return coaches

def matchresult(match, team1, team2):
    return {"teamid": match[team1]["team"]["teamid"], 
            'td_for': match[team1]["td"],
            'td_against': match[team2]["td"],
            'cas_for': match[team1]["casualties"]["total"],
            'cas_against': match[team2]["casualties"]["total"],
            'matchid': match["matchid"],
            'date': match["date"],
            "result": match[team1]["result"]
            }

def add_result(result, match):
    teamid = match["teamid"]
    if not teamid in result:
        result[teamid] = { "teamid": teamid,
            "W": 0, "L": 0, "T": 0 , 
            'td_for': 0,
            'td_against': 0,
            'cas_for': 0,
            'cas_against': 0,

            'matches': []}
    result[teamid][match["result"]] = result[teamid][match["result"]] + 1
    result[teamid]["td_for"] = result[teamid]["td_for"] + match["td_for"]
    result[teamid]["td_against"] = result[teamid]["td_against"] + match["td_against"]
    result[teamid]["cas_for"] = result[teamid]["cas_for"] + match["cas_for"]
    result[teamid]["cas_against"] = result[teamid]["cas_against"] + match["cas_against"]
    result[teamid]["matches"].append(match["matchid"])


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
    return ranking

def format_for_teamlist(ranked_team):
    return {"teamid": ranked_team["teamid"],
            "name": ranked_team["team"]["name"],
            "race": ranked_team["team"]["race"],
            "coach": ranked_team["team"]["coach"],
            "teamvalue": ranked_team["team"]["teamvalue"]/1000 if ranked_team["team"]["teamvalue"] else 0,
            "gamesplayed": len(ranked_team["matches"]),
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
    return {"win": sum(map(lambda x: x["win"], teams))/gamesplayed if gamesplayed > 0 else 0,
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


def list_all_games_by_race():
#    return list_all_teams_by_points()
    matches = match.match_list()
    teams = all_teams()
    team_count = team_count_by_race(teams.values())
    for m in matches:
        m["home"]["team"]["teamid"] = teams[m["home"]["team"]["teamid"]]["race"]
        m["away"]["team"]["teamid"] = teams[m["away"]["team"]["teamid"]]["race"]

    matches = rank(matches)

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
    for t in list_all_teams_by_points():
        print(t)


if __name__ == "__main__":
    main()