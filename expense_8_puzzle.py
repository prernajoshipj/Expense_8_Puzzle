#Name: Prerna Joshi
#UTA ID: 1002127280
import sys
#import datetime
from puzzle_utils import read_puzzle
from search_methods import bfs, dfs, ucs, astar, greedy, dls, ids, generate_trace_filename

if __name__ == "__main__":
    start_file = sys.argv[1]  # Start state file
    goal_file = sys.argv[2]  # Goal state file
    search_method = sys.argv[3] if len(sys.argv) > 3 else 'astar'  # Search method
    dump_flag = sys.argv[4] == "true" or "True" or "TRUE" if len(sys.argv) > 4 else False
    #trace_file = f"trace-{datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}.txt" if dump_flag else None
    trace_file = generate_trace_filename() if dump_flag else None

    start = read_puzzle(start_file)
    goal = read_puzzle(goal_file)
    

    if search_method == 'bfs':
        result = bfs(start, goal, dump_flag, trace_file)
    elif search_method == 'dfs':
        depth_limit = int(sys.argv[5]) if len(sys.argv) > 5 else float('inf')
        result = dfs(start, goal, depth_limit, dump_flag, trace_file)
    elif search_method == 'ucs':
        result = ucs(start, goal, dump_flag, trace_file)
    elif search_method == 'astar':
        result = astar(start, goal, dump_flag, trace_file)
    elif search_method == 'greedy':
        result = greedy(start, goal, dump_flag, trace_file)
    elif search_method == 'dls':
        depth_limit = int(sys.argv[5]) if len(sys.argv) > 5 else float('inf')
        #depth_limit = int(input("Enter the depth limit for DLS: "))
        result = dls(start, goal, depth_limit, dump_flag, trace_file)
       
        #result = dls(start, goal, depth_limit, dump_flag, trace_file)
    elif search_method == 'ids':
        result = ids(start, goal, dump_flag, trace_file)

    if result:
        path, nodes_popped, nodes_expanded, nodes_generated, max_fringe_size, depth = result[:6]
        cost = result[6] if len(result) > 6 else "N/A"
        
        print(f"Nodes Popped: {nodes_popped}")
        print(f"Nodes Expanded: {nodes_expanded}")
        print(f"Nodes Generated: {nodes_generated}")
        print(f"Max Fringe Size: {max_fringe_size}")
        print(f"Solution Found at depth {depth} with cost of {cost if 'cost' in locals() else 'N/A'}.")
        print("Steps:")
        for tile, move in path:
            print(f"        Move {tile} {move}")
