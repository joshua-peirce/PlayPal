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
import random

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

    def get_pw(self, user_id):
        """ gets a user's pw """
        return self.r.hget(f'users:{user_id}', "pw")

    def user_rating(self, user_id):
        """ gets user rating as int """
        return int(self.r.hget(f'users:{user_id}', 'rating'))

    def user_skill(self, user_id):
        """ gets user skill """
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

        # if not a draw
        if winner != 0:
            self.update_winner(winner)
            self.update_loser(loser)

    def update_winner(self, user_id):
        """ update user's rating and skill after playing a game """

        # get users rating and skill
        rating = self.user_rating(user_id)
        skill = self.user_skill(user_id)
        # update rating
        if skill == 'beginner':
            # beginner winning adds 15 to rating
            self.update_rating(user_id, 15)
        elif skill == 'intermediate':
            # intermediate winning adds 10 to rating
            self.update_rating(user_id, 10)
        elif skill == 'advanced':
            # advanced winning adds 5 to rating
            self.update_rating(user_id, 5)
            # maximum rating of 500
            new_rating = self.user_rating(user_id)
            if new_rating > 500:
                self.set_rating(user_id, 500)

        # update skill with new points
        self.update_player_skill(user_id, rating, skill)

    def update_loser(self, user_id):
        """ update user's rating and skill after playing a game """
        # get users rating and skill
        rating = self.user_rating(user_id)
        skill = self.user_skill(user_id)
        # update rating
        if skill == 'beginner':
            # beginner loser subtracts 15 from rating
            self.update_rating(user_id, -5)
            # minimum rating of 0
            new_rating = self.user_rating(user_id)
            if new_rating < 0:
                self.set_rating(user_id, 0)
        elif skill == 'intermediate':
            # intermediate loser subtracts 10 from rating
            self.update_rating(user_id, -10)
        elif skill == 'advanced':
            # advanced loser subtracts 5 from rating
            self.update_rating(user_id, -15)

        # update skill with new points
        self.update_player_skill(user_id, rating, skill)

    def update_player_skill(self, user_id, rating, skill):
        """ updates a user's skill based on rating value """
        if rating <= 150:
            self.update_skill(user_id, 'beginner')
        elif rating > 150 and rating <= 350:
            self.update_skill(user_id, 'intermediate')
        elif rating > 350:
            self.update_skill(user_id, 'advanced')

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

    def valid_user(self, user_id, pw):
        """ checks if the user exists/they inputted pw correctly """
        # define hash key
        hash_key = f'users:{user_id}'

        # check if their user_id exists in user table
        if self.r.exists(hash_key):
            # get their password
            stored_pw = self.get_pw(user_id)

            # check if stored pw = entered pw
            if stored_pw == pw:
                return True
        # else
        return False

    def login(self):
        """ log user into PlayPal """

        # get user/pass from user
        username = input("User ID: ")
        password = input("Password: ")

        # check if the username/password combo exists
        valid_user = self.valid_user(username, password)

        # if logged in then play
        if valid_user:
            print('Login Successful')
            self.launch_app(username)

        else:
            print("Invalid User ID or Password.")
            user_answer = input("Enter 1 to login again, Enter 2 to make a new account. ")
            if user_answer == "1":
                self.login()
            else:
                new_user_id = self.get_new_id("users")
                print("Your User Id is", new_user_id)
                self.create_account(new_user_id)

    def create_account(self, new_user_id):
        """ make new user account """

        pw1 = input("Enter a password: ")
        pw2 = input("Enter your password again: ")
        # check passwords match
        if pw1 == pw2:
            # add new user to DB
            self.insert_one_user(new_user_id, pw2)
            print("Account Creation Successful. Please Login")
            self.login()

        else:
            print("Passwords don't match")
            self.create_account(new_user_id)

    def get_new_id(self, table):
        """ gets next highest id for particular table keys """
        max_id = 0
        cursor = 0
        while True:
            cursor, keys = self.r.scan(cursor, match=f"{table}:*")
            for key in keys:
                id = int(key.split(":")[1])
                if id > max_id:
                    max_id = id
            if cursor == 0:
                break
        next_id = max_id + 1
        return next_id


    def launch_app(self, user_id):
        """ PlayPal app with options to play a game or get game history """
        user_choice = int(input("Enter 1 to play a new game. Enter 2 to view your game history. "))

        if user_choice == 1:
            chosen_skill_level = input("Choose Game Level:\n"
                                       "Beginner (1), Intermediate (2), Advanced (3) \n"
                                       "Enter anything else for a random skill level.")
            opponent_id = self.get_opponent(user_id)
            opponent_skill = self.user_skill(opponent_id)
            print("You will be playing against a(n)", opponent_skill, "level player")

            # PLAY GAME HERE WITH USERNAME AND OPPONENT ID
            # JOSH - HERE
            # G = game.Game(username, opponent_id)
            # winner, loser, hist = G.play()
            game_id = self.get_new_id("games")
            print(game_id)
            winner, loser, hist = user_id, opponent_id, '72461'
            self.insert_one_game(game_id, user_id, opponent_id, winner, loser, hist)
            # PRINT FINAL BOARD




        elif user_choice == 2:
            self.get_game_history(user_id)

    def get_opponent(self, user_id, skill = "4"):
        """ get opponent's user id """

        # set skill level to indicated or randomly choose level
        if skill == "1":
            skill_level = "beginner"
        elif skill == "2":
            skill_level = "intermediate"
        elif skill == "3":
            skill_level = "advanced"
        else:
            skill_level = random.choice(['beginner', 'intermediate', 'advanced'])

        keys = self.r.keys('users:*')
        keys = [key.split(":")[1] for key in keys]

        all_opponents = [key for key in keys if self.user_skill(key) == skill_level and key != user_id]
        opponent_id = random.choice(all_opponents)

        return opponent_id










