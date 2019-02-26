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
    total_kills = data['stats'][1]['value']
    total_kills = int(total_kills)
    #resp = "*Total Kills:* {}\n".format(total_kills)
    resp = ""
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