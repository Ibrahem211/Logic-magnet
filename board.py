def create_board(n, purple_magnet_pos, iron, zero, red_magnet_pos=None):
    board = [['*' for _ in range(n)] for _ in range(n)]
    
    if purple_magnet_pos is not None and 0 <= purple_magnet_pos[0] < n and 0 <= purple_magnet_pos[1] < n:
        board[purple_magnet_pos[0]][purple_magnet_pos[1]] = 'P'
    else:
        print("purple magnet position is None or out of bounds; skipping placement.")

    if red_magnet_pos and 0 <= red_magnet_pos[0] < n and 0 <= red_magnet_pos[1] < n:
        board[red_magnet_pos[0]][red_magnet_pos[1]] = 'R'
    elif red_magnet_pos:
        print("red magnet position out of bounds.")

    for pos in iron:
        if 0 <= pos[0] < n and 0 <= pos[1] < n:
            board[pos[0]][pos[1]] = 'H'
        else:
            print(f"Error: Iron position {pos} out of bounds.")

    for pos in zero:
        if 0 <= pos[0] < n and 0 <= pos[1] < n:
            board[pos[0]][pos[1]] = 0
        else:
            print(f"Error: Zero position {pos} out of bounds.")

    return board, purple_magnet_pos
