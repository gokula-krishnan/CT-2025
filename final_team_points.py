import json
import os
import requests
from functools import reduce
from dotenv import load_dotenv

load_dotenv()

# open auction team list file
teamListFile = open('CT_2025_TEAMS/teamList.json')
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
#
# # Most runs and MOTT
# results["RohitRam"] += 100
#
# # Most wickets
# results["ChanIjaz"] += 50

# sort by points
sortList = sorted(results.items(), key=lambda x: x[1], reverse=True)
for team in sortList:
    print(team)

with open("./Data/team_with_players_points.json", "w") as fw:
    json.dump(team_with_players_dict, fw)


# Function to update Gist content
def update_gist():
    # Read JSON data from file
    # Prepare Gist payload
    payload = {
        "files": {}
    }

    # Iterate through each key-value pair in JSON data and add to payload
    payload["files"][os.getenv('gist_file_name')] = {"content": json.dumps(pointsData)}

    # Prepare headers with access token
    headers = {
        "Authorization": f"Bearer {os.getenv('access_token')}",
        "Accept": "application / vnd.github + json",
        "X-GitHub-Api-Version": "2022-11-28",
    }

    # Make PATCH request to update Gist
    response = requests.patch(f"https://api.github.com/gists/{os.getenv('gist_id')}", headers=headers, json=payload)

    # Check if update was successful
    if response.status_code == 200:
        print("Gist content updated successfully.")
    else:
        print(f"Failed to update Gist. Status code: {response.status_code}")
        print(f"Error message: {response.text}")


update_gist()
