def coach_anchor(input):
    #return input
    if not input:
        return "None"
    return "<a href='coach/{}.html'>{}</a>".format(input.replace(' ','-'), input)


def team_value(input):
    if not input:
        return "Unknown"
    return "{}k".format(int(input/1000))


def race_short(input):
    lowered_input = input.lower()
    if not input:
        return ""
    if "undead" in lowered_input or "renegades" in lowered_input:
        return input.split(" ")[-1]
    if "horne" in lowered_input or "underworld" in lowered_input or "necromantic" in lowered_input or "chosen" in lowered_input:
        return input.split(" ")[0]
    if "union" in lowered_input:
        return "{}lf".format(input[0])
    return input


def race_link(input):
    return "race/{}.html".format(input.replace(' ', '-'))


def team_link(input):
    return "team/{}.html".format(input.replace(' ', '-'))


def player_link(input):
    return "player/{}.html".format(input.replace(' ', '-'))


def load_filter(environment):
    environment.filters["race_short"] = race_short
    environment.filters["race_link"] = race_link
    environment.filters["player_link"] = player_link
    environment.filters["team_link"] = team_link
    environment.filters["coach_anchor"] = coach_anchor
    environment.filters["team_value"] = team_value
    return environment

