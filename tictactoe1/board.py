"""
Author: Josh Peirce
Date: 3/12/23

This class holds all the information about the board needed to play the game.
The ideal workflow would have the board being passed from the server to the
players and they would pass back the corresponding moves. This implementation
allows for a  near-optimal space-complexity for storing the board. The 
theoretical minimum amount of information is that each cell in the nxn grid
can be one of three states, so ceil(n^2 * log2(3)) is the minimum number of bits
to store the board. This implementation achieves 2 * n^2 bits in the worst case,
Other operations, such as adding a piece or checking if the game is over are
also near-optimal. (I'm not brave enough to claim that they are optimal)
The integer representation works by assigning each cell a consecutive number. 
The top left gets 0, then it increments by 1 as you go across the top. Once you
get to the top right corner, it goes down one row and continues. In this
fashion, every cell on the board is assigned a number. The integer
representation works by writing out the board in binary in that order. So for
example:

    X | O | X
    - | - | -
    - | - | -
For computing the integer representation of the pieces on the board, we see that
there are pieces in cells 0, 1, and 2. Therefore in binary this board is written
as: 
    000000111
And this is the minimal representation. As for distinguishing between X and O,
we do the same procedure except only considering the X's on the board. So for 
our example, the integer representatin of x's pieces on the board is:
    000000101
Under the hood, this is how this class works.
"""

PIECE_X = "X"
PIECE_O = "O"
PIECE_EMPTY = "-"

class Board:
    def __init__(self, size=3, p=0, x=0, to_win=None, solutions=None):
        """
        Size is the size of the board, defaults to 3.
        p is the integer representation of the pieces on the board (see top)
        x is the integer representation of x's pieces on the board (see top)
        to_win is the number of pieces in a row a player needs to win.
        solutions is the set of winning combinations. If not provided, generates
        automatically upon initialization. However, this is expensive, so it
        is best to comput once and then pass to the constructor.
        """
        self.n = size
        self.p = p
        self.x = x
        self.tw = to_win
        if solutions is None:
            self.solutions = self.comp_solutions(self.n, to_win)
        else:
            self.solutions = solutions
        self.x_wins = self.check_x_wins()
        self.o_wins = self.check_o_wins()

    def comp_solutions(self, n, tw):
        """Generates the the set of all winning combinations."""
        wins = []
        if n < tw:
            return wins #No possible wins.
        #Start with horizontal
        for row in range(n):
            for col in range(n - tw + 1):
                start = col + n * row
                #Here we take advantage of them all being on order:
                wins.append(2 ** (start + tw) - 2 ** start)
        #Now vertical wins:
        for col in range(n):
            for row in range(n - tw + 1):
                start = col + n * row
                wins.append(
                    sum((2 ** i for i in range(start, start + n * tw, n))))
        #Now diagonal down-right
        for col in range(n - tw + 1):
            for row in range(n - tw + 1):
                start = col + n * row
                wins.append(
                    sum((2 ** i for i in range(
                        start, start + (n + 1) * tw, n + 1))))
        #Now diagonal down-left
        for col in range(tw - 1, n):
            for row in range(n - tw + 1):
                start = col + n * row
                wins.append(
                    sum((2 ** i for i in range(
                        start, start + (n - 1) * tw, n - 1))))
        return wins
    
    def check_player_wins(self, pieces):
        """Check if a player with the specified pieces wins"""
        return any((pieces & x == x for x in self.solutions))
    
    def check_x_wins(self):
        """Check if player x wins"""
        return self.check_player_wins(self.x)
    
    def check_o_wins(self):
        """Check if player o wins"""
        return self.check_player_wins(self.p - self.x)
    
    def add_piece(self, row, col, isx):
        """Place a new piece at (col, row) in the board
        Returns a new copy of the board rather than updating this one."""
        spot = row * self.n + col
        if isx:
            return Board(size=self.n,
                         p=self.p + 2 ** spot,
                         x=self.x + 2 ** spot,
                         to_win=self.tw,
                         solutions=self.solutions)
        else:
            return Board(size=self.n,
                         p=self.p + 2 ** spot,
                         x=self.x,
                         to_win=self.tw,
                         solutions=self.solutions)

    def get_empty_cells_integer(self):
        """Get a list of all open cells in the integer representation"""
        empty = 2 ** (self.n ** 2) - self.p - 1
        empty_cells = []
        for cell in range(self.n ** 2 - 1, -1, -1):
            if empty // (2 ** cell) == 1:
                empty_cells.append(cell)
                empty -= 2 ** cell
        return empty_cells
    
    def get_empty_cells(self):
        """Get the empty cells in (row, col) format"""
        return list(map(
            lambda x: (x // self.n, x % self.n),
            self.get_empty_cells_integer()))
    
    def get_seed(self):
        """Returns the simplest representation of the board"""
        return self.n, self.p, self.x
    
    def get_cell_at(self, row, col):
        """Get the piece that is kept at cell (col, row)"""
        i = row * self.n + col
        if self.x & 2 ** i > 0:
            return PIECE_X
        elif self.p & 2 ** i > 0:
            return PIECE_O
        return PIECE_EMPTY
    
if __name__ == "__main__":
    b = Board(size=21, to_win=10)
    print(len(b.solutions))