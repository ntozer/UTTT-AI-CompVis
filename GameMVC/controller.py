from GameMVC import *
from GameAgents import *
import pickle


class Controller():
    def __init__(self, root, params):
        self.model = Engine()
        self.view = View(root)
        self.view.pack(fill='both', expand=True)
        self.agent = MinimaxAgent(self.model)
        self.list_moves = params['list_moves']
        self.write_moves = False
        self.move_list = []
        self.simulate = False

    def handle_click(self, event):
        x = ord(event.widget['text'][0]) - 65
        y = int(event.widget['text'][1])
        move = Coord(x, y)
        if self.model.make_move(move) is not None:
            self.view.update_visuals(move, self.model.player)

            # output and record moves
            move_code = chr(move.x + 97) + str(move.y)
            if self.list_moves:
                print(move_code)
            if self.write_moves:
                self.move_list.append(move_code)
                if self.model.game_state is not None:
                    print(self.move_list)

    def make_agent_move(self, event):
        move = self.agent.compute_next_move()
        self.make_move(move)

    def handle_enter(self, event):
        x = ord(event.widget['text'][0]) - 65
        y = int(event.widget['text'][1])
        hover_coord = Coord(x, y)
        
        if self.model.check_valid_move(hover_coord):
            colors_to_use = self.view.valid_colors
        else:
            colors_to_use = self.view.invalid_colors
            
        if event.widget['bg'] == self.view.colors[0]:
            event.widget.configure(bg=colors_to_use[0])
        elif event.widget['bg'] == self.view.colors[1]:
            event.widget.configure(bg=colors_to_use[1])

    def handle_leave(self, event):
        if event.widget['bg'] in [self.view.valid_colors[0], self.view.invalid_colors[0]]:
            event.widget.configure(bg=self.view.colors[0])
        elif event.widget['bg'] in [self.view.valid_colors[1], self.view.invalid_colors[1]]:
            event.widget.configure(bg=self.view.colors[1])

    def restart_game(self, event):
        self.model.reset_game()
        self.view.reset_board()

    def bind_actions(self):
        for i in range(9):
            for j in range(9):
                self.view.board_spaces[i][j].bind("<Enter>", self.handle_enter)
                self.view.board_spaces[i][j].bind("<Leave>", self.handle_leave)
                self.view.board_spaces[i][j].bind("<Button-1>", self.handle_click)
        self.view.restart_btn.bind("<Button-1>", self.restart_game)
        self.view.simulate_btn.bind("<Button-1>", self.run_simulations)
        self.view.ai_move_btn.bind("<Button-1>", self.make_agent_move)
