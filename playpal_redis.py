"""
PlayPal Redis API
Functions to be run in the PlayPal Driver App
"""

# import statements
import redis
import uuid
import time
import game
from tabulate import tabulate
import pandas as pd
from collections import Counter


class PlayPI:
    """ API simulating Tic Tac Toe Game """

    def __init__(self, channel, host='localhost', port=6379, db=0):
        """ initialize connection and flush any previous connection """
        self.r = redis.Redis(host=host, port=port, db=db, decode_responses=True)
        self.channel = channel

    def flush_all(self):
        self.r.flushall()

    def insert_one_user(self, user_id, pw, rating = 100, skill_level = 'beginner'):
        """ insert a single user """
        self.r.hmset(f'users:{user_id}', {'pw': pw, 'rating': rating, 'skill_level': skill_level})

    def insert_all_users(self, users):
        """ insert all users given a list of lists with user info """
        pipe = self.r.pipeline()
        for user_id, pw, rating, skill_level in users:
            pipe.hmset(f'users:{user_id}', {'pw': pw, 'rating': rating, 'skill_level': skill_level})
        pipe.execute()

    def get_user(self, user_id):
        """ gets info about a particular user """
        # fields to get about a user
        fields = ['pw', 'rating', 'skill_level']
        pw, rating, skill_level = self.r.hmget(f'users:{user_id}', fields)
        return(user_id, pw, rating, skill_level)

    def get_new_user_id(self):
        max_id = 0
        cursor = 0
        while True:
            cursor, keys = self.r.scan(cursor, match="users:*")
            for key in keys:
                user_id = int(key.split(":")[1])
                if user_id > max_id:
                    max_id = user_id
            if cursor == 0:
                break
        next_id = max_id + 1
        return next_id

    def user_rating(self, user_id):
        """ gets user rating as int """
        return int(self.r.hget(f'users:{user_id}', 'rating'))

    def user_skill(self, user_id):
        """ gets user rating """
        return self.r.hget(f'users:{user_id}', 'skill_level')

    def update_rating(self, user_id, amt):
        """ add/subtract certain amount to user rating after a game """
        return self.r.hincrby(f'users:{user_id}', 'rating', amt)
    
    def update_skill(self, user_id, new_skill):
        """ updates user rating """
        return self.r.hset(f'users:{user_id}', 'skill_level', new_skill)
    
    def set_rating(self, user_id, amt):
        """ sets rating to certain amount """
        return self.r.hset(f'users:{user_id}', 'rating', amt)

    def set_skil(self, user_id, skill):
        """ sets skill to certain level """
        return self.r.hset(f'users:{user_id}', 'skill_level', skill)

    def insert_one_game(self, game_id, p1, p2, winner, loser, game_pattern):
        """ insert a single game and update users' ratings and skill_levels """
        self.r.hmset(f'games:{game_id}',
                     {'player1': p1, 'player2': p2, 'winner': winner, 'loser': loser, 'game_pattern': game_pattern})

    def insert_all_games(self, games):
        """ insert all games given a list of lists with game info """
        pipe = self.r.pipeline()
        for game_id, p1, p2, winner, loser, game_pattern in games:
            self.r.hmset(f'games:{game_id}',
                         {'player1': p1, 'player2': p2, 'winner': winner, 'loser': loser, 'game_pattern': game_pattern})
        pipe.execute()

    def get_game(self, game_id):
        """ gets info about a particular user """
        # fields to get about a user
        fields = ['player1', 'player2', 'winner', 'loser', 'game_pattern']
        p1, p2, winner, loser, pattern = self.r.hmget(f'games:{game_id}', fields)
        return (game_id, p1, p2, winner, loser, pattern)

    def game_pattern(self, game_id):
        """ gets game pattern for particular game_id """
        return self.r.hget(f'games:{game_id}', 'game_pattern')

    def get_all_games(self, user_id):
        """ get all the games that particular user was in """
        game_ids = self.r.keys('games:*')  # get all game IDs
        user_games = []
        for game_id in game_ids:
            game_data = self.r.hgetall(game_id)
            if game_data['player1'] == user_id or game_data['player2'] == user_id:
                game_data_dict = dict(game_id=game_id.split(':')[1], **game_data)
                user_games.append(game_data_dict)
        return user_games

    def get_all_wins(self, user_id):
        """ get all the games that particular user was in """
        game_ids = self.r.keys('games:*')  # get all game IDs
        won_games = []
        for game_id in game_ids:
            game_data = self.r.hgetall(game_id)
            if game_data['winner'] == user_id:
                game_data_dict = dict(game_id=game_id.split(':')[1], **game_data)
                won_games.append(game_data_dict)
        return won_games

    def get_all_losses(self, user_id):
        """ get all the games that particular user was in """
        game_ids = self.r.keys('games:*')  # get all game IDs
        lost_games = []
        for game_id in game_ids:
            game_data = self.r.hgetall(game_id)
            if game_data['loser'] == user_id:
                game_data_dict = dict(game_id=game_id.split(':')[1], **game_data)
                lost_games.append(game_data_dict)
        return lost_games

    def get_all_draws(self, user_id):
        """ get all the games that particular user was in """
        game_ids = self.r.keys('games:*')  # get all game IDs
        tied_games = []
        for game_id in game_ids:
            game_data = self.r.hgetall(game_id)
            if game_data['player1'] == user_id or game_data['player2'] == user_id:
                if game_data['winner'] == '0':
                    game_data_dict = dict(game_id=game_id.split(':')[1], **game_data)
                    tied_games.append(game_data_dict)
        return tied_games

    def get_game_history(self, user_id):

        wins = self.get_all_wins(user_id)
        # most commonly played first move
        first_move = [int(game['game_pattern'][0]) for game in wins]
        counter = Counter(first_move)
        most_common_first = counter.most_common(1)[0][0]

        # show # of games won/lost by user
        games = len(self.get_all_games(user_id))
        wins = len(self.get_all_wins(user_id))
        losses = len(self.get_all_losses(user_id))
        draws = len(self.get_all_draws(user_id))

        # make sure they have played at least 1 game to avoid divide by 0
        if games != 0:
            win_rate = wins/games
        else:
            win_rate = 0

        
        table = [['Wins', 'Losses', 'Draws', 'Win Rate', 'Most Common'],
                 [wins, losses, draws, win_rate, most_common_first ]]

        print(tabulate(table, headers='firstrow', tablefmt='fancy_grid'))
