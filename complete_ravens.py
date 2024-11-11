import requests
import csv

url = "https://api.collegefootballdata.com/recruiting/players"

file = open("ravens_data.csv", "w")
writer = csv.writer(file)
writer.writerow(["CONFERENCE","TEAM", "NAMES", "POSITION", "JERSEY", "HEIGHT", "WEIGHT", "YEAR", "BIRTHPLACE","HS RANKING","HS STARS","RECRUITING YEAR"])
file.close()

ACC_teams = ["bc", "california", "clem", "duke", "fsu", "gt", "lou", "mia", "ncsu", "WakeForest", "vt", "uva", "Syracuse", "Stanford", "SMU", "Pitt", "Unc"]
ACC_teams_full = [
    "Boston College", "California", "Clemson", "Duke", "Florida State", 
    "Georgia Tech", "Louisville", "Miami", "NC State", "Wake Forest", 
    "Virginia Tech", "Virginia", "Syracuse", "Stanford", "SMU", "Pittsburgh", "North Carolina"
]

PAC_12_teams = ["orst","wsu"] 
PAC_12_teams_full = [
    "Oregon State", "Washington State"
]

SEC_teams = ["ala","ark","aub","fla","uga","uk","lsu","msst","miz","ou","miss","sc","tenn","ta&m","tex","van"]
SEC_teams_full = [
    "Alabama", "Arkansas", "Auburn", "Florida", "Georgia", "Kentucky", 
    "Louisiana State", "Mississippi State", "Missouri", "Oklahoma", 
    "Ole Miss", "South Carolina", "Tennessee", "Texas A&M", "Texas", "Vanderbilt"
]

BIG_12_teams = ["asu","ariz","byu","bay","cin","colo","hou","isu","ku","ksu","okst","tcu","ttu","ucf","utah","wvu"]
BIG_12_teams_full = [
    "Arizona State", "Arizona", "Brigham Young (BYU)", "Baylor", "Cincinnati", 
    "Colorado", "Houston", "Iowa State", "Kansas", "Kansas State", 
    "Oklahoma State", "Texas Christian (TCU)", "Texas Tech", "Central Florida (UCF)", 
    "Utah", "West Virginia"
]

BIG_10_teams = ["ill","iu","iowa","md","msu","mich","minn","neb","nu","ohiost","ore","psu","pur","rutg","ucla","usc","wash","wis"]
BIG_10_teams_full = [
    "Illinois", "Indiana", "Iowa", "Maryland", "Michigan State", 
    "Michigan", "Minnesota", "Nebraska", "Northwestern", 
    "Ohio State", "Oregon", "Penn State", "Purdue", 
    "Rutgers", "UCLA", "USC", "Washington", "Wisconsin"
]


def build_csv(abv, name, conference):
    params1 = {
    "classification": "HighSchool",
    "team": {name},
    }
    headers = {
        "Authorization": "Bearer 7C8szdUBtn6yb4OU5/6ky4dglVZJ6dZ+LMGVhIeAqcnqK8RF90AcqFhDse2FXT6v"  # Replace with your actual API key
    }

    response = requests.get(url, headers=headers, params=params1)

    if response.status_code == 200:
        data1 = response.json()
    else:
        print(f"Error: {response.status_code}")

    params2 = {
        "classification": "JUCO",
        "team": {name},
    }

    response = requests.get(url, headers=headers, params=params2)

    if response.status_code == 200:
        data2 = response.json()
    else:
        print(f"Error: {response.status_code}")

    params3 = {
        "classification": "PrepSchool",
        "team": {name},
    }

    response = requests.get(url, headers=headers, params=params3)

    if response.status_code == 200:
        data3 = response.json()
    else:
        print(f"Error: {response.status_code}")

    data = data1+data2+data3
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
            jersey_num = "NA"

        try:
            height = player['height']
        except:
            height = 0

        try:
            dis_height = player['displayHeight']
        except:
            dis_height = "NA"

        try:
            weight = player['weight']
        except:
            weight = "NA"

        try:
            dis_weight = player['displayWeight']
        except:
            dis_weight = "NA"

        try:
            year = player['experience']['displayValue']
        except:
            year = "NA"

        try:
            birth_place = player['birthPlace']['displayText']
        except:
            birth_place = "NA"
        ranking = "NA"
        stars = "NA"
        recruiting_year = "NA"
        for person in data:
            test_height = person['height']
            test_weight = person['weight']
            if person['name'] == player_name and test_height in range(int(height)-2, int(height)+2) and test_weight in range(int(weight)-20,int(weight)+20) and person['year'] > 2016:
                ranking = person.get('ranking', "NA")
                stars = person.get('stars', "NA")
                recruiting_year = person.get('year', "NA")
                break  
        print(team_name + ": " + player_name + "|" + position + "|" + "Jersey: " + jersey_num + "|" + "Height: " + dis_height + "|" + "Weight: " + dis_weight +  "|" + year + "|" + birth_place)
        writer.writerow([conference, team_name, player_name,position, jersey_num, dis_height, dis_weight, year, birth_place, ranking, stars, recruiting_year])
    file.close()

def clear_rows():
    file = open("ravens_data.csv", "w")
    writer = csv.writer(file)
    writer.writerow(["CONFERENCE","TEAM", "NAMES", "POSITION", "JERSEY", "HEIGHT", "WEIGHT", "YEAR", "BIRTHPLACE","HS RANKING","HS STARS","RECRUITING YEAR"])

clear_rows()
for team,full_team in zip(ACC_teams,ACC_teams_full):
    conference2 = "ACC"
    build_csv(team, full_team, conference2)
for team,full_team in zip(PAC_12_teams,PAC_12_teams_full):
    conference2 = "PAC12"
    build_csv(team, full_team, conference2)
for team,full_team in zip(SEC_teams,SEC_teams_full):
    conference2 = "SEC"
    build_csv(team, full_team, conference2)
for team,full_team in zip(BIG_12_teams,BIG_12_teams_full):
    conference2 = "BIG12"
    build_csv(team, full_team, conference2)
for team,full_team in zip(BIG_10_teams,BIG_10_teams_full):
    conference2 = "BIG10"
    build_csv(team, full_team, conference2)
