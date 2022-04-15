# projet_0

For now all it does is return your recent games' placements, regardless of ranked, normal, double_up and shows your winrate and number of top#1s*
(which is actually false here because a 2nd in double_up is a first as you are paired)


How to use this script:
python3 test.py api_key

where api_key is your riot developer api key, which can be found on https://developer.riotgames.com/.
Also, your API key expires after one day, therefore you'll have to generate a new one at least once every day.




notes for myself (to differenciate game types and correctly count double_up top#1s): 
queue_id 
    1150 = double up
    1130 = hyper roll
    1100 = ranked
    1090 = normal
    1110 = tft tutorial
    1111 = tft test