
import heapq
from collections import deque
from datetime import datetime
from puzzle_utils import states_equal, get_possible_moves, move_tile, dump_trace, manhattan_distance

def log_trace_data(trace_data, trace_file):
    with open(trace_file, 'a') as f:
        for line in trace_data:
            f.write(line + '\n')

def bfs(start, goal, dump_flag=False, trace_file=None, method="bfs"):
    frontier = deque([(start, [], 0)])  # Queue for BFS: (state, path, depth)
    explored = set()
    trace_data = []
    nodes_popped = nodes_expanded = nodes_generated = max_fringe_size = 0

    if dump_flag and trace_file:
        trace_data.append(f"Command-Line Arguments: ['start.txt', 'goal.txt', '{method}', '{str(dump_flag)}']")
        trace_data.append(f"Method Selected: {method}")
        #trace_data.append(f"Running bfs")

    while frontier:
        max_fringe_size = max(max_fringe_size, len(frontier))
        current_state, path, depth = frontier.popleft()
        nodes_popped += 1

        if dump_flag and trace_file:
            trace_data.append(f"Generating successors to < state = {current_state}, g(n) = {depth}, d = {depth} >:")
            trace_data.append(f"Closed:{[list(state) for state in explored]}")
            trace_data.append(f"Fringe: {['< state =' + str(state) + ', >' for state, _, _ in frontier]}")

        if states_equal(current_state, goal):
            if dump_flag and trace_file:
                trace_data.append(f"Goal Found: < state = {current_state}, action = {path[-1][0] if path else None} >")
                trace_data.append(f"Nodes Popped: {nodes_popped}")
                trace_data.append(f"Nodes Expanded: {nodes_expanded}")
                trace_data.append(f"Nodes Generated: {nodes_generated}")
                trace_data.append(f"Max Fringe Size: {max_fringe_size}")
                dump_trace(trace_data, trace_file)
            return (path, nodes_popped, nodes_expanded, nodes_generated, max_fringe_size, len(path))

        explored.add(tuple(map(tuple, current_state)))
        nodes_expanded += 1

        successors = []
        for move in get_possible_moves(current_state):
            new_state, moved_tile = move_tile(current_state, move)

            if tuple(map(tuple, new_state)) not in explored and new_state not in [state for state, _, _ in frontier]:
                frontier.append((new_state, path + [(moved_tile, move)], depth + 1))
                nodes_generated += 1
                successors.append((new_state, moved_tile, move))

        if dump_flag and trace_file:
            trace_data.append(f"{len(successors)} successors generated")
            for successor in successors:
                trace_data.append(f"< state = {successor[0]}, action = {successor[1]}, move = {successor[2]}, g(n) = {depth+1}, d = {depth+1}, Parent = Pointer to < state = {current_state}, ... > >")

    if dump_flag and trace_file:
        trace_data.append("No solution found.")
        dump_trace(trace_data, trace_file)

    #return None, nodes_popped, nodes_expanded, nodes_generated, max_fringe_size

def dump_trace(trace_data, trace_file):
    # Function to dump trace to the file with timestamp
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    with open(f"{trace_file}-{timestamp}.txt", "w") as f:
        f.write("\n".join(trace_data))

def dfs(start, goal, depth_limit=float('inf'), dump_flag=False, trace_file=None):
    frontier = [(start, [], 0)]  # Stack for DFS: (state, path, depth)
    explored = set()
    trace_data = []
    nodes_popped = nodes_expanded = nodes_generated = max_fringe_size = 0

    while frontier:
        max_fringe_size = max(max_fringe_size, len(frontier))
        current_state, path, depth = frontier.pop()  # LIFO Stack for DFS
        nodes_popped += 1

        if dump_flag and trace_file:
            trace_data.append(f"Frontier Size: {len(frontier)}, Closed set size: {len(explored)}")
            trace_data.append(f"Nodes Expanded: {nodes_expanded}, Nodes Generated: {nodes_generated}")

        if states_equal(current_state, goal):
            if dump_flag and trace_file:
                dump_trace(trace_data, trace_file)
            return (path, nodes_popped, nodes_expanded, nodes_generated, max_fringe_size, len(path))

        explored.add(tuple(map(tuple, current_state)))
        nodes_expanded += 1

        if depth < depth_limit:
            for move in get_possible_moves(current_state):
                new_state, moved_tile = move_tile(current_state, move)
                if tuple(map(tuple, new_state)) not in explored:
                    frontier.append((new_state, path + [(moved_tile, move)], depth + 1))
                    nodes_generated += 1

    if dump_flag and trace_file:
        dump_trace(trace_data, trace_file)
    return None


