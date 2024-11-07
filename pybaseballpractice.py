# from pybaseball import standings
# data = standings(2024)
# for division in data:
#     print(division)

from pybaseball import batting_stats_bref, pitching_stats_bref

# get all of this season's batting data so far
data = batting_stats_bref(2024)
orioles_data = data[data["Tm"] == "Baltimore"]
orioles_regulars = orioles_data[orioles_data["PA"] > 300]
print(orioles_regulars)

# cowser = orioles_regulars[orioles_regulars["Name"] == "Colton Cowser"]
# print("Colton Cowser has hit " + str(cowser["HR"].values[0]) + " home runs.")

for index, player in orioles_regulars.iterrows():
    player_name = player["Name"]
    home_runs = player["HR"]
    print(player_name + " has hit " + str(home_runs) + " home runs.")


categorized_data = data.sort_values(by="OPS", ascending=False)
categorized_data = categorized_data[categorized_data["PA"] > 300]
print(categorized_data.head(10))

stat = "ERA"
pitching_data = pitching_stats_bref(2024)
pitching_by_stat = pitching_data.sort_values(by=stat)
pitching_by_stat = pitching_by_stat[pitching_by_stat["IP"] > 160]
for index, player in pitching_by_stat.head(10).iterrows():
    player_name = player["Name"]
    era = player[stat]
    print(player_name + " has a " + str(era) + " " + stat + ".")