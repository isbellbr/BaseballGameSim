from pybaseball import batting_stats_bref, pitching_stats_bref

team_names = []
team_lineups = []


def add_lineup(team_name, br_team):
    import misc_funcs
    team_names.append(team_name)
    #Get the Orioles Lineup
    data = batting_stats_bref(2024)
    team_data = data[data["Tm"] == br_team]
    team_regulars = team_data[team_data["PA"] > 300]
    team_lineup = []
    for index, player in team_regulars.iterrows():
        PAs = player["PA"]
        Ks = player["SO"]
        hits = player["H"]
        doubles = player["2B"]
        triples = player["3B"]
        homers = player["HR"]
        walks = player["BB"]
        name = player["Name"]
        team_lineup.append(misc_funcs.create_hitter(PAs, Ks, hits, doubles, triples, homers, walks, name))
    team_lineups.append(team_lineup)

add_lineup("Orioles", "Baltimore")
add_lineup("Astros", "Houston")
add_lineup("Phillies", "Philadelphia")

lineups_dict = dict(zip(team_names, team_lineups))

def get_lineups():
    return lineups_dict

for hitter in lineups_dict["Phillies"]:
    print(hitter.name)