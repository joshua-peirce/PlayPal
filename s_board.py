"""
Author: Josh Peirce
Date: 4/15/23

This file contains all the functionality needed to "standardize" a board
position. The symmetry group of the game of tic-tac-toe is D4, and thus any game
of tic-tac-toe is isomorphic to (at most) 7 other games, and any position is 
isomorphic to at most 7 other positions. This means that the evaluation for one
position is the same as the other 7. Consider the following example:

    X | O | X
    - | - | -
    - | O | X

is isomorphic to:

    X | - | -
    O | - | O
    X | - | X

as well as:

    X | - | X
    O | - | O
    X | - | -

we can get from the starting to the ending position just by rotating or flipping
the board, according to the symmetry group D4.

When we save the evalutaion of a position, we want to "standardize" it in some
way, so that when we reach any of the isomorphic positions, we can use the same
evalutaion. Basically, we need a standard way to "pick" which isomorphism of the
board we wish to use.

Conveniently, because of the way the board class was designed, each distinct
board position is described by two numbers (along with the size and to-win of
each board; evaluations from boards with different n & tw values are useless).
We simply pick the isomorphism that has the lowest value of p, and if there is
a tie, we choose the one with the lowest value of x.
"""

import board, player

def flip_horiz(x, n=3):
    """Flip position x horizontally (this is fast; O(n))"""
    out = 0
    for rownum in range(n - 1, -1, -1):
        #Basically the idea here is we take each row
        #starting from the bottom, subtract it off the old array
        #and add it to the new one. We know this is safe because
        #x is an integer so it's copied into the stack and we're
        #not messing with and variables still in use elsewhere
        #thereby deleting the contents of some other board.
        old_row_end = 1 << (n * rownum)
        new_row_end = 1 << (n * (n - rownum - 1))
        row = int(x // old_row_end)
        x -= row * old_row_end
        out += row * new_row_end
    return out

def rotate_90(x, n=3):
    """Rotate a board by 90 deg. We need an order 4 permutation to generate
    the full group D4, but the specific direction we rotate doesn't matter.
    This operation is slower because I can't think of a fast way to do it, so
    it's O(n^2)"""
    out = 0
    for old_row in range(n):
        for old_col in range(n):
            old_mask = 1 << (n * old_row + old_col)
            new_row = old_col
            new_col = n - 1 - old_row
            new_mask = 1 << (n * new_row + new_col)
            out += new_mask * ((x & old_mask) == old_mask)
    return int(out)

def standardize(n, tw, p, x):
    """Generate all the symmetries, and simply take the smallest value"""
    symmetries = [[p, x], [flip_horiz(p, n=n), flip_horiz(x, n=n)]]
    for j in range(3):
        symmetries.append([rotate_90(i, n=n) for i in symmetries[-2]])
        symmetries.append([flip_horiz(i, n=n) for i in symmetries[-1]])
    return min(symmetries)

def standardize_board(b):
    """It's annoying that you have to cast from board to seed to board again,
    so this function does it for you:"""
    sol = standardize(*b.get_seed())
    return board.Board(size=b.n, 
                       to_win=b.tw,
                       p=sol[0],
                       x=sol[1],
                       solutions=b.solutions)

if __name__ == "__main__":
    import time
    pl = player.Player(True)
    
    p = 1 + 2
    x = 1

    b = board.Board(size=3, p=p, x=x)
    print()
    start = time.time()
    sb = standardize_board(b)
    end = time.time()
    print("time to flip: {:.3f}ms".format((end - start) * 1000))
