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

def get_placement_game(game, puuid):
    i=-1
    game_type = "" 
    cgame = get_Match(game)
    for e in cgame["metadata"]["participants"]:
        i+=1
        if e == puuid:
            #print(get_Summoner_info_puuid(e)["name"] + get_Summoner_info_puuid(e)["id"])
            #print("placement for " + get_Summoner_info_puuid(e)["name"] + " in game " + game + " : " + str(cgame["info"]["participants"][i]["placement"]))
            placement = cgame["info"]["participants"][i]["placement"]
            match str(cgame["info"]["queue_id"]):
                case "1090":
                    game_type = "normal"
                case "1100":
                    game_type = "ranked"
                case "1110":
                    game_type = "tutorial"
                case "1111":
                    game_type = "test"
                case "1130":
                    game_type = "hyper_roll"
                case "1150":
                    game_type = "double_up"
    return(game_type, placement)

def get_placement_game_list(game, puuid_list):
    i=-1
    game_type = "" 
    friends = []
    cgame = get_Match(game)
    for e in cgame["metadata"]["participants"]:
        i+=1
        if e in puuid_list[1:]:
            friends.append(get_Summoner_info_puuid(e)["name"])
        if e == puuid_list[0]:
            #print(get_Summoner_info_puuid(e)["name"] + get_Summoner_info_puuid(e)["id"])
            #print("placement for " + get_Summoner_info_puuid(e)["name"] + " in game " + game + " : " + str(cgame["info"]["participants"][i]["placement"]))
            placement = cgame["info"]["participants"][i]["placement"]
            match str(cgame["info"]["queue_id"]):
                case "1090":
                    game_type = "normal"
                case "1100":
                    game_type = "ranked"
                case "1110":
                    game_type = "tutorial"
                case "1111":
                    game_type = "test"
                case "1130":
                    game_type = "hyper_roll"
                case "1150":
                    game_type = "double_up"
    return(game_type, placement,friends)         

def get_winrate(summoner_name, count, match_type):
    wins = 0
    first = 0
    games_count = 0
    my_puuid = get_Puuid_from_sn(summoner_name)
    print( " my puuid is " + my_puuid)
    my_latest_games = get_Match_list(my_puuid,count)
    for game in my_latest_games: 
        rslt = get_placement_game(game, my_puuid)
        print(rslt)
        if match_type==rslt[0] or match_type=="any":
            games_count+=1
            if rslt[1]<=4:
                wins+=1
                if rslt[0]=="double_up":
                    if rslt[1]<=2:
                        first+=1
                        print(rslt,"double up victory")
                else:
                    if rslt[1]==1:
                        first+=1
                        print(rslt,"regular victory")
    print("In the last ",count," games you played, ",games_count, " matched the game type you indicated.")
    print("Wins: ", wins, "  Winrate: ", wins/games_count, "  Top#1s: ", first)
                    
def get_winrate_list(summoner_name_list, count, match_type):
    wins = 0
    first = 0
    games_count = 0
    my_puuid_list = []
    for summoner_name in summoner_name_list:
        my_puuid_list.append(get_Puuid_from_sn(summoner_name))
    print(my_puuid_list)
    my_latest_games = get_Match_list(my_puuid_list[0],count)
    for game in my_latest_games: 
        rslt = get_placement_game_list(game, my_puuid_list)
        print(rslt)
        if match_type==rslt[0] or match_type=="any":
            games_count+=1
            if rslt[1]<=4:
                wins+=1
                if rslt[0]=="double_up":
                    if rslt[1]<=2:
                        first+=1
                        print(rslt,"double up victory")
                else:
                    if rslt[1]==1:
                        first+=1
                        print(rslt,"regular victory")
    print("In the last ",count," games you played, ",games_count, " matched the game type you indicated.")
    print("Wins: ", wins, "  Winrate: ", wins/games_count, "  Top#1s: ", first)
                    


if __name__ == '__main__':
    #get_winrate("Zut de Flûte", 20, "any")
    get_winrate_list(("Zut de Flûte","APL Cha0s", "Apl Buble", "Kookie10","APL TasDeadCa","Rosette"), 10, "any")