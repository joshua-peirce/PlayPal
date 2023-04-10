"""
PlayPal App
"""

# import statements
from playpal_redis import PlayPI


def start_app(api):
    """ PlayPal Game """
    # ask user if new or returning player
    user_answer = input("Welcome to PlayPal!\n\n"
                        "Login (1)\n"
                        "New User (2)\n"
                        "Close App (9)\n"
                        "-->   ")
    print()

    if user_answer == "9":
        print("Goodbye")
    else:
        if user_answer == "1":
            username = api.login()
            return

        elif user_answer == "2":
            # give new user_id
            new_user_id = api.get_new_id("users")
            print("Your User Id is", new_user_id)
            # make new account
            username = api.create_account(new_user_id)
            return

        # if anything else is entered
        else:
            start_app(api)


def main():
    # create and start the PlayPal API
    api = PlayPI('playpal')

    # run flushall to clear redis database
    #api.flush_all()

    # print the overall best first move
    api.overall_best_first_move()

    # use the app from terminal
    start_app(api)


if __name__ == '__main__':
    main()
