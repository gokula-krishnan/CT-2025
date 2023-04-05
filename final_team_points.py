import json

# open auction team list file
teamListFile = open('IPL_2023_TEAMS/teamList.json')
teamListData = json.load(teamListFile)

#  initialise results
results = {}

#  load playerPoints file
pointFile = open('./Data/playerPoints.json')
pointsData = json.load(pointFile)

# loop through the team list
for team in teamListData:
    playersList = teamListData[team]
    # initialise team in results blob
    results[team] = ''
    # initialise pointSum for each team
    pointSum = 0
    # for each player in team list, get points and add to pointSum
    for player in playersList:
        point = [x['totalPoints'] for x in pointsData['Players'] if x['id'] == player]
        if len(point) != 0:
            pointSum += point.pop()
    # store to the results blob
    results[team] = pointSum

# sort by points
sortList = sorted(results.items(), key=lambda x: x[1],reverse=True)
for team in sortList:
    print(team)
