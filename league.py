"""
Everything League of Legends related in this bot is using an API key from Riot Games, thus all the stats received are from https://developer.riotgames.com/
"""

from telegram import InputMedia, InputMediaPhoto
import json, requests, os
from imagestuff import addToImage, createStatsImage

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

	#Save all the info to a list and return the list
	summoner_info.append(data["profileIconId"])
	summoner_info.append(data["name"])
	summoner_info.append(data["puuid"])
	summoner_info.append(data["summonerLevel"])
	summoner_info.append(data["accountId"])
	summoner_info.append(data["id"])
	summoner_info.append(data["revisionDate"])

	return summoner_info

#Method that returns the current version of the game (needed cause each patch == new version)
def getVersion():
	url = "https://ddragon.leagueoflegends.com/api/versions.json"
	r = requests.get(url)
	data = r.json()
	version = data[0]
	return version

#Method that returns a dictionary with champion keys / ids(names) as the keys / values
def getChampDictionary():
	champ_dict = {}

	#This url returns a json file that details a bunch of info about every champion in the game
	url = "http://ddragon.leagueoflegends.com/cdn/" + getVersion() + "/data/en_US/champion.json"
	r = requests.get(url)
	data = r.json()
	
	#For each champion in the json file, save their ID number and Name into a dictionary
	for champo in data["data"]:
		champ_dict[data["data"][champo]["key"]] = data["data"][champo]["id"]

	#Return the dictionary
	return champ_dict

#Method that returns a tuple with info regarding a players 5 most played champions
def getChampMastery(summoner_name):

	#Get a dictionary of champions and info about the requested player
	champ_dict = getChampDictionary()
	summoner_info = getSummonerInfo(summoner_name)
	summoner_id = summoner_info[5]

	#Make the API call based off of the player name given
	url = base_URL + "champion-mastery/v4/champion-masteries/by-summoner/" + summoner_id
	r = requests.get(url, headers=headers)
	data = r.json()
	champs = []
	points = []

	#Sort the json file returned so that the objects (champions) with the most mastery points are first.
	data = sorted(data, key = lambda i : i["championPoints"], reverse = True)

	#For each champion object, add the top 5 champions with the most mastery points to a list
	for champ in data:
		if not (len(champs) >= 3 and len(points) >= 3):
			champs.append(champ_dict.get(str(champ["championId"])))
			points.append(champ["championPoints"])
		else:
			break
	
	#Return a tuple with the lists of the champions and their respective mastery points
	return champs, points


def getRankedStats(summoner_name):
	summoner_info = getSummonerInfo(summoner_name)
	summoner_id = summoner_info[5]

	#Make the API call based off of the player name given
	url = base_URL + "league/v4/entries/by-summoner/" + summoner_id
	r = requests.get(url, headers=headers)
	data = r.json()
	resp = ""
	
	for queue in data:
		queue_type = queue['queueType']
		tier = queue['tier']
		rank = queue['rank']
		lp = queue['leaguePoints']

		if(queue_type == "RANKED_FLEX_SR"):
			queue_type = "Ranked Flex"
		elif(queue_type == "RANKED_SOLO_5x5"):
			queue_type = "Ranked Solo/Duo"
		elif(queue_type == "RANKED_TFT"):
			queue_type = "Ranked TFT"
		
		resp += "*{}:*\n{} {}, {}LP \n\n".format(queue_type, tier.capitalize(), rank, lp)

	return resp

#Method that will return an image detailing all the players and champions in a specified players game
def getCurrentGame(summoner_name):
	
	#Get a dictionary of champions and info about the requested player
	champ_dict = getChampDictionary()
	summoner_info = getSummonerInfo(summoner_name)

	#Make the API call based off of the player name given
	url = base_URL + "spectator/v4/active-games/by-summoner/" + summoner_info[5]
	r = requests.get(url, headers = headers)
	data = r.json()

	#Each player in the current game is its own json object
	participants = data['participants']
	players = []
	champs = []

	#For each player in the game, add their summoner name to a list and the champion they are playing to another list
	for player in participants:
		players.append(player['summonerName'])
		champs.append(champ_dict.get(str(player['championId'])))

	#For each player in the game, add their name and the champion they are playing to an image (method found in imagestuff.py)
	for i, player in enumerate(players):
		addToImage(player, champs[i], i)


def getAllStats(summoner_name):
	summoner_info = getSummonerInfo(summoner_name)
	summoner_name = summoner_info[1]
	summoner_id = summoner_info[5]


	#"globals" that will be needed to pass to image creation
	tier = ""
	rank = ""
	lp = ""

	#Make the API call based off of the player name given
	url = base_URL + "league/v4/entries/by-summoner/" + summoner_id
	r = requests.get(url, headers=headers)
	data = r.json()

	for queue in data:
		#go through the json until we find the solo queue stats
		if(queue['queueType'] != "RANKED_SOLO_5x5"):
			continue


		tier = queue['tier'].capitalize()
		rank = queue['rank']
		lp = queue['leaguePoints']

	if(tier == ""):
		tier = "Unranked"

	#Now rank tier and LP are grabbed. If player is unranked, then tier will be "Unranked" and rank / LP will be empty

	#Now we get Champ Mastery data
	champ_mastery_result = getChampMastery(summoner_name)
	count = 0
	reply = ""
	#For each champion (up to 5), add to a string their name and the points the player has on them.
	for champ in champ_mastery_result[0]:
		reply += champ + " - " + str(champ_mastery_result[1][count]) + "\n"
		count += 1

	champ1 = champ_mastery_result[0][0]
	champ1_pts = "{:,}".format(champ_mastery_result[1][0])
	champ2 = champ_mastery_result[0][1]
	champ2_pts = "{:,}".format(champ_mastery_result[1][1])
	champ3 = champ_mastery_result[0][2]
	champ3_pts = "{:,}".format(champ_mastery_result[1][2])

	#return "{} - {}\n{} - {}\n{} - {}\n".format(champ1, champ1_pts, champ2, champ2_pts, champ3, champ3_pts)
	
	createStatsImage(summoner_name, tier, rank, lp, champ1, champ2, champ3, champ1_pts, champ2_pts, champ3_pts)