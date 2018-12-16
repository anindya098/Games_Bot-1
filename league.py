import json, requests, os

#base_URL is the base URL for Riot's API. All calls extend this URL
#API_key is the API key proved by Riot that is needed to use the API
#headers is the list of headers for the requests we make to Riot's API
base_URL = "https://na1.api.riotgames.com/lol/"
API_key = os.getenv('RIOT_API_KEY')
headers = {'X-Riot-Token' : API_key}

#Returns a list containing summoner info
#info = [profileIconId, name, puuid, summonerLevel, accountId, id, revisionDate]
def getSummonerInfo(summoner_name):
	url = base_URL + "summoner/v4/summoners/by-name/" + summoner_name
	r = requests.get(url, headers=headers)
	data = r.json()
	summoner_info = []

	summoner_info.append(data["profileIconId"])
	summoner_info.append(data["name"])
	summoner_info.append(data["puuid"])
	summoner_info.append(data["summonerLevel"])
	summoner_info.append(data["accountId"])
	summoner_info.append(data["id"])
	summoner_info.append(data["revisionDate"])

	return summoner_info

def getVersion():
	url = "https://ddragon.leagueoflegends.com/api/versions.json"
	r = requests.get(url)
	data = r.json()
	version = data[0]
	return version

def getChampDictionary():

	champ_dict = {}
	url = "http://ddragon.leagueoflegends.com/cdn/" + getVersion() + "/data/en_US/champion.json"
	r = requests.get(url)
	data = r.json()
	
	for champo in data["data"]:
		champ_dict[data["data"][champo]["key"]] = data["data"][champo]["name"]

	return champ_dict

def getChampMastery(summoner_name):
	champ_dict = getChampDictionary()
	summoner_info = getSummonerInfo(summoner_name)
	summoner_id = summoner_info[5]
	url = base_URL + "champion-mastery/v4/champion-masteries/by-summoner/" + summoner_id
	r = requests.get(url, headers=headers)
	data = r.json()
	champs = []
	points = []

	for champ in data:
		if (champ["championLevel"] == 7):
			champs.append(champ_dict.get(str(champ["championId"])))
			points.append(champ["championPoints"])

	return champs, points