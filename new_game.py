"""
Date: 4/8/23

Normally I wouldn't put this in a new file
but it makes handling merge conflicts much easier
and it keeps all these functions in one place
feel free to put all the following code where it needs to go
- Josh
"""
import game
import player
import ai_player
import random

DIFFICULTIES = [1, 2, 3, 4] #easy, medium, hard, random
PIECES = [1, 2, 3] #X, O, random

def diff_prompt():
    """Tell the user the options for the difficulties they could play against"""
    print("Which difficulty would you like to play against:")
    print("""    1. Easy
    2. Medium
    3. Hard
    4. Surprise me!""")

def get_difficulty():
    """Get the difficulty of the opponent their supposed to play against"""
    diff = None
    while diff not in DIFFICULTIES:
        try:
            diff_prompt()
            diff = int(input(""))
            if diff == 4:
                return random.randrange(1, 4), True
        except ValueError:
            pass
    return diff, False

def piece_prompt():
    """Tell the user the options for the piece they could play as"""
    print("Which do you want to be:")
    print("""    1. X
    2. O
    3. Surprise me!""")

def get_user_piece():
    """Get the piece the user would like to play as"""
    piece = None
    while piece not in PIECES:
        try:
            piece_prompt()
            piece = int(input(""))
            if piece == 3:
                return random.randrange(1, 3)
        except ValueError:
            pass
    return piece

def get_opp(piece=None, diff=1):
    return ai_player.RandomPlayer(piece)

def new_game():
    """Have the user play a new game against the computer"""
    diff, show = get_difficulty()
    user_piece = get_user_piece()
    opp  = get_opp(piece=["O", "X"][user_piece], diff=diff)
    user = player.Player(user_piece == 1)
    if user_piece == 1:
        p1 = user
        p2 = opp
    else:
        p1 = opp
        p2 = user
    g = game.Game(p1, p2)
    g.play()
    if show:
        diff_str = "n easy" if diff == 1 else " medium" if diff == 2 else " hard"
        print()
        print(f"You played against a{diff_str} opponent!")

if __name__ == "__main__":
    new_game()