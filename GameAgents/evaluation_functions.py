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
            value = (100 if game_state == 1 else -100)
    return value
