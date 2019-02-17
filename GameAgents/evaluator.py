corners = [0, 2, 6, 8]
sides = [1, 3, 5, 7]
middle = [4]


class Evaluator:
    def __init__(self, genome):
        self.features = self.get_features()
        self.genome_len = len(self.features)
        self.genome = genome
        self.player = None
        self.engine = None

    def get_features(self):
        a = self.count_active_middles
        b = self.count_active_corners
        c = self.count_active_sides
        d = self.count_board_winning_moves
        e = self.count_won_middles
        f = self.count_won_corners
        g = self.count_won_sides
        h = self.count_game_winning_boards
        i = self.count_game_winning_moves
        return [a, b, c, d, e, f, g, h, i]

    def eval(self, engine):
        self.engine = engine
        state_eval = 0
        if self.engine.game_state is not None:
            if self.engine.game_state == 0:
                return 0
            else:
                return 10000 if self.engine.game_state == 1 else -10000
        for player in [1, 2]:
            if self.engine.game_state is None:
                self.player = player
                player_eval = self.gene_eval()
                state_eval += player_eval if player == 1 else -1 * player_eval
        return state_eval

    def gene_eval(self):
        if len(self.genome) != len(self.features):
            raise Exception(f'Invalid genome length, genome is of length {len(self.genome)}, but should be {len(self.features)}')
        eval = 0
        for i in range(len(self.features)):
            eval += self.features[i]() * self.genome[i]
        return eval

    def get_active_boards(self):
        indices = list(filter(lambda i: self.engine.master_board[i] is None, range(9)))
        return list(map(lambda i: self.engine.board[i], indices))

    def count_active_corners(self):
        count = 0
        for board in self.get_active_boards():
            count += sum([1 for i in corners if board[i] == self.player])
        return count

    def count_active_sides(self):
        count = 0
        for board in self.get_active_boards():
            count += sum([1 for i in sides if board[i] == self.player])
        return count

    def count_active_middles(self):
        count = 0
        for board in self.get_active_boards():
            count += sum([1 for i in middle if board[i] == self.player])
        return count

    def count_board_winning_moves(self):
        count = 0
        for board in self.get_active_boards():
            board_count, _ = self.num_board_winners(board)
            count += board_count
        return count

    def num_board_winners(self, board):
        count = 0
        indices = []
        # checking verticals
        for vertical in list(map(lambda i: [board[i], board[i+1], board[i+2]], [0, 3, 6])):
            if vertical.count(self.player) == 2 and None in vertical:
                count += 1
                indices.append(vertical.index(None))
        # checking horizontals
        for horizontal in list(map(lambda i: [board[i], board[i + 3], board[i + 6]], [0, 1, 2])):
            if horizontal.count(self.player) == 2 and None in horizontal:
                count += 1
                indices.append(horizontal.index(None))
        # checking diagonals
        for diagonal in [[board[0], board[4], board[8]], [board[2], board[4], board[6]]]:
            if diagonal.count(self.player) == 2 and None in diagonal:
                count += 1
                indices.append(diagonal.index(None))
        return count, indices

    def count_game_winning_boards(self):
        count, _ = self.num_board_winners(self.engine.master_board)
        return count

    def count_game_winning_moves(self):
        count = 0
        _, indices = self.num_board_winners(self.engine.master_board)
        boards = list(map(lambda i: self.engine.board[i], indices))
        for board in boards:
            board_count, _ = self.num_board_winners(board)
            count += board_count
        return count

    def count_won_middles(self):
        count = 0
        for i in middle:
            if self.engine.master_board[i] == self.player:
                count += 1
        return count

    def count_won_sides(self):
        count = 0
        for i in sides:
            if self.engine.master_board[i] == self.player:
                count += 1
        return count

    def count_won_corners(self):
        count = 0
        for i in corners:
            if self.engine.master_board[i] == self.player:
                count += 1
        return count


def simple_eval(engine):
    board = engine.board
    master_board = engine.master_board
    player = engine.player
    game_state = engine.game_state
    value = 0
    # TODO account for adjacent pieces
    for i in range(len(board)):
        for j in range(len(board[0])):
            board_pos = board[i][j]
            if board_pos is not None and master_board[i] is None:
                if i in corners:
                    value += (1.25 if board_pos == 1 else -1.25)
                elif i in sides:
                    value += (1 if board_pos == 1 else -1)
                else:
                    value += (1.5 if board_pos == 1 else -1.5)

                if j in corners:
                    value += (0.375 if board_pos == 1 else -0.375)
                elif j in sides:
                    value += (0.25 if board_pos == 1 else -0.25)
                else:
                    value += (0.50 if board_pos == 1 else -0.50)
    for i in range(len(master_board)):
        if master_board[i] is not None:
            if i in sides:
                value += (10 if master_board[i] == 1 else -10)
            elif i in corners:
                value += (12.5 if master_board[i] == 1 else -12.5)
            else:
                value += (15 if master_board[i] == 1 else -15)
    if game_state is not None:
        if game_state == 0:
            value = 0
        else:
            value = 10000 if game_state == 1 else -10000

    return value
