"""
Everything fortnite related in this bot is using an API key from Fortnite Tracker, thus all the stats received are from https://fortnitetracker.com/
"""

from telegram import InputMedia, InputMediaPhoto
import requests, json, os

#Method that gets base stats for pc players for the current fortnite season 
def getStats(name, platform="pc"):
	
	#Make API call
	base_URL = "https://api.fortnitetracker.com/v1/profile/"
	API_key = os.getenv('FORTNITE_API_KEY')
	headers = {'TRN-Api-Key' : API_key}
	url = base_URL + "/" + platform + "/" + name
	r = requests.get(url, headers=headers)

	#The API call returns the data in json format so we have to use .json() so python treats it as json
	data = r.json()

	#Save all stats from the API into variables
	epic_name = data['epicUserHandle']
	solo_kills = data['stats']['curr_p2']['kills']['value']
	solo_wins = data['stats']['curr_p2']['top1']['value']
	solo_kd = data['stats']['curr_p2']['kd']['displayValue']
	duo_kills = data['stats']['curr_p10']['kills']['value']
	duo_wins = data['stats']['curr_p10']['top1']['value']
	duo_kd = data['stats']['curr_p10']['kd']['displayValue']
	squad_kills = data['stats']['curr_p9']['kills']['value']
	squad_wins = data['stats']['curr_p9']['top1']['value']
	squad_kd = data['stats']['curr_p9']['kd']['displayValue']

	#Create a string detailing all the player's stats. This will be returned to the calling function and sent to the telegram chat
	resp = "{}'s Stats:\n\nSolo Kills: {}\nSolo K/D: {}\nSolo Wins: {}\n------------\nDuo Kills: {}\nDuo K/D: {}\nDuo Wins: {}\n------------\nSquad Kills: {}\nSquad K/D: {}\nSquad Wins: {}".format(epic_name, solo_kills, solo_kd, solo_wins, duo_kills, duo_kd, duo_wins, squad_kills, squad_kd, squad_wins)
	return(resp)


#Method that gets items on sale in the Weekly Store
def getWeeklyStore():
	#Make API call to get the store contents
	url = "https://api.fortnitetracker.com/v1/store"
	API_key = os.getenv('FORTNITE_API_KEY')
	headers = {'TRN-Api-Key' : API_key}
	r = requests.get(url, headers=headers)

	#The API call returns the data in json format so we have to use .json() so python treats it as json
	data = r.json()

	resp = []

	#For loop that goes through every item in the store and checks if it is a weekly item
	for item in data:
		if(item['storeCategory'] == "BRWeeklyStorefront"):
			resp.append(InputMediaPhoto(media=item['imageUrl'], caption=item['name'] + " - " + str(item['vBucks']) + " V-Bucks"))

	#After adding all the weekly items to the resp list, return the list
	return(resp)


#Method that gets items on sale in the Daily Store
def getDailyStore():
	#Make API call to get the store contents
	url = "https://api.fortnitetracker.com/v1/store"
	API_key = os.getenv('FORTNITE_API_KEY')
	headers = {'TRN-Api-Key' : API_key}
	r = requests.get(url, headers=headers)

	#The API call returns the data in json format so we have to use .json() so python treats it as json
	data = r.json()

	resp = []

	#For loop that goes through every item in the store and checks if it is a daily item
	for item in data:
		if(item['storeCategory'] == "BRDailyStorefront"):
			resp.append(InputMediaPhoto(media=item['imageUrl'], caption=item['name'] + " - " + str(item['vBucks']) + " V-Bucks"))

	#After adding all the daily items to the resp list, return the list
	return(resp)


#Method that gets the weekly challenges for the current week of the season
def getChallenges():
	#Make API call
	url = "https://api.fortnitetracker.com/v1/challenges"
	API_key = os.getenv('FORTNITE_API_KEY')
	headers = {'TRN-Api-Key' : API_key}
	r = requests.get(url, headers=headers)

	#The API call returns the data in json format so we have to use .json() so python treats it as json
	data = r.json()
	resp = ""

	#The challenges are returned as json objects, so for each challenge we get lots of info about it
	for item in data['items']:
		challenge = item['metadata'][1]['value']
		current = item['metadata'][2]['value']
		total = item['metadata'][3]['value']
		reward = item['metadata'][5]['value']

		resp += "{}: {}/{} \n{} Battlestars\n\n".format(challenge, current, total, reward)

	#Return the string that contains all the info about this weeks challenges
	return resp


