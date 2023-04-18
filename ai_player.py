import random
import s_board

EVALUATIONS = ["win", "loss", "draw"]

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

class GoodPlayer:
    """Player that learns from their mistakes"""
    def __init__(self, piece, api, print=False):
        self.piece = piece
        self.api = api
        self.print = print #View the AI's thought process
        self.isx = self.piece == "X"
        self.i_win = self.piece + "win"

    def play(self, board):
        """Play a more informed move.
        For every possible move, we query the api if this position has been seen
        before. Then choose the best one from those options, in the order:
        1. I win
        2. Unknown
        3. Draw
        4. I lose
        Also, if none of the outcomes is unknown (or one of them is i_win),
        the query saves that this position is the best of those outcomes.
        """
        if self.print: #If viewing thought process
            print("OLD:")
            self.print_board(board)

        #Get the available moves
        opts = board.get_empty_cells()
        evals = []

        for i in opts: #For each available move
            eval = self.eval_option(board, i) #Query API for eval
            if eval == self.i_win: #On a win - automatically return that option
                self.api.save_outcome(self.format_api_query(board), self.i_win)
                return i
            evals.append(eval)

        if None in evals: #2. If we don't know, explore first
            return opts[evals.index(None)]
        
        if "draw" in evals: #3. If it's between draws and losing, go w/ draw
            if self.print:
                print("Saving current state as a draw")
            self.api.save_outcome(self.format_api_query(board), "draw")
            return opts[evals.index("draw")]
        self.api.save_outcome(self.format_api_query(board), evals[0]) #4. Lose
        return random.choice(opts)

    def eval_option(self, board, opt):
        """Query the database to see what option we get
        Note: also check the board directly - if I have won in this position,
        I know the evaluation already. It's that I win."""

        #Get the board state after playing move `opt`
        new_board = board.add_piece(*opt, self.isx)

        #Check if this board state is already winning
        if self.isx:
            if new_board.check_x_wins():
                self.api.save_outcome(self.format_api_query(board), "Xwin")
                self.api.save_outcome(self.format_api_query(new_board), "Xwin")
                return "Xwin"
        else:
            if new_board.check_o_wins():
                self.api.save_outcome(self.format_api_query(board), "Owin")
                self.api.save_outcome(self.format_api_query(new_board), "Owin")
                return "Owin"
            
        #Since this game is not yet over, query the api
        query = self.format_api_query(new_board)
        eval = self.api.get_outcome(query)
        if self.print: #If debug
            print("EVALUATING:")
            self.print_board(new_board)
            print(query)
            print(eval)
            print()
        return eval

    def format_api_query(self, board):
        """Standardize board, and decompose seed into standard form for API"""
        b = s_board.standardize_board(board)
        return f"{b.n};{b.tw};{b.p};{b.x}"

    def win(self, board, hist):
        """Upon winning a game, save the last state as a win"""
        self.api.save_outcome(self.format_api_query(board), self.i_win)

    def lose(self, board, hist):
        """Upon losing a game, save the last state as a loss"""
        if self.isx:
            opiece = "O" #other piece
        else:
            opiece = "X"
        self.api.save_outcome(self.format_api_query(board), opiece + "win")

    def draw(self, board, hist):
        """Upon drawing a game, save the last state as a draw"""
        self.api.save_outcome(self.format_api_query(board), "draw")

    def print_board(self, board):
        """Debugging method to print the board"""
        for row in range(board.n):
            rowline = ""
            for col in range(board.n):
                rowline += board.get_cell_at(row, col) + " "
            print(rowline)
