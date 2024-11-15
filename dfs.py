import copy

def dfs_solve(board, purple_magnet_pos, n, red_magnet_pos=None):
    start_state = {
        'board': copy.deepcopy(board),
        'purple_pos': purple_magnet_pos,
        'red_pos': red_magnet_pos,
        'steps': []
    }

    stack = [start_state]
    visited = set()
    visited.add((tuple(map(tuple, start_state['board'])), start_state['purple_pos'], start_state['red_pos']))

    while stack:
        current_state = stack.pop()

        if check_win(current_state['board']):
            print("Solution found:", current_state['steps'])
            return current_state['steps']

        if current_state['purple_pos']:
            purple_moves = possible_moves(current_state['board'], current_state['purple_pos'], n)
            for move in purple_moves:
                new_state = apply_move(current_state, 'P', move)
                board_hash = (tuple(map(tuple, new_state['board'])), new_state['purple_pos'], new_state['red_pos'])
                if board_hash not in visited:
                    stack.append(new_state)
                    visited.add(board_hash)

        if current_state['red_pos']:
            red_moves = possible_moves(current_state['board'], current_state['red_pos'], n)
            for move in red_moves:
                new_state = apply_move(current_state, 'R', move)
                board_hash = (tuple(map(tuple, new_state['board'])), new_state['purple_pos'], new_state['red_pos'])
                if board_hash not in visited:
                    stack.append(new_state)
                    visited.add(board_hash)

    print("No solution found.")
    return None 



def possible_moves(board, magnet_pos, n):
    moves = []
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for dx, dy in directions:
        new_x, new_y = magnet_pos[0] + dx, magnet_pos[1] + dy

        if 0 <= new_x < n and 0 <= new_y < n and board[new_x][new_y] in [0, '*']:
            moves.append((new_x, new_y))
    return moves

def apply_move(state, magnet_type, new_pos):
    new_state = copy.deepcopy(state)
    if magnet_type == 'P':
        old_x, old_y = new_state['purple_pos']
        new_state['purple_pos'] = new_pos
        new_state['board'][old_x][old_y] = '*'
        new_state['board'][new_pos[0]][new_pos[1]] = 'P'
    elif magnet_type == 'R' and new_state['red_pos']:
        old_x, old_y = new_state['red_pos']
        new_state['red_pos'] = new_pos
        new_state['board'][old_x][old_y] = '*'
        new_state['board'][new_pos[0]][new_pos[1]] = 'R'
    new_state['steps'].append((magnet_type, new_pos))
    return new_state

def check_win(board):
    for row in board:
        for cell in row:
            if cell == 0:
                return False
    return True

def print_possible_moves(board, n):
    print("Possible moves:")
    for i in range(n):
        for j in range(n):
            if board[i][j] == 0 or board[i][j] == '*':
                print(f"({i}, {j})", end=" ")
    print() 
