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
import new_game
from board import Board


class PlayPI:
    """ API simulating Tic Tac Toe Game """

    def __init__(self, channel, host='localhost', port=6379, db=0):
        """ initialize connection and flush any previous connection """
        self.r = redis.Redis(host=host, port=port, db=db,
                             decode_responses=True)
        self.channel = channel

    def flush_all(self):
        self.r.flushall()

    def insert_one_user(self, user_id, pw, rating=100, skill_level='beginner'):
        """ insert a single user """
        self.r.hmset(f'users:{user_id}', {
                     'pw': pw, 'rating': rating, 'skill_level': skill_level})

    def insert_all_users(self, users):
        """ insert all users given a list of lists with user info """
        pipe = self.r.pipeline()
        for user_id, pw, rating, skill_level in users:
            pipe.hmset(f'users:{user_id}', {
                       'pw': pw, 'rating': rating, 'skill_level': skill_level})
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

    def set_rating(self, user_id, amt):
        """ sets rating to certain amount """
        return self.r.hset(f'users:{user_id}', 'rating', amt)

    def set_skill(self, user_id, skill):
        """ sets skill to certain level """
        return self.r.hset(f'users:{user_id}', 'skill_level', skill)

    def insert_one_game(self, game_id, p1, p2, winner, loser, game_pattern):
        """ insert a single game and update users' ratings and skill_levels """
        self.r.hmset(f'games:{game_id}',
                     {'player1': p1, 'player2': p2, 'winner': winner, 'loser': loser, 'game_pattern': game_pattern})

        # keep track of winning first move in Redis
        # if X won, get their first move
        if winner == p1:
            self.r.lpush('winning_first_move', (str(game_pattern)[0]))
        # if O won, get their first move
        elif winner == p2:
            self.r.lpush('winning_first_move', (str(game_pattern)[1]))

        # if not a draw
        if winner != 0:
            self.update_rating_skill(winner, loser)
        else:
            self.update_draw(p1, p2)

    def update_draw(self, p1, p2):
        """ update users' skill and rating after a draw """
        p1_skill = self.user_skill(p1)
        p2_skill = self.user_skill(p2)
        if  p1_skill == 'beginner':
            if p2_skill == 'beginner':
                # p1 and p2 get 1 point
                self.update_rating(p1, 1)
                self.update_rating(p2, 1)
            elif p2_skill == 'intermediate':
                # p1 gets 3, p2 loses 3
                self.update_rating(p1, 3)
                self.update_rating(p2, -3)
            else:
                # p1 gets 5, p2 loses 5
                self.update_rating(p1, 5)
                self.update_rating(p2, -5)
        elif p1_skill == 'intermediate':
            if p2_skill == 'beginner':
                # p1 loses 3 and p2 gets 3
                self.update_rating(p1, -3)
                self.update_rating(p2, 3)
            elif p2_skill == 'intermediate':
                # p1 and p2 get 1
                self.update_rating(p1, 1)
                self.update_rating(p2, 1)
            else:
                # p1 gets 3, p2 loses 3
                self.update_rating(p1, 3)
                self.update_rating(p2, -3)
        elif p1_skill == 'advanced':
            if p2_skill == 'beginner':
                # p1 loses 5 and p2 gets 5
                self.update_rating(p1, -5)
                self.update_rating(p2, 5)
            elif p2_skill == 'intermediate':
                # p1 loses 3 and p2 gets 3
                self.update_rating(p1, -3)
                self.update_rating(p2, 3)
            else:
                # p1 and p2 gets 1
                self.update_rating(p1, 1)
                self.update_rating(p2, 1)


    def update_rating_skill(self, user_id, opponent_id):
        """
            update user's rating and skill after playing a game
            user_id is winner, opponent_id is loser
        """

        # get users rating and skill
        user_rating = self.user_rating(user_id)
        user_skill = self.user_skill(user_id)
        opp_rating = self.user_rating(opponent_id)
        opp_skill = self.user_skill(opponent_id)
        # update rating
        if user_skill == 'beginner':
            if opp_skill == 'beginner':
                # winner gets 5, loser loses 5
                self.update_rating(user_id, 15)
                self.update_rating(opponent_id, -15)
            elif opp_skill == 'intermediate':
                # winner gets 10, loser loses 10
                self.update_rating(user_id, 20)
                self.update_rating(opponent_id, -20)
            else:
                # winner gets 15, loser loses 15
                self.update_rating(user_id, 25)
                self.update_rating(opponent_id, -25)
        elif user_skill == 'intermediate':
            if opp_skill == 'beginner':
                # winner gets 10, loser loses 10
                self.update_rating(user_id, 10)
                self.update_rating(opponent_id, -10)
            elif opp_skill == 'intermediate':
                # winner gets 15, loser loses 15
                self.update_rating(user_id, 15)
                self.update_rating(opponent_id, -15)
            else:
                # winner gets 20, loser loses 20
                self.update_rating(user_id, 20)
                self.update_rating(opponent_id, -20)

        elif user_skill == 'advanced':
            if opp_skill == 'beginner':
                # winner gets 5, loser loses 5
                self.update_rating(user_id, 5)
                self.update_rating(opponent_id, -5)
            elif opp_skill == 'intermediate':
                # winner gets 10, loser loses 10
                self.update_rating(user_id, 10)
                self.update_rating(opponent_id, -10)
            else:
                # winner gets 15, loser loses 15
                self.update_rating(user_id, 15)
                self.update_rating(opponent_id, -15)

            # maximum rating of 500
            user_rating = self.user_rating(user_id)
            if user_rating > 500:
                self.set_rating(user_id, 500)
            elif user_rating < 0:
                self.set_rating(user_id, 0)

            opp_rating = self.user_rating(opponent_id)
            if opp_rating > 500:
                self.set_rating(opponent_id, 500)
            elif opp_rating < 0:
                self.set_rating(opponent_id, 0)

        # update skill with new points
        self.update_player_skill(user_id, user_rating)
        self.update_player_skill(opponent_id, opp_rating)



    def update_player_skill(self, user_id, rating):
        """ updates a user's skill based on rating value """
        if rating <= 150:
            self.set_skill(user_id, 'beginner')
        elif rating > 150 and rating <= 350:
            self.set_skill(user_id, 'intermediate')
        elif rating > 350:
            self.set_skill(user_id, 'advanced')

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
        p1, p2, winner, loser, pattern = self.r.hmget(
            f'games:{game_id}', fields)
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
                game_data_dict = dict(
                    game_id=game_id.split(':')[1], **game_data)
                user_games.append(game_data_dict)
        return user_games

    def get_all_wins(self, user_id):
        """ get all the games that particular user was in """
        game_ids = self.r.keys('games:*')  # get all game IDs
        won_games = []
        for game_id in game_ids:
            game_data = self.r.hgetall(game_id)
            if game_data['winner'] == user_id:
                game_data_dict = dict(
                    game_id=game_id.split(':')[1], **game_data)
                won_games.append(game_data_dict)
        return won_games

    def get_all_losses(self, user_id):
        """ get all the games that particular user was in """
        game_ids = self.r.keys('games:*')  # get all game IDs
        lost_games = []
        for game_id in game_ids:
            game_data = self.r.hgetall(game_id)
            if game_data['loser'] == user_id:
                game_data_dict = dict(
                    game_id=game_id.split(':')[1], **game_data)
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
                    game_data_dict = dict(
                        game_id=game_id.split(':')[1], **game_data)
                    tied_games.append(game_data_dict)
        return tied_games

    def get_game_history(self, user_id):

        # get number of games played by that user
        games = self.get_all_games(user_id)
        num_games = len(games)

        # get all their wins
        wins = self.get_all_wins(user_id)

        # if zero games, fill with zeros
        if num_games == 0:
            table = [['Wins', 'Losses', 'Draws', 'Win Rate (%)', 'Best First Position'],
                     [0, 0, 0, 0]]
            print('No game history yet. Play some games to generate data!')
        else:
            # get the first move on the board if they were player1
            first_move = [game['game_pattern'][0] if game['player1'] == user_id else
                          game['game_pattern'][1] for game in wins]
            # most commonly played first move by winner
            counter = Counter(first_move)
            most_common_first = int(counter.most_common(1)[0][0])
            most_common_first_coord = str(
                Board(size=3, to_win=3).convert_integer_to_tuple(most_common_first))

            # show # of games won/lost by user
            num_wins = len(wins)
            num_losses = len(self.get_all_losses(user_id))
            num_draws = len(self.get_all_draws(user_id))

            # make sure they have played at least 1 game to avoid divide by 0
            if num_games != 0:
                win_rate = (num_wins/num_games) * 100
            else:
                win_rate = 0

            # create the table to output summary stats to the user
            table = [['Wins', 'Losses', 'Draws', 'Win Rate (%)', 'Most Common First Position'],
                     [num_wins, num_losses, num_draws, win_rate, most_common_first_coord]]

        # tabulate library allows us pretty print the table
        game_hist_table = tabulate(
            table, headers='firstrow', tablefmt='fancy_grid')
        print(game_hist_table)

    def overall_best_first_move(self):
        """ gets the game history for the whole PlayPal API """
        # fetches all the winning first moves
        winning_first_moves = self.r.lrange('winning_first_move', 0, -1)

        # determines the most common first move that resulted in a win
        counter = Counter(winning_first_moves)
        most_common_first = int(counter.most_common(1)[0][0])

        # convert to human readable format
        most_common_first_coord = str(
            Board(size=3, to_win=3).convert_integer_to_tuple(most_common_first))
        print(most_common_first_coord)

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
            print('Login Successful\n')

            self.launch_app(username)

        else:
            print("Invalid User ID or Password.")
            user_answer = input("Login Again (1)\n"
                                "Create New Account (2)\n"
                                "Close App (9)\n"
                                "-->   ")
            if user_answer == "9":
                print("Goodbye!")
            else:
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
        user_choice = input("New Game (1)\n"
                            "Game History (2)\n"
                            "Close App (9)\n"
                            "-->   ")
        print()
        if user_choice == "9":
            print("Goodbye!")
            return
        else:
            if user_choice == "1":
                chosen_skill_level = input("Choose Game Level:\n"
                                           "Beginner (1), Intermediate (2), Advanced (3) \n"
                                           "Enter anything else for a random skill level.\n"
                                           "-->   ")
                print("\n")
                user_rating = self.user_rating(user_id)
                opponent_id = self.get_opponent(user_id, chosen_skill_level)
                opponent_rating = self.user_rating(opponent_id)
                opponent_skill = self.user_skill(opponent_id)
                print("You will be playing against a(n)",
                      opponent_skill, "level player")

                # PLAY GAME HERE WITH USERNAME AND OPPONENT ID
                # JOSH - HERE

                G = new_game.setup_game(user_id, opponent_id, opponent_skill)
                winner, loser, hist = G.play()

                # generate next game_id
                game_id = self.get_new_id("games")

                self.insert_one_game(
                    game_id, user_id, opponent_id, winner, loser, hist)
                # print info about game and updated rating
                if user_id == winner:
                    print('You beat a(n)', opponent_skill,
                          'player with a rating of', opponent_rating)
                elif user_id == loser:
                    print('You lost to a(n)', opponent_skill,
                          'player with a rating of', opponent_rating)
                else:
                    print('It was a tie between you and your opponent. They were a(n)', opponent_skill,
                          'level player with a rating of', opponent_rating)
                new_user_rating = self.user_rating(user_id)
                print('After playing, your new rating is', new_user_rating)

            elif user_choice == "2":
                self.get_game_history(user_id)

            # load app again
            print()
            self.launch_app(user_id)

    def get_opponent(self, user_id, skill="4"):
        """ get opponent's user id """

        # set skill level to indicated or randomly choose level
        if skill == "1":
            skill_level = "beginner"
        elif skill == "2":
            skill_level = "intermediate"
        elif skill == "3":
            skill_level = "advanced"
        else:
            skill_level = random.choice(
                ['beginner', 'intermediate', 'advanced'])

        keys = self.r.keys('users:*')
        keys = [key.split(":")[1] for key in keys]

        all_opponents = [key for key in keys if self.user_skill(
            key) == skill_level and key != user_id]
        opponent_id = random.choice(all_opponents)

        return opponent_id
