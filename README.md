pydota2: Python wrapper for the Dota2 Web API
=========================================

This is a Python wrapper for the Steam Dota2 Web API to retrieve data on 
match histories and match details. You can request an API key 
from [here](http://steamcommunity.com/dev/apikey)

Installation
=============

Installation can be done via `pip` and should be Python 2 and 3 compatible:
```sh
pip install pydota2
```
The only dependency is the [requests](https://github.com/kennethreitz/requests) library. 

Usage
=======
Enter a valid API key:
```sh
>>> import dota2
>>> api_key = 'E5DAEA335681A46421D8EE7FF175E4BD'
>>> dota = dota2.Dota2(api_key)
>>> dota.is_valid # verify api key works
True
>>> dota.find_match_history()
[<Match 693301953, Co-op with bots>,
 <Match 693300359, Public matchmaking>,
 <Match 693299893, Public matchmaking>,
...
 <Match 693283739, Co-op with bots>]
```

Just calling `find_match_history` will return 25 of the most recent games. You can 
pass additional parameters to query a different set of matches as outlined
[here](http://wiki.teamfortress.com/wiki/WebAPI/GetMatchHistory#Method-specific_parameters).
For example `find_match_history(account_id=64931387, matches_requested=100)`

You can access match and player attributes:

```sh
>>> matches = dota.find_match_history(account_id=64931387, matches_requested=10)
>>> match = matches[0]
>>> match.id
712397156
>>> match.start_time
datetime.datetime(2014, 6, 10, 14, 58, 40)
>>> match.lobby_type
'Ranked'
>>> match.players 
[<Player 64931387, Radiant Dazzle>, 
<Player 101338368, Radiant Anti-Mage>, 
<Player 101971954, Radiant Queen of Pain>, 
...
<Player 4294967295, Dire Ancient Apparition>]
>>> match.players[5].hero
<Centaur Warrunner 96>
```

More Detailed Information
=========================

The Steam Web API lets you pull more detailed match information if you have the
match ID. You can call this information by:

```python
>>> match = dota.find_match(712397156)
>>> match
<DetailedMatch 712397156, Ranked>
>>> match.radiant_win
False
>>> match.duration
datetime.timedelta(0, 2000)
>>> match.duration.total_seconds()
2000.0
>>> match.kills_radiant
12
>>> match.kills_dire
37
>>> match.players[6].gpm
563
>>> match.players[6].kda
5.5
```

There is a difference between `Match` vs. `DetailedMatch` and `Player` vs. `DetailedPlayer` objects.
Detailed information is a separate API call. These objects will have much more information than
their counterparts, though. For example `DetailedPlayer` will have `kills`, `gpm`, and `items` during 
a match while `Player` will not. For a list of available detailed attributes see [here](http://wiki.teamfortress.com/wiki/WebAPI/GetMatchDetails)

Note that you can convert a regular player or match into a detailed player or match (at 
the cost of an additional API call) like so:

```python
>>> match
<Match 712360553, Ranked>
>>> match.to_detail(dota)
<DetailedMatch 712360553, Ranked>
```

Testing
==========
Download the sources and then run:
```bash
DOTA_API_KEY="<YOUR API KEY HERE>" python3 tests.py
```

Contributing
============
Please feel free to email me at jephdo@gmail.com.

You can also submit pull requests through [github](https://github.com/jephdo/pydota2).
