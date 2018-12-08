from GameMVC import *
from GameAgents import *
import pickle


class Controller():
    def __init__(self, root, params):
        self.model = Engine()
        self.view = View(root)
        self.view.pack(fill='both', expand=True)
        try:
            self.agent = pickle.load(open('GameAgents/SavedAgents/MonteCarloAgent.p', 'rb'))
        except FileNotFoundError:
            self.agent = MonteCarloAgent()
        self.list_moves = params['list_moves']
        self.write_moves = False
        self.move_list = []
        self.simulate = False

    def handle_click(self, event):
        x = ord(event.widget['text'][0]) - 65
        y = int(event.widget['text'][1])
        move = Coord(x, y)
        self.make_move(move)

    def make_move(self, move):
        if self.model.check_valid_move(move):
            # movement updates
            self.model.board[move.x][move.y] = self.model.player
            self.model.prev_move = move
            # game state updates
            self.model.update_master_board()
            self.model.update_game_state()
            # update visuals
            self.view.update_visuals(move, self.model.player)
            # player updates
            self.model.update_player()
            
            # output and record moves
            move_code = chr(move.x + 97) + str(move.y)
            if self.list_moves:
                print(move_code)
            if self.write_moves:
                self.move_list.append(move_code)
                if self.model.game_state is not None:
                    print(self.move_list)

        if self.model.player == 2 and not self.simulate:
            self.make_agent_move()

    def make_agent_move(self):
        move = self.agent.compute_next_move(self.model.get_valid_moves(), self.model.prev_move)
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

    def restart_game(self, event=None):
        self.model.reset_game()
        self.view.reset_board()
        self.agent.reset_agent('Play')

    def simulation_restart(self):
        self.model.reset_game()
        self.view.reset_board()
        self.agent.reset_agent('Selection')

    def run_simulations(self, event):
        self.simulate = True
        sim_count = 0
        max_sim = int(self.view.simulate_txt.get('1.0', 'end-1c'))
        while sim_count < max_sim:
            self.agent.phase = 'Selection'
            while self.model.game_state is None:
                self.make_agent_move()
            self.agent.update(self.model.game_state)
            self.simulation_restart()
            if self.agent.total_sims % 10000 == 0:
                pickle.dump(self.agent, open('GameAgents/SavedAgents/MonteCarloAgent.p', 'wb'))
            sim_count += 1

    def bind_actions(self):
        for i in range(9):
            for j in range(9):
                self.view.board_spaces[i][j].bind("<Enter>", self.handle_enter)
                self.view.board_spaces[i][j].bind("<Leave>", self.handle_leave)
                self.view.board_spaces[i][j].bind("<Button-1>", self.handle_click)
        self.view.restart_btn.bind("<Button-1>", self.restart_game)
        self.view.simulate_btn.bind("<Button-1>", self.run_simulations)