def dls(start, goal, depth_limit, dump_flag, trace_file):
    return dfs(start, goal, depth_limit, dump_flag, trace_file)

def ids(start, goal, dump_flag=False, trace_file=None):
    depth = 0
    result = None
    trace_data = []

    # Record initial command-line arguments and method selected
    if dump_flag and trace_file:
        trace_data.append(f"Command-Line Arguments: ['start.txt', 'goal.txt', 'ids', '{str(dump_flag)}']")
        trace_data.append(f"Method Selected: ids")

    while result is None:
        # Capture trace information for the current depth
        if dump_flag and trace_file:
            trace_data.append(f"Running DLS with depth limit: {depth}")

        result = dls(start, goal, depth, dump_flag, trace_file)#, trace_data)
        depth += 1

    # Dump the collected trace data
    if dump_flag and trace_file:
        dump_trace(trace_data, trace_file)

    return result

def ucs(start, goal, dump_flag=False, trace_file=None):
    frontier = [(0, start, [])]  # Priority queue for UCS: (cost, state, path)
    explored = set()
    trace_data = []
    nodes_popped = nodes_expanded = nodes_generated = max_fringe_size = 0
    method = "ucs"

    if dump_flag and trace_file:
        trace_data.append(f"Command-Line Arguments: ['start.txt', 'goal.txt', '{method}', '{str(dump_flag)}']")
        trace_data.append(f"Method Selected: {method}")
    
    while frontier:
        max_fringe_size = max(max_fringe_size, len(frontier))
        path_cost, current_state, path = heapq.heappop(frontier)
        nodes_popped += 1

        if dump_flag and trace_file:
            trace_data.append(f"Generating successors to < state = {current_state}, g(n) = {path_cost} >:")
            trace_data.append(f"Closed: {list(explored)}")
            trace_data.append(f"Fringe: {list(frontier)}")
            trace_data.append(f"Nodes Expanded: {nodes_expanded}, Nodes Generated: {nodes_generated}")

        if states_equal(current_state, goal):
            if dump_flag and trace_file:
                dump_trace(trace_data, trace_file)
            return (path, nodes_popped, nodes_expanded, nodes_generated, max_fringe_size, len(path), path_cost)

        explored.add(tuple(map(tuple, current_state)))
        nodes_expanded += 1

        for move in get_possible_moves(current_state):
            new_state, moved_tile = move_tile(current_state, move)
            move_cost = moved_tile
            if tuple(map(tuple, new_state)) not in explored:
                total_cost = path_cost + move_cost
                heapq.heappush(frontier, (total_cost, new_state, path + [(moved_tile, move)]))
                nodes_generated += 1

    if dump_flag and trace_file:
        dump_trace(trace_data, trace_file)
    return None

# Greedy algorithm with path cost calculation
def greedy(start, goal, dump_flag=False, trace_file=None):
    frontier = [(manhattan_distance(start, goal), start, [], 0)]  # Priority queue for Greedy Search
    explored = set()
    trace_data = []
    nodes_popped = nodes_expanded = nodes_generated = max_fringe_size = 0

    while frontier:
        max_fringe_size = max(max_fringe_size, len(frontier))
        heuristic, current_state, path, path_cost = heapq.heappop(frontier)
        nodes_popped += 1

        if dump_flag and trace_file:
            trace_data.append(f"Frontier: {frontier}, Closed set: {explored}")
            trace_data.append(f"Nodes Expanded: {nodes_expanded}, Nodes Generated: {nodes_generated}")

        if states_equal(current_state, goal):
            if dump_flag and trace_file:
                dump_trace(trace_data, trace_file)
            return (path, nodes_popped, nodes_expanded, nodes_generated, max_fringe_size, len(path), path_cost)

        explored.add(tuple(map(tuple, current_state)))
        nodes_expanded += 1

        for move in get_possible_moves(current_state):
            new_state, moved_tile = move_tile(current_state, move)
            if tuple(map(tuple, new_state)) not in explored:
                new_path_cost = path_cost + moved_tile  # Update path cost
                heapq.heappush(frontier, (manhattan_distance(new_state, goal), new_state, path + [(moved_tile, move)], new_path_cost))
                nodes_generated += 1

    if dump_flag and trace_file:
        dump_trace(trace_data, trace_file)
    return None
