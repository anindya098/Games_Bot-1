from telegram import InputMedia, InputMediaPhoto
import json, requests, os

BASE_URL = "https://public-api.tracker.gg/apex/v1/standard/profile/"
API_KEY = 'b519f694-0607-47d4-b89a-02c555002fab'
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
    resp = "*Total Kills:* {}\n".format(total_kills)
    
    for character in data['children']:
        character_name = character['metadata']['legend_name']
        character_stat1_name = character['stats'][0]['metadata']['name']
        character_stat1_value = character['stats'][0]['displayValue']
        character_stat2_name = ''
        character_stat2_value = ''
        character_stat3_name = ''
        character_stat3_value = ''
        character_stat2 = True
        character_stat3 = True
        try:
            character_stat2_name = character['stats'][1]['metadata']['name']
            character_stat2_value = character['stats'][1]['displayValue']
        except:
            character_stat2 = False
        try:
            character_stat3_name = character['stats'][2]['metadata']['name']
            character_stat3_value = character['stats'][2]['displayValue']
        except:
            character_stat3 = False
        
        if(not character_stat2 and not character_stat3):
            resp += "\n*{}:*\n    *{}:* {}".format(character_name, character_stat1_name, character_stat1_value)
        elif(character_stat2 and not character_stat3):
            resp += "\n*{}:*\n    *{}:* {}\n    *{}:* {}".format(character_name, character_stat1_name, character_stat1_value, character_stat2_name, character_stat2_value)
        elif(character_stat2 and character_stat3):
            resp += "\n*{}:*\n    *{}:* {}\n    *{}:* {}\n    *{}:* {}".format(character_name, character_stat1_name, character_stat1_value, character_stat2_name, character_stat2_value, character_stat3_name, character_stat3_value)
        #resp += "\n*{}*\n    *{}:* {}\n    *{}:* {}\n    *{}:* {}".format(character_name, character_stat1_name, character_stat1_value, character_stat2_name, character_stat2_value, character_stat3_name, character_stat3_value)
    
    return resp