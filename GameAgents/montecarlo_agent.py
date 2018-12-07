from .agent import Agent
from math import sqrt, log
from random import randrange
# TODO use pickle to store decision tree
import pickle


class Node:
    def __init__(self, parent=None):
        self.move = None
        self.parent = parent
        self.children = []
        self.plays = 0
        self.value = 0
        self.depth = 0


class MonteCarloAgent(Agent):
    def __init__(self, confidence=sqrt(2)):
        self.tree_root = Node()
        self.cur_node = self.tree_root
        self.total_sims = 0
        self.c = confidence
        self.phase = 'Selection'

    # Upper Confidence Bound 1 applied to Trees (UCT)
    def uct(self, node):
        try:
            return node.value / node.plays + self.c * sqrt(log(self.total_sims) / node.plays)
        except ZeroDivisionError:
            return node.value / 1 + self.c * sqrt(log(self.total_sims) / 1)

    def select(self, last_move, valid_moves):
        if len(self.cur_node.children) == 0:
            return self.expand(valid_moves)

        if last_move.x is not None and self.cur_node.move != last_move:
            for child in self.cur_node.children:
                if child.move == last_move:
                    self.cur_node = child
            if len(self.cur_node.children) == 0:
                return self.expand(valid_moves)

        max_child = self.cur_node.children[0]
        max_uct = self.uct(max_child)
        for child in self.cur_node.children:
            if self.uct(child) > max_uct:
                max_uct = self.uct(child)
                max_child = child
        self.cur_node = max_child
        return self.cur_node.move

    def expand(self, valid_moves):
        for move in valid_moves:
            child = Node(parent=self.cur_node)
            child.move = move
            child.depth = self.cur_node.depth + 1
            self.cur_node.children.append(child)
        self.cur_node = self.cur_node.children[randrange(0, len(self.cur_node.children))]
        self.phase = 'Simulation'
        return self.cur_node.move

    def simulate(self, valid_moves):
        return valid_moves[randrange(0, len(valid_moves))]

    # -1 -> loss, 0 -> tie, 1 -> win
    def update(self, game_result):
        print(f'Simulation #{self.total_sims}\t\tResult: {game_result}\t\tTree Depth Achieved: {self.cur_node.depth}')
        self.total_sims += 1
        while self.cur_node is not None:
            self.cur_node.plays += 1
            if game_result == 0:
                self.cur_node.value += 0.5
            elif game_result == 1 and self.cur_node.depth % 2 == 1:
                self.cur_node.value += 1
            elif game_result == -1 and self.cur_node.depth % 2 == 0:
                self.cur_node.value += 1
            self.cur_node = self.cur_node.parent

    def play(self, last_move):
        if last_move.x is not None and self.cur_node.move != last_move:
            for child in self.cur_node.children:
                if child.move == last_move:
                    self.cur_node = child

        max_child = self.cur_node.children[0]
        max_wr = max_child.value / max_child.plays
        for child in self.cur_node.children:
            if (child.value / child.plays) > max_wr:
                max_wr = child.value / child.plays
                max_child = child
                print('Best Move: ({}, {})\t Win Rate: {}'.format(child.move.x, child.move.y, max_wr))
        self.cur_node = max_child
        return self.cur_node.move

    def reset_agent(self):
        self.phase = 'Selection'
        self.cur_node = self.tree_root

    def compute_next_move(self, valid_moves, last_move):
        if self.phase != 'Play':
            if self.phase == 'Selection':
                return self.select(last_move, valid_moves)
            elif self.phase == 'Simulation':
                return self.simulate(valid_moves)
        else:
            self.play(last_move)
