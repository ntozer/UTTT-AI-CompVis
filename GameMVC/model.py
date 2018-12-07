from .coord import Coord

class Engine():
    def __init__(self):
        self.board = [[None for i in range(9)] for j in range(9)]
        self.master_board = [None for i in range(9)] # contains the win states of all other boards
        self.prev_move = Coord(None, None)
        self.player = 1
        self.game_state = None

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
        def player_won():
            if self.check_board_win(self.master_board):
                return True
            return False
        
        if player_won() or len(self.get_valid_moves()) == 0:
            self.game_state = 1 if self.player == 1 else -1 if self.player == 2 else 0

    def check_valid_move(self, curr_move):
        if curr_move is None:
            return False

        if self.check_board_win(self.master_board):
            return False

        if self.prev_move.x is not None:
            if self.prev_move.y != curr_move.x:
                if self.master_board[self.prev_move.y] is None:
                    return False
            
        try:
            if self.board[curr_move.x][curr_move.y] is not None:
                return False
            if self.master_board[curr_move.x] is not None:
                return False
        except IndexError:
            return False

        return True

    def get_valid_moves(self):
        valid_moves = []
        for i in range(9):
            if self.master_board[i] is None:
                for j in range(9):
                    if self.check_valid_move(Coord(i, j)):
                        valid_moves.append(Coord(i, j))

        return valid_moves

    def update_player(self):
        if self.player == 1:
            self.player = 2
        else:
            self.player = 1

    def reset_game(self):
        self.board = [[None for i in range(9)] for j in range(9)]
        self.master_board = [None for i in range(9)]
        self.prev_move = Coord(None, None)
        self.player = 1
        self.game_state = None
