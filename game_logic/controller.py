from coord import Coord
from model import Engine

class Controller(Object):
    def __init__(self, engine):
        self.model = engine
    
    
    def restart(self):
        self.model.reset_game()

    
    def make_move(self, curr_move):
        if self.model.check_valid_move(curr_move):
            # movement updates
            self.model.board[curr_move.x][curr_move.y] = self.player
            self.model.prev_move = curr_move
            # game state updates
            self.model.update_master_board()
            self.model.update_game_state()
            # player updates
            self.model.update_player()