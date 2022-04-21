from re import A
from requests.auth import HTTPBasicAuth
import requests
from urllib.request import urlopen
import json
import sys
import numpy as np

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
    val_friends = 0
    cgame = get_Match(game)
    for e in cgame["metadata"]["participants"]:
        i+=1
        if e in puuid_list[1:]:
            friends.append(get_Summoner_info_puuid(e)["name"])
            val_friends+= 2**(puuid_list.index(e))
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
    return(game_type, placement,friends,val_friends)         

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
    output = np.zeros( (1, 4) ) # val_friends | games | wins | first
    my_puuid_list = []
    for summoner_name in summoner_name_list:
        my_puuid_list.append(get_Puuid_from_sn(summoner_name))
    #print(my_puuid_list)

    my_latest_games = get_Match_list(my_puuid_list[0],count)

    for game in my_latest_games: 
        rslt = get_placement_game_list(game, my_puuid_list)
        print(rslt)
        if match_type==rslt[0] or match_type=="any":
            games_count+=1
            if rslt[3] in output[:,0]:
                indx = np.where(output[:,0]==rslt[3])
                output[indx, 1]+=1
            else:
                output = np.append(output,[rslt[3],1,0,0])
                output = np.reshape(output, (len(output)//4,4))
            indx = np.where(output[:,0]==rslt[3])
            if rslt[1]<=4:
                wins+=1
                output[indx, 2]+=1
                if rslt[0]=="double_up":
                    if rslt[1]<=2:
                        first+=1
                        output[indx, 3]+=1
                        #print(rslt,"double up victory")
                else:
                    if rslt[1]==1:
                        first+=1
                        output[indx, 3]+=1
                        #print(rslt,"regular victory")
    print("In the last ",count," games you played, ",games_count, " matched the game type you indicated.")
    print("Wins: ", wins, "  Winrate: ", wins/games_count, "  Top#1s: ", first)
    return(output) 

def decompo_p2(n):
    L=[]
    p=1
    while n:
        q=n//2
        r=n%2
        if r:
            L.append(p)
        p*=2
        n=q
    return(L)

def show_names_winrates(list, output):
    i = 0
    for e in output[:,0]:
        n = e
        L = decompo_p2(n)
        friends=[]
        for a in L:
            friends.append(list[val_p2(a)])
        print("With", friends, ", you played", str(int(output[i,1])), "games, won", str(int(output[i,2])), "of them, and did", str(int(output[i,3])), "Top#1s. Winrate =", str((output[i,2]/output[i,1])*100),"%")
        i+=1
def val_p2(n):
    val = 0
    if n==0:
        return 0
    while n >= 2:
        val+=1
        n=n/2
    return val

if __name__ == '__main__':
    #get_winrate("Zut de Flûte", 20, "any")
    list = ("Zut de Flûte","APL Cha0s", "Apl Buble", "Kookie10","APL TasDeadCa","Rosette")
    output = get_winrate_list(list, 10, "any")
    print(output)
    show_names_winrates(list, output)