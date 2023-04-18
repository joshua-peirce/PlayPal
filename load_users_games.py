"""
PlayPal - Loading Users and Games into DB
"""
import pandas as pd

# import statements
from playpal_redis import PlayPI
import pandas
import time

# universal variables
USERS_FILE = 'user_table.csv'
GAMES_FILE = 'game_data.csv'
RATING_COL = 2
SKILL_COL = 3
P1_COL = 1
P2_COL = 2
WIN_COL = 3
LOSE_COL = 4

def load_users(filename, api):
    """
    loads users file into DB
    filename: csv with user data to be loaded in
    api: particular api to use functions to load csv
    """
    # read csv into dataframe of users
    users_df = pd.read_csv(filename)

    # all new users have rating = 100 and skill_level = 'beginner'
    users_df['rating'] = 100
    users_df['skill_level'] = 'beginner'

    # turn df into list of lists
    users_lst = users_df.values.tolist()

    # load user data into users table using api method
    api.insert_all_users(users_lst)

    #Return the number of users added
    return len(users_lst)

def load_games(filename, api):
    """
    loads games file into DB
    filename: csv with game data to be loaded in
    api: particular api to use functions to load csv
    """
    # read csv into dataframe of games
    start = time.time()
    games_df = pd.read_csv(filename)
    
    # turn df into list of lists
    games_lst = games_df.values.tolist()
    end = time.time()
    print("It took {:.3f} seconds to read the games df".format(end - start))

    for game in games_lst:
        # add game to database
        api.insert_one_game(*game)

    return len(games_lst)

def make_users_advanced(api, amt):
    """
    make some users advanced for intial game play
    amt - number of ids to update skill (advanced) and rating (500)
    """
    for id in range(amt):
        # update rating
        api.set_rating(id, 500)
        # update skill
        api.set_skill(id, 'advanced')

def main():

    # authentification to access DB
    api = PlayPI("playpal")
    api.flush_all()

    start_time = time.time()
    # insert all users
    lines = load_users(USERS_FILE, api)
    end_time = time.time()

    # set some users to advanced to start
    make_users_advanced(api, 50)

    # how many inserts per second
    insert_rate = round((lines / (end_time - start_time)), 2)

    print("We are able to load", insert_rate, "users / second.")

    # insert all games
    start_time = time.time()
    lines = load_games(GAMES_FILE, api)
    end_time = time.time()



    # how many inserts per second
    insert_rate = round((lines / (end_time - start_time)), 2)

    print("We are able to load", insert_rate, "games / second.")



if __name__ == '__main__':
    main()