from coord import Coord

class Engine(object):
    def __init__(self):
        self.board = [[None] * 9] * 9
        self.master_board = [None] * 9 # contains the win states of all other boards
        self.prev_move = Coord(None, None)
        self.player = 'X'
        self.game_state = 0


    @staticmethod
    def check_board_win(board):
        # checking verticals
        for idx in [0, 3, 6]:
            if board[idx] is not None:
                if board[idx] == board[idx + 1] and board[idx] == board[idx + 2]:
                    return True
        # checking horizontals
        for idx in [0, 1, 2]:
            if board[idx] is not None:
                if board[idx] == board[idx + 3] and board[idx] == board[idx + 6]:
                    return True
        # checking diagonals
        if board[4] is not None:
            if board[0] == board[4] and board[0] == board[8]:
                    return True
            if board[2] == board[4] and board[2] == board[6]:
                    return True
        return False


    def update_master_board(self):
        if self.check_board_win(self.board[self.prev_move.x]):
            self.master_board[self.prev_move.x] = self.player


    def update_game_state(self):
        if player_won():
            self.game_state = self.player
        else: 
            self.game_state = 1

        def player_won():
            if self.check_board_win(self.master_board):
                return True
            return False


    def check_valid_move(self, curr_move):
        if self.prev_move.x is not None:
            if self.prev_move.y != curr_move.x:
                if self.master_board[self.prev_move.y] is None:
                    return False

        try:
            if self.board[curr_move.x][curr_move.y] is not None:
                return False
        except IndexError:
            return False

        return True

    
    def update_player(self):
        if self.player == 'X':
            self.player = 'O'
        else:
            self.player = 'X'


    def reset_game(self):
        self.board = [[None] * 9] * 9
        self.master_board = [None] * 9 # contains the current state of all other boards
        self.prev_move = Coord(None, None)
        self.player = 'X'
        self.game_state = 0
