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

class ClientSidePlayer:

    def __init__(self, rc, ps, isx):
        print("Making client side player", isx)
        self.sols = board.Board(size=3, to_win=3).solutions
        self.rc = rc
        self.ps = ps
        if isx:
            self.piece = "X"
        else:
            self.piece = "O"
        self.console = Player(isx)
        self.mainloop()

    def mainloop(self):
        go = True
        while go:
            for message in self.ps.listen():
                if message["type"] == "message":
                    data = str(message["data"])[2:-2]
                    if data[0] == "a":
                        if data[1] == self.piece:
                            n, p, x = data[3:].split(", ")
                            b = board.Board(size=int(n), p=int(p), x=int(x), to_win=3, solutions=self.sols)
                            move = self.console.play(b)
                            move = b.convert_tuple_to_integer(*move)
                            self.rc.publish("game", "b" + str(move))
                    elif data[0] == 'c':
                        self.console.win(data[1:])
                    elif data[0] == 'd':
                        self.console.lose(data[1:])
                    elif data[0] == "e":
                        go = False
                        break
