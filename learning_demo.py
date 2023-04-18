"""
Demo for the "reinforcement learning" portion
"""

from playpal_redis import PlayPI
from ai_player import GoodPlayer
from player import Player
from game import Game
from tqdm import tqdm
    
N = 3
TW = 3

def demo(flush_db=False):
    #I chose the following IDs for the ai players
    p1id = "GOAT" 
    p2id = "LEGEND"

    #Start API
    api = PlayPI('demo')
    if flush_db:
        api.flush_all()

    #Make players
    p1 = GoodPlayer("X", api)
    p2 = GoodPlayer("O", api)
    p3 = Player(True)

    #Users plays 1 game before training
    g = Game(p3, p2, "YOU", p2id, n=N, tw=TW)
    g.play()
    
    #On a loop: train 1,000 games then play against user, alternating X and O
    while True:
        for _ in tqdm(range(1000)):
            g = Game(p1, p2, p1id, p2id, n=N, tw=TW)
            g.play()
        g = Game(p1, p3, "YOU", p2id, n=N, tw=TW)
        g.play()
        for _ in tqdm(range(1000)):
            g = Game(p1, p2, p1id, p2id, n=N, tw=TW)
            g.play()
        g = Game(p3, p2, "YOU", p2id, n=N, tw=TW)
        g.play()

if __name__ == "__main__":
    demo(flush_db=True)