from telegram import InputMedia, InputMediaPhoto
import json, requests, os

BASE_URL = "https://public-api.tracker.gg/apex/v1/standard/profile/"
API_KEY = os.getenv('APEX_API_KEY')
HEADERS = {'TRN-Api-Key' : API_KEY}

def getStats(platform, name):
    url = BASE_URL + str(platform) + "/" + str(name)
    r = requests.get(url, headers=HEADERS)
    data = r.json()
    data = data['data']
    character_name = data['children'][0]['metadata']['legend_name']
    character_kills = data['stats'][1]['value']
    character_kills = int(character_kills)
    resp = "Current Banner Stats:\n*{}*\n*Kills:* {}".format(character_name, character_kills)
    return resp