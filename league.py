import json, requests, os

#base_URL is the base URL for Riot's API. All calls extend this URL
#API_key is the API key proved by Riot that is needed to use the API
#headers is the list of headers for the requests we make to Riot's API
base_URL = "https://na1.api.riotgames.com/lol/"
API_key = os.getenv('RIOT_API_KEY')
headers = {'X-Riot-Token' : API_key}


class Summoner:

	#Lists the account and summoner id's for everyone searched
	account_ID = []
	summoner_ID = []

	def __init__(self, name):
		self.summoner_name = name

		#basic_info is a json file containing very basic summoner info
		self.basic_info = self.get_summoner_by_name()

		#account_ID is the account ID for the summoner
		self.account_ID = self.get_account_ID()
		Summoner.account_ID.append(self.account_ID)

		#summoner_ID is the summoner ID for the summoner
		self.summoner_ID = self.get_summoner_ID()
		Summoner.summoner_ID.append(self.summoner_ID)
		
		self.ranked_info = self.get_league_by_summoner()

		self.champ_mastery_info = self.get_champion_mastery_by_summoner()

		#level is the level of the summoner
		self.level = self.get_level()

		#rank is the 1-5 for tier
		self.rank = self.get_rank()

		#division is summoner tier(eg: gold, silver, bronze etc)
		self.division = self.get_division()

		#Points earned in ranked
		self.lp = self.get_LP()

		#number of wins in ranked
		self.rank_wins = self.get_rank_wins()
		
		#number of losses in ranked
		self.rank_loss = self.get_rank_loss()

		

	#returns a json file containing summoner's basic info
	def get_summoner_by_name(self):
		url = base_URL + "summoner/v3/summoners/by-name/" + self.summoner_name
		
		#make a get request to the url using the specified headers
		r = requests.get(url, headers=headers)
		data = r.json()

		return data		

	def get_league_by_summoner(self):
		url = base_URL + "league/v3/positions/by-summoner/" + str(self.summoner_ID)
	
		r = requests.get(url, headers=headers)
		data = r.json()

		return data

	def get_champion_mastery_by_summoner(self):
		url = base_URL + "champion-mastery/v3/champion-masteries/by-summoner/" + str(self.summoner_ID)

		r = requests.get(url, headers=headers)
		data = r.json()
		return data

	#returns summoner's account id as an int
	def get_account_ID(self):
		a_ID = self.basic_info['accountId']
		return a_ID
	#returns summoner's summoner id as an int
	def get_summoner_ID(self):
		s_ID = self.basic_info['id']
		return s_ID
	#returns summoner's level as an int
	def get_level(self):
		level = self.basic_info['summonerLevel']
		return level

	#Returns summoner's division (Bronze, Silver, etc.)
	def get_division(self):
		division = self.ranked_info[0]['tier']
		return division

	#Returns summoner's rank (I , II, III, etc.)
	def get_rank(self):
		rank = self.ranked_info[0]['rank']
		return rank

	#Returns summoner's LP
	def get_LP(self):
		lp = self.ranked_info[0]['leaguePoints']
		return lp

	#Returns number of ranked wins for summoner
	def get_rank_wins(self):
		r_wins = self.ranked_info[0]['wins']
		return r_wins

	#Returns number of ranked losses for summoner
	def get_rank_loss(self):
		r_loss = self.ranked_info[0]['losses']
		return r_loss

	def get_top_10_masteries(self):
		champ_mastery_lst = self.champ_mastery_info
		champs = []
		points = []

		for i in range(10):
			champs.append(champ_mastery_lst[i]['championId'])
			points.append(champ_mastery_lst[i]['championPoints'])

		for i in range(10):
			print(str(champs[i]) + "\t-\t" + str(points[i]))

	def get_rank_7_champs(self):
		champ_mastery_lst = self.champ_mastery_info
		level_7 = []
		for champ_obj in champ_mastery_lst:
			if (champ_obj['championLevel'] == 7):
				level_7.append(champ_obj['championId'])

		return level_7

"""
def main():
	s = Summoner("l am inting")
	print(s.get_rank_7_champs())
	s.get_top_10_masteries()

	p = Summoner("Monorpale")
	print("Class:")
	print("Summoner:", Summoner.account_ID)
	print("Summoner:", Summoner.summoner_ID)
	print("Obj:")
	print(s.summoner_name + ": " + str(s.account_ID))
	print(s.summoner_name + ": " + str(s.summoner_ID))
	print(s.summoner_name + ":", s.level)
	print("bobby:")
	print(p.summoner_name + ": " + str(p.account_ID))
	print(p.summoner_name + ": " + str(p.summoner_ID))
	print(p.summoner_name + ":", p.level)

	print(s.summoner_name + ":")
	print(s.division + " " + s.rank + ", " + str(s.lp) + " LP")


main()

"""