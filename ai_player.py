import random

class RandomPlayer:
    """Player that makes random moves"""
    def __init__(self, piece):
        """Constructor:do nothing"""
        pass

    def play(self, board):
        """Play a random move"""
        return random.choice(board.get_empty_cells())
    
    def win(self, hist):
        """Random player won: Do nothing"""
        pass

    def lose(self, hist):
        """Random player lost: Do nothing"""
        pass