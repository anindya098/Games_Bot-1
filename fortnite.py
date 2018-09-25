import requests, json, os


def getStats(name, platform="pc"):
	base_URL = "https://api.fortnitetracker.com/v1/profile/"
	API_key = os.getenv('FORTNITE_API_KEY')
	headers = {'TRN-Api-Key' : API_key}
	url = base_URL + "/" + platform + "/" + name
	r = requests.get(url, headers=headers)
	data = r.json()

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

	resp = "{}'s Stats:\n\nSolo Kills: {}\nSolo K/D: {}\nSolo Wins: {}\n------------\nDuo Kills: {}\nDuo K/D: {}\nDuo Wins: {}\n------------\nSquad Kills: {}\nSquad K/D: {}\nSquad Wins: {}".format(epic_name, solo_kills, solo_kd, solo_wins, duo_kills, duo_kd, duo_wins, squad_kills, squad_kd, squad_wins)
	return(resp)

