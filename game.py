"""
Author: Josh Peirce
Date: 3/12/23

This class operates the game. It communicates with the players when it is their
it is their turn and tells them the state of the board. It also runs the
mainloop  and checks for the game being ower.
"""

from board import Board

class Game:
    
    def __init__(self, p1, p2):
        """Make a new game with players p1 and p2"""
        self.p1 = p1
        self.p2 = p2
        self.board = Board(size=3, to_win=3)
        self.hist = []
        

    def play(self):
        """Play a game"""
        isx = True
        while not (self.board.check_x_wins() or self.board.check_o_wins()):
            move = self.query_move(isx)
            self.board = self.board.add_piece(*move, isx)
            self.hist.append(move)
            isx = not isx
        if self.board.check_x_wins():
            self.p1.win(self.hist)
            self.p2.lose(self.hist)
        else:
            self.p1.lose(self.hist)
            self.p2.win(self.hist)
        return self.hist 

    def query_move(self, isx):
        """Get a move from player.
        Keep asking until the player gives a legal move.
        This has the potential to infinitely loop - need to be careful here"""
        opts = self.board.get_empty_cells()
        move = None
        while move not in opts:
            print(move)
            if isx:
               move = self.p1.play(self.board)
            else:
                move = self.p2.play(self.board)
        return move
        
if __name__ == "__main__":
    import player #perhaps putting imports here is bad practice but idk
    px = player.Player(True)
    po = player.Player(False)
    game = Game(px, po)
    game.play()