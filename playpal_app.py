"""
PlayPal App
"""

# import statements
from playpal_redis import PlayPI

if __name__ == '__main__':
    # authentification to access DB
    api = PlayPI('playpal')
    
    user_answer = input('Are you a new user? ')
    if user_answer == 'Yes':
        new_user_id = api.get_new_user_id()
        print('Your user ID is: ', new_user_id)
        
        while True:
            user_input_pass1 = input('Create a new password: ')
            user_input_pass2 = input('Re-enter the password: ')
            
            if user_input_pass1 == user_input_pass2:
                api.insert_one_user(new_user_id, user_input_pass2)
                print('Successfully added user!')
                break
            else:
                print('Passwords do not match; enter again.')
    elif user_answer == 'No':
        user_ID = input('What is your User ID? ')
        user_password = input('What is your password? ')
           
    # # learn about user 1's game history
    # games = api.get_all_games('1')
    # print(games)
    # print("User 1 has played:", len(games), "games.")
    # wins = api.get_all_wins('1')
    # print("\tUser 1 has won:", len(wins), "games.")
    # losses = api.get_all_losses('1')
    # print("\tUser 1 has lost:", len(losses), "games.")
    # draws = api.get_all_draws('1')
    # print("\tUser 1 has tied:", len(draws), "games.")

    # # show the game pattern for a game on board
    # print(api.game_pattern(1))

    # test game history function
    api.get_game_history("25")

