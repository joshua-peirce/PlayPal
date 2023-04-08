"""
Author: Josh Peirce
Date: 3/14/23

This class serves as a base player, that uses the terminal. Not to be used in 
the final project, this is more a tool to validate the correctness of the other
classes
"""

import board

class Player:

    def __init__(self, isx):
        """Initialize the player"""
        self.isx = isx

    def play(self, board):
        """Print the board to the console and query user for answer"""
        print("Your legal moves are:", board.get_empty_cells())
        self.print_board(board)
        print("Enter in format <row>, <col>. Example: 1, 1")
        move = None
        while move == None:
            try:
                move = [int(i) for i in input("Move: ").split(", ")]
            except ValueError:
                print("Unable to read move (hint: don't include parentheses)")
        return tuple(move)
    
    def print_board(self, board):
        for row in range(board.n):
            rowline = ""
            for col in range(board.n):
                rowline += board.get_cell_at(row, col) + " "
            print(rowline)
    
    def win(self, board, hist):
        """Basic win screen"""
        self.end("win", board, hist)

    def lose(self, board, hist):
        """Basic lose screen"""
        self.end("lose", board, hist)

    def draw(self, board, hist):
        """Basic draw screen"""
        self.end("draw", board, hist)

    def end(self, ending, board, hist):
        """Generic end screen"""
        print("You " + ending)
        print("Final board:")
        self.print_board(board)

