import requests
import csv

requestURL = "https://hs-consumer-api.espncricinfo.com/v1/pages/series/squad/details?seriesId=1345038&squadId={0}"

teamIds = ["1345088", "1345099", "1345118", "1345123", "1345126", "1345167", "1345168", "1346157", "1346159", "1346156"]

for id in teamIds:
    teamInfo = requests.get(url=requestURL.format(id)).json()
    print(teamInfo.keys())
    with open('Data/teams.csv', 'a', newline='\n') as teamFile:
        writer = csv.writer(teamFile)
        writer.writerow([teamInfo["content"]["squadDetails"]["squad"]["teamId"], teamInfo["content"]["squadDetails"]["squad"]["teamName"]])
    
    with open('Data/players.csv', 'a', newline='\n') as playerFile:
        writer = csv.writer(playerFile)
        for player in teamInfo["content"]["squadDetails"]["players"]:
            writer.writerow([player["player"]["id"], player["player"]["longName"], teamInfo["content"]["squadDetails"]["squad"]["teamId"]])
