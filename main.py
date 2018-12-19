import tkinter as tk
from GameMVC import Controller
from GameAgents import *
import sys


def create_agent(agent_type):
    if agent_type == 'random':
        return RandomAgent()
    elif agent_type == 'minimax':
        print('TODO: create minimax agent')
        return None
    elif agent_type == 'montecarlo':
        print('TODO: create montecarlo agent')
        return None
    elif agent_type == 'reinforcment':
        print('TODO: create RL agent')
        return None


def handle_cl_args(params):
    args = sys.argv
    if len(args) == 1:
        return
        
    if '-agent' in args:
        attempted_agent = args[args.index('-agent') + 1]
        if attempted_agent not in agent_types:
            print('ERROR: {} is not an agent type, defaulting to no agent'.format(attempted_agent))
        else:
            params['agent'] = create_agent(attempted_agent)

    if '-listmoves' in args:
        params['list_moves'] = True
    else:
        params['list_moves'] = False


def main():
    params = {'agent': None, 'list_moves': False}
    handle_cl_args(params)
    root = tk.Tk()
    app = Controller(root, params)
    app.bind_actions()
    root.after(1000, app.handle_next_move)
    root.geometry('396x378')
    root.title('Tic Tac Katsu')
    root.mainloop()


if __name__ == '__main__':
    main()
