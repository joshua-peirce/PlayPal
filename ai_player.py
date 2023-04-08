import random

class RandomPlayer:
    """Player that makes random moves"""
    def __init__(self, piece):
        """Constructor:do nothing"""
        pass 

    def play(self, board):
        """Play a random move"""
        return random.choice(board.get_empty_cells())
    
    def win(self, board, hist):
        """Random player won: Do nothing"""
        pass

    def lose(self, board, hist):
        """Random player lost: Do nothing"""
        pass

    def draw(self, board, hist):
        """Random player drew: Do nothing"""
        pass