

def read_puzzle(file):
    puzzle = []
    with open(file, 'r') as f:
        for line in f:
            if "END OF FILE" in line:
                break
            puzzle.append(list(map(int, line.split())))
    return puzzle

# Function to compare if two states are equal
def states_equal(state1, state2):
    return state1 == state2

# Function to calculate Manhattan distance between current state and goal state
def manhattan_distance(state, goal):
    dist = 0
    for r in range(3):
        for c in range(3):
            tile = state[r][c]
            if tile != 0:  # Don't calculate distance for the blank tile
                goal_r, goal_c = next((gr, gc) for gr in range(3) for gc in range(3) if goal[gr][gc] == tile)
                dist += abs(r - goal_r) + abs(c - goal_c)
    return dist

# Get the possible moves for the blank tile
def get_possible_moves(state):
    x, y = find_blank(state)
    moves = []
    if x > 0: moves.append('Down')   # Can move blank tile down
    if x < 2: moves.append('Up')     # Can move blank tile up
    if y > 0: moves.append('Right')  # Can move blank tile right
    if y < 2: moves.append('Left')   # Can move blank tile left
    return moves

# Function to find the blank tile (0) in the state
def find_blank(state):
    for i, row in enumerate(state):
        if 0 in row:
            return i, row.index(0)
        
# Function to move the tile in a given direction and return the new state
def move_tile(state, direction):
    new_state = [row[:] for row in state]  # Deep copy of the state
    x, y = find_blank(new_state)

    moved_tile = None

    if direction == 'Down' and x > 0:
        new_state[x][y], new_state[x-1][y] = new_state[x-1][y], new_state[x][y]
        moved_tile = new_state[x][y]
    elif direction == 'Up' and x < 2:
        new_state[x][y], new_state[x+1][y] = new_state[x+1][y], new_state[x][y]
        moved_tile = new_state[x][y]
    elif direction == 'Right' and y > 0:
        new_state[x][y], new_state[x][y-1] = new_state[x][y-1], new_state[x][y]
        moved_tile = new_state[x][y]
    elif direction == 'Left' and y < 2:
        new_state[x][y], new_state[x][y+1] = new_state[x][y+1], new_state[x][y]
        moved_tile = new_state[x][y]
    
    return new_state, moved_tile

# Function to dump the search trace data to a file
def dump_trace(trace_data, trace_file):
    with open(trace_file, 'w') as f:
        for data in trace_data:
            f.write(f"{data}\n")
