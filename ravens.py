import requests
import csv
# print(response)
# print(response.json())

file = open("ravens_data.csv", "w")
writer = csv.writer(file)
#Ranking
writer.writerow(["TEAM", "NAMES", "POSITION", "JERSEY", "HEIGHT", "WEIGHT", "YEAR", "BIRTHPLACE"])
file.close()

ACC_teams = ["bc", "california", "clem", "duke", "fsu", "gt", "lou", "mia", "ncsu", "WakeForest", "vt", "uva", "Syracuse", "Stanford", "SMU", "Pitt", "Unc"]

def build_csv(abv):
    response = requests.get("https://site.api.espn.com/apis/site/v2/sports/football/college-football/teams/"+abv+"/roster?limit=200")

    offense = response.json()['athletes'][0]['items']

    defense = response.json()['athletes'][1]['items']

    special = response.json()['athletes'][2]['items']

    all_players = offense + defense + special

    file = open("ravens_data.csv", "a")
    writer = csv.writer(file)
    for player in all_players:
        team_name = player['college']['name'] + " " + player['college']['mascot']
        player_name = player['fullName']
        position = player['position']["name"]
        try:
            jersey_num = player['jersey']
        except:
            jersey_num = 00

        try:
            height = player['displayHeight']
        except:
            height = "NA"

        try:
            weight = player['displayWeight']
        except:
            weight = "NA"

        try:
            year = player['experience']['displayValue']
        except:
            year = "NA"

        try:
            birth_place = player['birthPlace']['displayText']
        except:
            birth_place = "NA"

        print(team_name + ": " + player_name + "|" + position + "|" + "Jersey: " + jersey_num + "|" + "Height: " + height + "|" + "Weight: " + weight +  "|" + year + "|" + birth_place)
        writer.writerow([team_name, player_name,position, jersey_num, height, weight, year, birth_place])
    file.close()

def clear_rows():
    file = open("ravens_data.csv", "w")
    writer = csv.writer(file)
    writer.writerow(["TEAM", "NAMES", "POSITION", "JERSEY", "HEIGHT", "WEIGHT", "YEAR", "BIRTHPLACE"])

clear_rows()
for team in ACC_teams:
    build_csv(team)

#ACC

# Boston College Eagles

# California Golden Bears

# Clemson Tigers

# Duke Blue Devils

# Florida State Seminoles

# Georgia Tech Yellow Jackets

# Louisville Cardinals

# Miami Hurricanes

# NC State Wolfpack

# North Carolina Tar Heels

# Pittsburgh Panthers

# SMU Mustangs

# Stanford Cardinal

# Syracuse Orange

# Virginia Cavaliers

# Virginia Tech Hokies

# Wake Forest Demon Deacons




