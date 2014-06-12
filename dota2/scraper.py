import json
import os
import time

try:
    import sqlalchemy as sa
except ImportError:
    HAS_SQLALCHEMY = False
else:
    HAS_SQLALCHEMY = True

def scrape(api, directory, sequence_number=None, matches_requested=None,
    matches_per_file=1000, sleep_delay=1):

    if matches_requested is None:
        matches_requested = 10000000

    scraped_matches = []
    
    while matches_requested > 0:
        matches = api.get_match_history_by_sequence(sequence_number)

        # no more matches to collect
        if not matches:
            break

        scraped_matches.extend(matches)

        if len(scraped_matches) > matches_per_file:
            write_to_file(directory, matches)

            # flush scraped_matches
            scraped_matches = []


        sequence_number = max(m.sequence_number for m in matches) + 1
        matches_requested = matches_requested - len(matches)

        time.sleep(sleep_delay)

def write_to_file(directory, matches):
    first_match, last_match = min(m.sequence_number for m in matches), max(m.sequence_number for m in matches)

    filename = "%s-%s" % (first_match, last_match) 
    path = os.path.join(directory, filename + '.json')

    with open(path, 'w') as outfile:
        json.dump([m.raw_data for m in matches], outfile, 
            sort_keys=True, indent=4)

    print('Processed (%s) matches from %s to %s' % (len(matches), 
        first_match, last_match))

def create_db(file):
    pass

def add_match_data_to_db(db):
    pass

# if HAS_SQLALCHEMY:
#     from sqlalchemy import Column, ForeignKey
#     from sqlalchemy import Boolean, DateTime, Integer, String, Text
#     Base = sa.ext.declarative.declarative_base()
    
#     class Match(Base):
#         __tablename__ = 'match'

#         id = Column(Integer, primary_key=True)
#         start_time = Column(DateTime)
#         sequence_number = Column(Integer)
        
#         # needs foreign key
#         lobby_type_id = Column(Integer)

#         # detailed match attributes
#         radiant_win = Column(Boolean)
#         duration = Column(Integer)
#         tower_status_radiant = Column(Integer)
#         tower_status_dire = Column(Integer)
#         barracks_status_radiant = Column(Integer)
#         barracks_status_dire = Column(Integer)
#         cluster = Column(Integer)
#         first_blood = Column(Integer)
#         human_players = Column(Integer)

#         # needs foreign key?
#         league_id = Column(Integer)

#         positive_votes = Column(Integer)
#         negative_votes = Column(Integer)

#         # needs foreign key
#         game_mode_id = Column(Integer)



#     class MatchPlayer(Base):
#         __tablename__ = 'matchplayer'

#         id = Column(Integer, primary_key=True)
#         match_id = Column(Integer, ForeignKey('match.id'))
#         player_id = Column(Integer, ForeignKey('player.id'))
#         hero_id = Column(Integer, ForeignKey('hero.id'))
#         slot_id = Column(Integer)
#         is_radiant = Column(Boolean)

#         # detailed player attributes
#         kills = Column(Integer)
#         deaths = Column(Integer)
#         assists = Column(Integer)
#         leaver_status = Column(Integer)
#         gold = Column(Integer)
#         last_hits = Column(Integer)
#         denies = Column(Integer)
#         gpm = Column(Integer)
#         xpm = Column(Integer)
#         gold_spent = Column(Integer)
#         hero_damage = Column(Integer)
#         tower_damage = Column(Integer)
#         hero_healing = Column(Integer)
#         level = Column(Integer)


#     class PlayerItem(Base):
#         __tablename__ = 'playeritem'
#         id = Column(Integer, primary_key=True)
#         match_player_id = Column(Integer, ForeignKey('matchplayer.id'))
#         item_id = Column(Integer, ForeignKey('item.id'))

#     class Lobby(Base):
#         pass

#     class GameMode(Base):
#         pass

#     class Hero(Base):
#         pass

#     class League(Base):
#         pass


#     class Item(Base):
#         id = Column(Integer, primary_key=True)
#         name = Column(String(255))
#         cost = Column(Integer)
