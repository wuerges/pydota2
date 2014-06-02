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
```python
>>> import dota2
>>> api_key = 'A1B2C3D4E5F6'
>>> dota = dota2.Dota2(api_key)
>>> dota.is_valid # verify api key works
True
>>> dota.match_history()
[<Match 693301953, Co-op with bots>,
 <Match 693300359, Public matchmaking>,
 <Match 693299893, Public matchmaking>,
...
 <Match 693283739, Co-op with bots>]
```

Just calling `match_history` will return 25 of the most recent games. You can 
pass additional parameters to query a different set of matches as outlined
[here](http://wiki.teamfortress.com/wiki/WebAPI/GetMatchHistory#Method-specific_parameters).
For example `match_history(account_id=123456, matches_requested=100)`

You can access match and player attributes like so:

```python
>>> matches = dota.match_history(account_id=12356, matches_requested=10)
>>> match = matches[0]
>>> match.id
123456
>>> match.start_time

>>> match.lobby_type

>>> match.players 

>>> match.players[5].hero
```

More Detailed Information
=========================

The Steam Web API lets you pull more detailed match information if you have the
match ID. You can call this information by:

```python
>>> match = dota.match(123456)
>>> print(match)
class
>>> match.players
```

There is a difference between `Match` vs. `DetailedMatch` and `Player` vs. `DetailedPlayer` objects.
Detailed information is a separate API call. These objects will have much more information than
their counterparts, though. For example `DetailedPlayer` will have `kills`, `gpm`, and `items` during 
a match while `Player` will not. For a list of available detailed attributes see [here](http://wiki.teamfortress.com/wiki/WebAPI/GetMatchDetails)

Note that you can convert a regular player or match into a detailed player or match (at 
the cost of an additional API call) like so:

```python
>>> match
dd
>>> match.to_detail()
dd
```

Contributing
============
Please feel free to email me at jephdo@gmail.com.

You can also submit pull requests through [github](https://github.com/jephdo/pydota2).

