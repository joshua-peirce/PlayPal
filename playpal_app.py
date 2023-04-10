"""
PlayPal App
"""

# import statements
from playpal_redis import PlayPI

def main():

    # authentification to access DB
    api = PlayPI('playpal')

    # ask user if new or returning player
    user_answer = int(input("Welcome to PlayPal!\n Enter 1 to login, Enter 2 to make a new account. "))

    if user_answer == 1:
        username = api.login()

    if user_answer == 2:
        # give new user_id
        new_user_id = api.get_new_user_id()
        print("Your User Id is", new_user_id)
        # make new account
        username = api.create_account(new_user_id)



if __name__ == '__main__':
    main()


