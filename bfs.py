from collections import deque
import copy

def bfs_solve(board, purple_magnet_pos, n, red_magnet_pos=None):
    start_state = {
        'board': copy.deepcopy(board),
        'purple_pos': purple_magnet_pos,
        'red_pos': red_magnet_pos,
        'steps': [],
        'turn': 'R' if red_magnet_pos else 'P'
    }

    queue = deque([start_state])
    visited = set()
    visited.add((tuple(map(tuple, start_state['board'])), start_state['purple_pos'], start_state['red_pos'], start_state['turn']))

    while queue:
        current_state = queue.popleft()

        if check_win(current_state['board']):
            last_zero_position = current_state['purple_pos'] if current_state['purple_pos'] else current_state['red_pos']
            current_state['steps'].append(('Place Magnet', last_zero_position))
            print("Solution found:", current_state['steps'])
            return current_state['steps']

        if current_state['turn'] == 'R' and current_state['red_pos']:
            red_moves = possible_moves(current_state['board'], current_state['red_pos'], n)
            for move in red_moves:
                new_state = apply_move(current_state, 'R', move)
                new_state['turn'] = 'P' if current_state['purple_pos'] else 'R'
                board_hash = (tuple(map(tuple, new_state['board'])), new_state['purple_pos'], new_state['red_pos'], new_state['turn'])
                if board_hash not in visited:
                    queue.append(new_state)
                    visited.add(board_hash)

        if current_state['turn'] == 'P' and current_state['purple_pos']:
            purple_moves = possible_moves(current_state['board'], current_state['purple_pos'], n)
            for move in purple_moves:
                new_state = apply_move(current_state, 'P', move)
                new_state['turn'] = 'R' if current_state['red_pos'] else 'P'
                board_hash = (tuple(map(tuple, new_state['board'])), new_state['purple_pos'], new_state['red_pos'], new_state['turn'])
                if board_hash not in visited:
                    queue.append(new_state)
                    visited.add(board_hash)

        if current_state['turn'] == 'R' and not current_state['purple_pos']:
            red_moves = possible_moves(current_state['board'], current_state['red_pos'], n)
            for move in red_moves:
                new_state = apply_move(current_state, 'R', move)
                new_state['turn'] = 'R'
                board_hash = (tuple(map(tuple, new_state['board'])), new_state['purple_pos'], new_state['red_pos'], new_state['turn'])
                if board_hash not in visited:
                    queue.append(new_state)
                    visited.add(board_hash)

        elif current_state['turn'] == 'P' and not current_state['red_pos']:
            purple_moves = possible_moves(current_state['board'], current_state['purple_pos'], n)
            for move in purple_moves:
                new_state = apply_move(current_state, 'P', move)
                new_state['turn'] = 'P'  
                board_hash = (tuple(map(tuple, new_state['board'])), new_state['purple_pos'], new_state['red_pos'], new_state['turn'])
                if board_hash not in visited:
                    queue.append(new_state)
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
        if new_state['board'][new_pos[0]][new_pos[1]] == 0:
            new_state['board'][new_pos[0]][new_pos[1]] = 'P'
        new_state['board'][old_x][old_y] = '*'
    elif magnet_type == 'R' and new_state['red_pos']:
        old_x, old_y = new_state['red_pos']
        new_state['red_pos'] = new_pos
        if new_state['board'][new_pos[0]][new_pos[1]] == 0:
            new_state['board'][new_pos[0]][new_pos[1]] = 'R'
        new_state['board'][old_x][old_y] = '*'
    new_state['steps'].append((magnet_type, new_pos))
    return new_state

def check_win(board):
    for row in board:
        for cell in row:
            if cell == 0:
                return False 
    return True