"""
def astar(start, goal, dump_flag=False, trace_file=None):
    frontier = [(manhattan_distance(start, goal), 0, start, [])]  # Priority queue for A*: (f = g + h, g, state, path)
    explored = set()
    trace_data = []
    nodes_popped = nodes_expanded = nodes_generated = max_fringe_size = 0
    method = "a*"

    if dump_flag and trace_file:
        trace_data.append(f"Command-Line Arguments: ['start.txt', 'goal.txt', '{method}', '{str(dump_flag)}']")
        trace_data.append(f"Method Selected: {method}")
    
    while frontier:
        max_fringe_size = max(max_fringe_size, len(frontier))
        f_value, g_value, current_state, path = heapq.heappop(frontier)
        nodes_popped += 1

        if dump_flag and trace_file:
            trace_data.append(f"Generating successors to < state = {current_state}, g(n) = {g_value}, d = {len(path)}, f(n) = {f_value} >:")
            trace_data.append(f"Closed: {list(explored)}")
            trace_data.append(f"Fringe: {list(frontier)}")
            trace_data.append(f"Nodes Expanded: {nodes_expanded}, Nodes Generated: {nodes_generated}")

        if states_equal(current_state, goal):
            if dump_flag and trace_file:
                dump_trace(trace_data, trace_file)
            return (path, nodes_popped, nodes_expanded, nodes_generated, max_fringe_size, len(path), g_value)

        explored.add(tuple(map(tuple, current_state)))
        nodes_expanded += 1

        for move in get_possible_moves(current_state):
            new_state, moved_tile = move_tile(current_state, move)
            move_cost = moved_tile  # Cost of moving the tile
            if tuple(map(tuple, new_state)) not in explored:
                g_new_value = g_value + move_cost
                f_new_value = g_new_value + manhattan_distance(new_state, goal)
                heapq.heappush(frontier, (f_new_value, g_new_value, new_state, path + [(moved_tile, move)]))
                nodes_generated += 1

    if dump_flag and trace_file:
        dump_trace(trace_data, trace_file)
    return None

"""

# A* Search Algorithm Implementation
def astar(start, goal, dump_flag=False, trace_file=None):
    frontier = [(manhattan_distance(start, goal), 0, start, [])]  # (f = g + h, g, state, path)
    explored = set()  # Set to store explored states
    trace_data = []
    nodes_popped = nodes_expanded = nodes_generated = max_fringe_size = 0
    method = "a*"

    if dump_flag and trace_file:
        trace_data.append(f"Command-Line Arguments: ['start.txt', 'goal.txt', '{method}', '{str(dump_flag)}']")
        trace_data.append(f"Method Selected: {method}")
    
    while frontier:
        max_fringe_size = max(max_fringe_size, len(frontier))
        f_value, g_value, current_state, path = heapq.heappop(frontier)
        nodes_popped += 1

        if dump_flag and trace_file:
            trace_data.append(f"Generating successors to < state = {current_state}, g(n) = {g_value}, d = {len(path)}, f(n) = {f_value} >:")
            trace_data.append(f"Closed: {list(explored)}")
            trace_data.append(f"Fringe: {list(frontier)}")
            trace_data.append(f"Nodes Expanded: {nodes_expanded}, Nodes Generated: {nodes_generated}")

        if states_equal(current_state, goal):  # Goal state found
            if dump_flag and trace_file:
                dump_trace(trace_data, trace_file)
            return (path, nodes_popped, nodes_expanded, nodes_generated, max_fringe_size, len(path), g_value)

        explored.add(tuple(map(tuple, current_state)))  # Add state to explored
        nodes_expanded += 1

        for move in get_possible_moves(current_state):
            new_state, moved_tile = move_tile(current_state, move)
            move_cost = moved_tile  # Cost of moving the tile (tile number itself)
            if tuple(map(tuple, new_state)) not in explored:
                g_new_value = g_value + move_cost
                f_new_value = g_new_value + manhattan_distance(new_state, goal)
                heapq.heappush(frontier, (f_new_value, g_new_value, new_state, path + [(moved_tile, move)]))
                nodes_generated += 1

    if dump_flag and trace_file:
        dump_trace(trace_data, trace_file)

    return None  # If no solution is found
# Function to generate trace file name
def generate_trace_filename():
    timestamp = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    return f"trace-{timestamp}.txt"
