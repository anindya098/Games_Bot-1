from telegram import InputMedia, InputMediaPhoto
import json, requests, os

BASE_URL = "https://public-api.tracker.gg/apex/v1/standard/profile/"
API_KEY = os.getenv('APEX_API_KEY')
HEADERS = {'TRN-Api-Key' : API_KEY}

def getStats(platform, name):
    url = BASE_URL + str(platform) + "/" + str(name)
    r = requests.get(url, headers=HEADERS)
    data = r.json()
    try:
        data = data['data']
    except KeyError:
        return "That's not a player, babe"
    try:
        rank = data['stats'][3]['value']
    except:
        rank = -1
    rank = rpToRank(rank)
    total_kills = data['stats'][1]['value']
    total_kills = int(total_kills)
    resp = "*{}*\n\n*Total Kills:* {}\n".format(rank, total_kills)
    for character in data['children']:
        character_name = character['metadata']['legend_name']
        resp += "*{}:* \n".format(character_name)
        for stat in character['stats']:
            char_stat_name = stat['metadata']['name']
            if(character_name == "Bangalore"):
                if(char_stat_name == "Legend Specific 1"):
                    char_stat_name = "Creeping Barrage: Damage"
                elif(char_stat_name == "Legend Specific 2"):
                    char_stat_name = "Smoke Grenade: Enemies Hit"
                elif(char_stat_name == "Legend Specific 3"):
                    char_stat_name = "Double Time: Distance"
            elif(character_name == "Bloodhound"):
                if(char_stat_name == "Legend Specific 1"):
                    char_stat_name = "Beast of the Hunt: Kills"
                elif(char_stat_name == "Legend Specific 2"):
                    char_stat_name = "Eye: Enemies Scanned"
                elif(char_stat_name == "Legend Specific 3"):
                    char_stat_name = "Eye: Traps Scanned"
            elif(character_name == "Caustic"):
                if(char_stat_name == "Legend Specific 1"):
                    char_stat_name = "NOX: Gas Damage Dealt"
                elif(char_stat_name == "Legend Specific 2"):
                    char_stat_name = "Gas Trap: Times Activated"
                elif(char_stat_name == "Legend Specific 3"):
                    char_stat_name = "NOX: Gassed Enemies Killed"
            elif(character_name == "Gibraltar"):
                if(char_stat_name == "Legend Specific 1"):
                    char_stat_name = "Bombardment: Kills"
                elif(char_stat_name == "Legend Specific 2"):
                    char_stat_name = "Dome: Damage Blocked"
                elif(char_stat_name == "Legend Specific 3"):
                    char_stat_name = "Gun Shield: Damage Blocked"
            elif(character_name == "Lifeline"):
                if(char_stat_name == "Legend Specific 1"):
                    char_stat_name = "Drop Pod: Items for Squadmates"
                elif(char_stat_name == "Legend Specific 2"):
                    char_stat_name = "Revive Shield: Damage Blocked"
                elif(char_stat_name == "Legend Specific 3"):
                    char_stat_name = "D.O.C. Drone: Healing"
            elif(character_name == "Mirage"):
                if(char_stat_name == "Legend Specific 1"):
                    char_stat_name = "Bamboozles"
                elif(char_stat_name == "Legend Specific 2"):
                    char_stat_name = "Encore: Executions Escaped"
                elif(char_stat_name == "Legend Specific 3"):
                    char_stat_name = "Decoys Created"
            elif(character_name == "Pathfinder"):
                if(char_stat_name == "Legend Specific 1"):
                    char_stat_name = "Zipline: Times Used by Squad"
                elif(char_stat_name == "Legend Specific 2"):
                    char_stat_name = "Grapple: Travel Distance"
                elif(char_stat_name == "Legend Specific 3"):
                    char_stat_name = "Survey: Beacons Scanned"
            elif(character_name == "Wraith"):
                if(char_stat_name == "Legend Specific 1"):
                    char_stat_name = "Rifts: Squadmates Phased"
                elif(char_stat_name == "Legend Specific 2"):
                    char_stat_name = "Phase Walk: Time"
                elif(char_stat_name == "Legend Specific 3"):
                    char_stat_name = "Voices: Warnings Heard"

            resp += "    *{}*: {}\n".format(char_stat_name, stat['displayValue'])

    return resp

def rpToRank(rp):
    """
    Bronze Starts at 0, 30 between each rank
    B4 - 0
    B3 - 30
    B2 - 60
    B1 - 90

    Silver Starts at 120, 40 between each rank
    S4 - 120
    S3 - 160
    S2 - 200
    S1 - 240

    Gold Starts at 280, 50 between each rank
    G4 - 280
    G3 - 330
    G2 - 380
    G1 - 430

    Plat Starts at 480, 60 between each rank
    P4 - 480
    P3 - 540
    P2 - 600
    P1 - 660

    Diamond Starts at 720, 70 between each rank
    D4 - 720
    D3 - 790
    D2 - 860
    D1 - 930

    Apex Predator is 1000+
    """

    if(rp >= 1000):
        return "Apex Predator"
    elif(rp >= 930):
        return "Diamond I"
    elif(rp >= 860):
        return "Diamond II"
    elif(rp >= 790):
        return "Diamond III"
    elif(rp >= 720):
        return "Diamond IV"
    elif(rp >= 660):
        return "Platinum I"
    elif(rp >= 600):
        return "Platinum II"
    elif(rp >= 540):
        return "Platinum III"
    elif(rp >= 480):
        return "Platinum IV"
    elif(rp >= 430):
        return "Gold I"
    elif(rp >= 380):
        return "Gold II"
    elif(rp >= 330):
        return "Gold III"
    elif(rp >= 280):
        return "Gold IV"
    elif(rp >= 240):
        return "Silver I"
    elif(rp >= 200):
        return "Silver II"
    elif(rp >= 160):
        return "Silver III"
    elif(rp >= 120):
        return "Silver IV"
    elif(rp >= 90):
        return "Bronze I"
    elif(rp >= 60):
        return "Bronze II"
    elif(rp >= 30):
        return "Bronze III"
    elif(rp >= 0):
        return "Bronze IV"
    elif(rp == -1):
        return "Unranked"
   
    