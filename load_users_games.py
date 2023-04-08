"""
PlayPal - Loading Users and Games into DB
"""
import pandas as pd

# import statements
from playpal_redis import PlayPI
import pandas

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

def update_winner(user_id, api):
    """ update user's rating and skill after playing a game """

    # get users rating and skill
    rating = api.user_rating(user_id)
    skill = api.user_skill(user_id)
    # update rating
    if skill == 'beginner':
        # beginner winning adds 15 to rating
        api.update_rating(user_id, 15)
    elif skill == 'intermediate':
        # intermediate winning adds 10 to rating
        api.update_rating(user_id, 10)
    elif skill == 'advanced':
        # advanced winning adds 5 to rating
        api.update_rating(user_id, 5)
        # maximum rating of 500
        new_rating = api.user_rating(user_id)
        if new_rating > 500:
            api.set_rating(user_id, 500)

    # update skill based on new points
    if rating <= 150:
        api.update_skill(user_id, 'beginner')
    elif rating > 150 and rating <= 350:
        api.update_skill(user_id, 'intermediate')
    elif rating > 350:
        api.update_skill(user_id, 'advanced')


def update_loser(user_id, api):
    """ update user's rating and skill after playing a game """
    # get users rating and skill
    rating = api.user_rating(user_id)
    skill = api.user_skill(user_id)
    # update rating
    if skill == 'beginner':
        # beginner loser subtracts 15 from rating
        api.update_rating(user_id, -5)
        # minimum rating of 0
        new_rating = api.user_rating(user_id)
        if new_rating < 0:
            api.set_rating(user_id, 0)
    elif skill == 'intermediate':
        # intermediate loser subtracts 10 from rating
        api.update_rating(user_id, -10)
    elif skill == 'advanced':
        # advanced loser subtracts 5 from rating
        api.update_rating(user_id, -15)

    # update skill based on new points
    if rating <= 150:
        api.update_skill(user_id, 'beginner')
    elif rating > 150 and rating <= 350:
        api.update_skill(user_id, 'intermediate')
    elif rating > 350:
        api.update_skill(user_id, 'advanced')
def load_games(filename, api):
    """
    loads games file into DB
    filename: csv with game data to be loaded in
    api: particular api to use functions to load csv
    """
    # read csv into dataframe of games
    games_df = pd.read_csv(filename)

    # turn df into list of lists
    games_lst = games_df.values.tolist()


    for game in games_lst:
        # add game to database
        api.insert_one_game(*game)

        # update both users' rating and skill after a game
        winner_id = game[WIN_COL]
        loser_id = game[LOSE_COL]

        if winner_id != 0:
            update_winner(winner_id, api)
            update_loser(loser_id, api)

def main():

    # authentification to access DB
    api = PlayPI("playpal")
    api.flush_all()

    # insert all users
    load_users(USERS_FILE, api)
    # check users are loaded in by getting info about user 25
    print(api.get_user(25))

    # insert all games
    load_games(GAMES_FILE, api)
    # check games are loaded by getting info about game 11
    print(api.get_game(11))

    # check updated status of user 25 after playing a bunch of games
    print(api.get_user(25))



if __name__ == '__main__':
    main()