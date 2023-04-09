"""
PlayPal App
"""

# import statements
from playpal_redis import PlayPI


def main():
    # authentification to access DB
    api = PlayPI('playpal')

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


if __name__ == '__main__':
    main()
