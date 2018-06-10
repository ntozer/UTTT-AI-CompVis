from coord import Coord
from model import Engine
from view import View

class Controller():
    def __init__(self):
        self.model = Engine()
        self.view = View()
    
    
    def restart(self):
        self.model.reset_game()

    
    def make_move(self, move):
        if self.model.check_valid_move(move):
            # movement updates
            self.model.board[move.x][move.y] = self.player
            self.model.prev_move = move
            # game state updates
            self.model.update_master_board()
            self.model.update_game_state()
            # player updates
            self.model.update_player()


    def run():
        #TODO: Add tkinter stuff here

        #game loop
        while(self.model.game_state is 0):
            #tkinter action on button gets coord
            self.make_move(move_coord)
