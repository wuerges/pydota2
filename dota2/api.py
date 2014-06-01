from datetime import datetime

import requests

from .constants import HEROES, LOBBIES

STEAM_WEB_API = "https://api.steampowered.com/IDOTA2Match_570/{resource}/V001/?key={api_key}"


class Dota2HttpError(Exception):
    pass


class Api(object):

    def __init__(self, api_key):
        self.api_key = api_key

    def __repr__(self):
        return '<Dota2 Api: %s>' % self.api_key


    @property
    def is_valid(self):
        """Check if the API key is valid by making a single call to the Steam 
        API service."""

        return bool(self.get('GetMatchHistory'))

    def get(self, resource, params=None):
        """
        Returns a dictionary of the data requested from the Steam API.

        :param resource: Resource being requested e.g. "GetMatchHistory"
        :param params: Optional parameters to the requested resource as a dictionary. 
            For example, {matches_requested:10, account_id=111111}. This gets 
            added into the query string.
        """

        url = STEAM_WEB_API.format(resource=resource, api_key=self.api_key)
        response = requests.get(url, params=params)

        if response.status_code >= 400:
            # add more descriptive information
            raise Dota2HttpError("Failed to retrieve data: %s. URL: %s" % (response.status_code, url))

        return response.json()

class Dota2(object):

    def __init__(self, api_key=None):
        self._api = Api(api_key)

    def match(self, match_id, **kwargs):
        resource = 'GetMatchDetails'
        
        kwargs['match_id'] = match_id
        match = self._api.get(resource, kwargs)['result']

        return DetailedMatch(match)

    def match_history(self, **kwargs):
        resource = 'GetMatchHistory'

        matches = self._api.get(resource, kwargs)['result']['matches']

        return [Match(m) for m in matches]


class _X(dict):

    def __init__(self, raw_data):
        self.raw_data = raw_data

    def lookup(self, attribute):
        try:
            return self.raw_data[attribute]
        except KeyError:
            raise AttributeError("Attribute not available: %s" % attribute)


class Match(object):

    def __init__(self, raw_data):
        self.raw_data = raw_data

    def __repr__(self):
        return '<Match: %s>' % self.id

    @property
    def id(self):
        return self.raw_data['match_id']

    @property
    def players(self):
        return [Player(p) for p in self.raw_data['players']]

    @property
    def start_time(self):
        start_time = self.raw_data['start_time']

        return datetime.fromtimestamp(int(start_time))

    @property
    def sequence_number(self):
        return self.raw_data['match_seq_num']

    @property
    def lobby_type(self):
        lobby_type = self.raw_data['lobby_type']

        return LOBBIES[lobby_type]


class DetailedMatch(Match):

    @property
    def game_mode(self):
        pass

    @property
    def first_blood(self):
        """Seconds after game started where first blood occurred."""
        return self.raw_data['first_blood_time']

    @property
    def radiant_win(self):
        return bool(self.raw_data['radiant_win'])

    @property
    def players(self):
        return [DetailedPlayer(p) for p in self.raw_data['players']]


class Player(object):
    
    # SteamID for anonymous players who don't reveal their actual names
    anonymous_id = 4294967295

    def __init__(self, raw_data):
        self.raw_data = raw_data

    def __repr__(self):
        return "<Player: %s. %s. %s>" % (self.id, 'Radiant' if self.is_radiant else 'Dire', self.hero)

    @property
    def id(self):
        return self.raw_data['account_id']

    @property
    def hero_id(self):
        return self.raw_data['hero_id']

    @property
    def hero(self):
        # It's possible for there to be no hero chosen for a player 
        # especially if the game ended in the first minute or so
        return HEROES.get(self.hero_id,"")

    @property
    def slot(self):
        return self.raw_data['player_slot']

    @property
    def is_radiant(self):
        """
        Returns if the player is on the Radiant side or not (i.e. Dire). This 
        is based on the "player slot" 

        See:
            http://wiki.teamfortress.com/wiki/WebAPI/GetMatchHistory#Player_Slot
        """
        if self.slot < 100:
            return True
        else:
            return False

    @property
    def name(self):
        if self.account_id == self.anonymous_id:
            return "Anonymous"
        else:
            return "x"


class DetailedPlayer(Player):

    @property
    def level(self):
        return self.raw_data['']

    @property
    def kills(self):
        pass

    @property
    def deaths(self):
        pass

    @property
    def items(self):
        pass
