

START_RATING = 0

def expected(A, B):
    """
    Calculate expected score of A in a match against B

    :param A: Elo rating for player A
    :param B: Elo rating for player B
    """
    return 1 / (1 + 10 ** ((B - A) / 400))


def elo(old, exp, score, k=10):
    """
    Calculate the new Elo rating for a player

    :param old: The previous Elo rating
    :param exp: The expected score for this match
    :param score: The actual score for this match
    :param k: The k-factor for Elo (default: 32)
    """
    return old + k * (score - exp)


def rate_all(data):
    def verify_coach(result, cid):
        if cid not in result:
            result[cid] = {"cid": cid, "rating": START_RATING, "games": []}
        return result
    def add_game(result, cid, game_id, old_rating, new_rating, score):
        result[cid]["rating"] = new_rating
        result[cid]["games"].append( {"game_id": game_id, "score": score, "old_rating": old_rating, "rating": new_rating} ) 

        return result

    result = {} 
    coaches = data["coach"]
    games = sorted(data["game"].values(), key=lambda x: "{0}-{1:04d}".format(x["date"], int(x["matchid"])))
    for g in games:
        c1_id = g["home"]["coachid"]
        verify_coach(result, c1_id)
        c1_gamecount = len(result[c1_id]["games"])

        c2_id = g["away"]["coachid"]
        verify_coach(result, c2_id)
        c2_gamecount = len(result[c2_id]["games"])

        c1_rating = result[c1_id]["rating"] if c1_id in result else START_RATING
        c2_rating = result[c2_id]["rating"] if c2_id in result else START_RATING

        c1_kfactor = 2 if c1_gamecount > 9 else 10
        c1_expected = expected(c1_rating, c2_rating) 

        c2_kfactor = 2 if c2_gamecount > 9 else 10
        c2_expected = expected(c2_rating, c1_rating) 

        c1_score = 1 if g["home"]["result"] == "W" else 0.5 if g["home"]["result"] == "T" else 0 
        c2_score = 1 - c1_score

        c1_newrating = elo(c1_rating, c1_expected, c1_score, c1_kfactor) if len(result) < 10 or c2_gamecount > 4 or (c1_gamecount < 5 and c2_gamecount < 5) else c1_rating 
        c2_newrating = elo(c2_rating, c2_expected, c2_score, c2_kfactor) if len(result) < 10 or c1_gamecount > 4 or (c1_gamecount < 5 and c2_gamecount < 5) else c2_rating

        add_game(result, c1_id, g["matchid"], c1_rating, c1_newrating, c1_score)
        add_game(result, c2_id, g["matchid"], c2_rating, c2_newrating, c2_score)

    return result
    


def main():
    from sys import argv
    import pprint
    from stats import collate
    from coach.coach import dict_coaches_by_uid

    pp = pprint.PrettyPrinter(indent=2)
    data = collate.collate()

    rates = rate_all(data)
    
    for r in sorted(rates.values(), key=lambda x: x["rating"]):
        #pp.pprint(r)
        uid = r["cid"]
        if uid in data["_coachid"]:
            print("{} {} {}".format( uid, data["_coachid"][uid]["nick"], 150 + r["rating"]))

    if len(argv) > 1:
        pp.pprint(rates[int(argv[1])])
    #pp.pprint(coaches_by_uid)

if __name__ == "__main__":
    main()

    




