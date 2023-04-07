import ai_player
import game
import pandas as pd
import random

NUM_GAMES = 10000
NUM_PLAYERS = 1000

def play_random_game(p1n, p2n):
    p1 = ai_player.RandomPlayer("X")
    p2 = ai_player.RandomPlayer("O")
    G = game.Game(p1, p2)
    return G.play()

if __name__ == "__main__":
    df = pd.DataFrame()
    for i in range(NUM_GAMES):
        #Make player names
        player_1_name = str(random.randrange(1, NUM_PLAYERS))
        player_2_name = str(random.randrange(1, NUM_PLAYERS))
        while player_1_name == player_2_name:
            #Not duplicate names
            player_2_name = "Player " + str(random.randrange(NUM_PLAYERS))
        #Play the game and get the result
        winner, hist = play_random_game(player_1_name, player_2_name)
        #Save the winner's name instead of piece
        if winner == "X":
            winner = player_1_name
        elif winner == "O":
            winner = player_2_name
        #Make a df to represent this result
        this = pd.DataFrame(
            {"Game_id": i,
             "P1": player_1_name,
             "P2": player_2_name,
             "Winner": winner,
             "History": str(hist)}, index=pd.Index([i])
            )
        this = this.set_index("Game_id")
        #Add this result to the dataframe
        df = pd.concat((df, this), axis=0)
        if i % (NUM_GAMES // 100) == 0:
            print(i)
    df.to_csv("game_data.csv")