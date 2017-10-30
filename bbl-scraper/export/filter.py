

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
    return "/race/{}.html".format(input.replace(' ', '-'))

def team_link(input):
    return "/team/{}.html".format(input.replace(' ', '-'))


def load_filter(environment):
    environment.filters["race_short"] = race_short
    environment.filters["race_link"] = race_link
    environment.filters["team_link"] = team_link
    return environment

