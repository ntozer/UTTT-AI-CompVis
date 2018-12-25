from math import inf


def simple_eval(engine):
    board = engine.board
    master_board = engine.master_board
    player = engine.player
    game_state = engine.game_state
    corners = [0, 2, 6, 8]
    sides = [1, 3, 5, 7]
    value = 0
    # TODO account for adjacent pieces
    for i in range(len(board)):
        for j in range(len(board[0])):
            board_pos = board[i][j]
            if board_pos is not None and master_board[i] is None:
                for k in [i, j]:
                    if k in corners:
                        value += 1.25 if board_pos == player else -1.25
                    elif k in sides:
                        value += 1 if board_pos == player else -1
                    else:
                        value += 1.5 if board_pos == player else -1.5
    for i in range(len(master_board)):
        if master_board[i] is not None:
            if i in sides:
                value += 10 if master_board[i] == player else -10
            elif i in corners:
                value += 12.5 if master_board[i] == player else -12.5
            else:
                value += 15 if master_board[i] == player else -15
    if game_state is not None:
        if game_state == 0:
            value = 0
        else:
            value = inf if game_state == player else -inf
    return value
