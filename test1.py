from re import A
from requests.auth import HTTPBasicAuth
import requests
from urllib.request import urlopen
import json

auth = "api_key=" + "RGAPI-0199010f-6df5-4602-af79-8d08ece8da26"

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

if __name__ == '__main__':
    wins= 0
    my_puuid = get_Puuid_from_sn("Zut de Flûte")
    print( " my puuid is " + my_puuid)
    my_latest_games = get_Match_list(my_puuid,20)
    #print(my_latest_games)
    #print("my latest game is : " + my_latest_games[0])
    latest_game = get_Match(my_latest_games[0])
    #print(latest_game["metadata"]["participants"])
    #print(get_Summoner_info_puuid(my_puuid))
    for game in my_latest_games:
        i=-1    
        cgame = get_Match(game)
        for e in cgame["metadata"]["participants"]:
            i+=1
            if e == my_puuid:
                print(get_Summoner_info_puuid(e)["name"] + get_Summoner_info_puuid(e)["id"])
                print("placement this game : " + str(cgame["info"]["participants"][i]["placement"]))
                if cgame["info"]["participants"][i]["placement"]<=4:
                    wins+=1
    print("TOTAL wins : " + str(wins) + " winrate : " + str(wins/20))