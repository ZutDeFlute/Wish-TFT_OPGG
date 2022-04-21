# projet_0

## CODE PURPOSE:
For now all it does is return your recent games' placements.
In the code you can specify the game type you want (will be argumented later maybe idk), possible arguments are: (any,normal,ranked,double_up,hyper_roll,tutorial,test) where "any" just retrieves data from all latest games regardless of a games' types.

## INFO/TODO:
If you ask for 20 games with "count" argument it will look at the last 20 games, but not give winrate over the last 20 "match_type" games specifically.
Max 20 API calls every sec, 100 API calls every 2min -> limited in API calls so calling a lot of games just to make sure "count" is equal to the actual number of "match_type" games will most likely return an "HTTP Error 429: Too Many Requests", this needs testing, I haven't yet payed attention to the number of API calls my code does.


## HOW TO USE:
```shell
python3 test1.py api_key
```
where **api_key** is your riot developer api key, which can be found on https://developer.riotgames.com/.
Also, your API key expires after one day, therefore you'll have to generate a new one at least once every day.




## NOTES FOR MYSELF:
queue_id (https://static.developer.riotgames.com/docs/lol/queues.json and observed data)
- 1150 = double up
- 1130 = hyper roll
- 1100 = ranked
- 1090 = normal
- 1110 = tft tutorial
- 1111 = tft test