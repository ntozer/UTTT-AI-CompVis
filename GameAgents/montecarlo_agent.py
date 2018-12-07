from .agent import Agent
from math import sqrt, log

class Node:
    def __init__(self, parent=None):
        self.move = None
        self.parent = parent
        self.children = []
        self.plays = 0
        self.value = 0


class MonteCarloAgent(Agent):
    def __init__(self, confidence):
        self.tree_root = Node()
        self.total_sims = 0
        self.c = confidence

    def ucb1(self, node):
        return node.value / node.plays + self.c * sqrt(log(self.total_sims) / node.plays)

    # finds the best node according to UCB1 and MCTS Selection process
    # TODO doesn't currently make moves as it parses the tree for the next move to explore
    def select(self):
        cur_node = self.tree_root
        while len(cur_node.children) != 0:
            max_ucb1 = self.ucb1(cur_node.children[0])
            best_child = cur_node.children[0]
            for child in cur_node.children:
                if self.ucb1(child) > max_ucb1:
                    max_ucb = self.ucb1(child)
                    best_child = child
            # TODO Make move with best child here
            # self.make_move
            cur_node = best_child
        return cur_node

    def expand(self, node, valid_moves):


    def compute_next_move(self, board, valid_moves):
        raise NotImplementedError
