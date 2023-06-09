"""
Author: Josh Peirce
Date: 3/12/23

This class operates the game. It communicates with the players when it is their
it is their turn and tells them the state of the board. It also runs the
mainloop  and checks for the game being ower.
"""

from board import Board

class Game:
    """Class to hold info and play a game"""
    
    def __init__(self, p1, p2, p1id, p2id, n=3, tw=3):
        """Make a new game with players p1 and p2"""
        self.p1 = p1
        self.p2 = p2
        self.p1id = p1id
        self.p2id = p2id
        self.board = Board(size=n, to_win=tw)
        self.hist = ""

    def play(self):
        """Play a game returns winner_id, loser_id, history"""
        isx = True #Keep track of whose turn it is
        while not (
                self.board.check_x_wins() or 
                self.board.check_o_wins() or 
                len(self.board.get_empty_cells()) == 0):
            #Game loop:
            move = self.query_move(isx) #Get move from player
            self.board = self.board.add_piece(*move, isx) #add it to the board
            self.hist += str(self.board.convert_tuple_to_integer(*move))
            isx = not isx #Alternate turns
        #Handle end of game
        if self.board.check_x_wins():
            self.p1.win(self.board, self.hist)
            self.p2.lose(self.board, self.hist)
            return self.p1id, self.p2id, self.hist
        elif self.board.check_o_wins():
            self.p1.lose(self.board, self.hist)
            self.p2.win(self.board, self.hist)
            return self.p2id, self.p1id, self.hist
        else:
            self.p1.draw(self.board, self.hist)
            self.p2.draw(self.board, self.hist)
            return "0", "0", self.hist

    def query_move(self, isx):
        """Get a move from player.
        Keep asking until the player gives a legal move.
        This has the potential to infinitely loop - need to be careful here"""
        opts = self.board.get_empty_cells()
        move = None
        their_board = self.board.clone()
        while move not in opts:
            if isx:
               move = self.p1.play(their_board)
            else:
                move = self.p2.play(their_board)
        return move

def test():
    """Simple test for one game against a random player"""
    import player
    import ai_player
    px = player.Player(True)
    po = ai_player.RandomPlayer(False)
    game = Game(px, po)
    game.play()

if __name__ == "__main__":
    test()
