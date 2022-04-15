from re import A
from requests.auth import HTTPBasicAuth
import requests
from urllib.request import urlopen
import json
import sys

auth = "api_key=" + sys.argv[1]

def get_Summoner_info_sn(summoner_name):
    url = "https://euw1.api.riotgames.com/tft/summoner/v1/summoners/by-name/" + summoner_name + "?" + auth
    response = requests.get(url)
    #print(url + summoner_name + auth)
    return response.text

def parser1(text):
	rmv_prthss = '{}"'
	for character in rmv_prthss:
		text = text.replace(character,"")
	text = text.split(",")
	for e in range(len(text)):
		text[e]=text[e].split(":")
	return text

def get_Puuid_from_sn(summoner_name):
    summoner_info = get_Summoner_info_sn(summoner_name)
    parsed_si = parser1(summoner_info)
    sn_puuid = parsed_si[2][1]
    return sn_puuid

def get_Match_list(puuid,count):
	url = "https://europe.api.riotgames.com/tft/match/v1/matches/by-puuid/"+ puuid + "/ids?count="+ str(count) +"&" + auth
	#print(url)
	response = urlopen(url)
	data_json = json.loads(response.read())
	return data_json


def get_Match(match_id):
	url = "https://europe.api.riotgames.com/tft/match/v1/matches/" + match_id + "?" + auth
	response = urlopen(url)
	data_json = json.loads(response.read())
	return data_json

def get_Summoner_info_puuid(puuid):
	url = "https://euw1.api.riotgames.com/tft/summoner/v1/summoners/by-puuid/" + puuid + "?" + auth
	response = urlopen(url)
	data_json = json.loads(response.read())
	return data_json

def get_winrate(summoner_name, count):
    wins = 0
    first = 0
    my_puuid = get_Puuid_from_sn(summoner_name)
    print( " my puuid is " + my_puuid)
    my_latest_games = get_Match_list(my_puuid,count)
    for game in my_latest_games:
        i=-1    
        cgame = get_Match(game)
        for e in cgame["metadata"]["participants"]:
            i+=1
            if e == my_puuid:
                #print(get_Summoner_info_puuid(e)["name"] + get_Summoner_info_puuid(e)["id"])
                print("placement for " + get_Summoner_info_puuid(e)["name"] + " in game " + game + " : " + str(cgame["info"]["participants"][i]["placement"]))
                if cgame["info"]["participants"][i]["placement"]<=4:
                    wins+=1
                    if cgame["info"]["participants"][i]["placement"]==1:
                        first+=1
    print("TOTAL wins : " + str(wins) + ", winrate : " + str(wins/count), ", Top#1s : " + str(first))

if __name__ == '__main__':
    get_winrate("Zut de Flûte", 50)