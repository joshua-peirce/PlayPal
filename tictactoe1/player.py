"""
Author: Josh Peirce
Date: 3/14/23

This class serves as a base player, that uses the terminal. Not to be used in 
the final project, this is more a tool to validate the correctness of the other
classes
"""

class Player:

    def __init__(self, isx):
        """Initialize the player"""
        self.isx = isx

    def play(self, board):
        """Print the board to the console and query user for answer"""
        print("Your legal moves are:", board.get_empty_cells())
        for row in range(board.n):
            rowline = ""
            for col in range(board.n):
                rowline += board.get_cell_at(row, col) + " "
            print(rowline)
        print("Enter in format <row>, <col>. Example: 1, 1")
        move = [int(i) for i in input("Move: ").split(", ")]
        return tuple(move)
    
    def win(self, hist):
        """Basic win screen"""
        print("You win")

    def lose(self, hist):
        """Basic lose screen"""
        print("You lose")
