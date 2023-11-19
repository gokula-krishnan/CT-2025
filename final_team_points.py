import json
from functools import reduce
# open auction team list file
teamListFile = open('WC_2023_TEAMS/teamList.json')
teamListData = json.load(teamListFile)

#  initialise results
results = {}

#  load playerPoints file
pointFile = open('./Data/playerPoints.json')
pointsData = json.load(pointFile)
team_with_players_dict = {}
# loop through the team list
for team in teamListData:
    playersList = teamListData[team]
    # initialise team with players
    team_with_players_dict[team] = {}
    # initialise team in results blob
    results[team] = ''
    # initialise pointSum for each team
    pointSum = []
    # for each player in team list, get points and add to pointSum
    for player in playersList:
        for x in pointsData['Players']:
            if x['id'] == player:
                players_total_point = x['totalPoints'] + reduce(lambda a, b: a+b, [25 if match['isMOTM'] else 0
                                                                                   for match in x['scores']])
                pointSum.append(players_total_point)
                team_with_players_dict[team].update({x['name']: players_total_point})
    # store to the results blob
    results[team] = sum(pointSum)

    # final points WC23
    if team == "CNI":
        results[team] += 200

    if team == "TH":
        results[team] += 100



# sort by points
sortList = sorted(results.items(), key=lambda x: x[1], reverse=True)
for team in sortList:
    print(team)

with open("./Data/team_with_players_points.json", "w") as fw:
    json.dump(team_with_players_dict, fw)
