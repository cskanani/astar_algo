import queue, random

#function for moving tile
def move_up(parent, hueristics_type):
    state = parent.state.copy()
    zero_index = state.index(0)
    if(zero_index in [0, 1, 2]):
        return None
    else:
        state[zero_index], state[zero_index-3] = state[zero_index-3], state[zero_index]
        return Node(parent, state, 'up', hueristics_type)
        
def move_down(parent, hueristics_type):
    state = parent.state.copy()
    zero_index = state.index(0)
    if(zero_index in [6, 7, 8]):
        return None
    else:
        state[zero_index], state[zero_index+3] = state[zero_index+3], state[zero_index]
        return Node(parent, state, 'down', hueristics_type)
        
def move_left(parent, hueristics_type):
    state = parent.state.copy()
    zero_index = state.index(0)
    if(zero_index in [0, 3, 6]):
        return None
    else:
        state[zero_index], state[zero_index-1] = state[zero_index-1], state[zero_index]
        return Node(parent, state, 'left', hueristics_type)
        
def move_right(parent, hueristics_type):
    state = parent.state.copy()
    zero_index = state.index(0)
    if(zero_index in [2, 5, 8]):
        return None
    else:
        state[zero_index], state[zero_index+1] = state[zero_index+1], state[zero_index]
        return Node(parent, state, 'right', hueristics_type)

#function for generating child-nodes
def generate_childs(parent, open_list, hueristics_type):
    up_child = move_up(parent, hueristics_type)
    down_child = move_down(parent, hueristics_type)
    left_child = move_left(parent, hueristics_type)
    right_child = move_right(parent, hueristics_type)
    new_nodes_count = 0
    if (up_child != None): open_list.put(up_child); new_nodes_count += 1
    if (down_child != None): open_list.put(down_child); new_nodes_count += 1
    if (left_child != None): open_list.put(left_child); new_nodes_count += 1
    if (right_child != None): open_list.put(right_child); new_nodes_count += 1
    return new_nodes_count
    
#function for calculating different type of hueristics
def get_huristics(state, hueristics_type):
    h = 0
    if(hueristics_type == 'manhattan'):
        for i in range(1, 9):
            i_position = state.index(i)
            x = i_position // 3
            y = i_position % 3
            i_goal_position = goal_state.index(i)
            x_goal = i_goal_position // 3
            y_goal = i_goal_position % 3
            h += abs(x_goal - x) + abs(y_goal - y)
    elif(hueristics_type == 'displaced_tiles'):
        for i in range(1, 9):
            if(state[i-1] != i): 
                h += 1
    elif(hueristics_type == 'over_estimated'):
        return random.randint(1000, 2000)
    else:
        return 0
    return h

#class for creating node objects
class Node:
    def __init__(self, parent, state, move, hueristics_type):
        self.parent = parent
        self.move = move
        self.g = parent.g+1 if (parent != None) else 0
        self.h = get_huristics(state, hueristics_type)
        self.f = self.g+self.h
        self.state = state
        
    def __lt__(self, other):
        return self.f < other.f

#function to run a_star algo
def run_as(start_state, hueristics_type):
    visited_nodes_count = 0
    explored_nodes_count = 0
    path = []
    closed_list = []
    #openlist implimented with PriorityQueue to store non-visited nodes based on f value
    open_list = queue.PriorityQueue()
    
    start_node = Node(None, start_state, '', hueristics_type)
    open_list.put(start_node)

    while(not open_list.empty()):
        visited_nodes_count += 1
        parent = open_list.get()
        if(parent.state == goal_state):
            while(parent.parent != None):
                path.insert(0, parent.move)
                parent = parent.parent
            break
        if parent in closed_list:
            continue
        explored_nodes_count += generate_childs(parent, open_list, hueristics_type)
        closed_list.append(parent.state)
    return explored_nodes_count, visited_nodes_count, path

#function for printing results data
def print_data(hueristics_type, explored_nodes_count, visited_nodes_count, path):
    print('\n')
    if(hueristics_type == 'manhattan'):
        print('Data with Manhatan hueristics : ')
    elif(hueristics_type == 'displaced_tiles'):
        print('Data with displaced tiles hueristics : ')
    elif(hueristics_type == 'over_estimated'):
        print('Data with over-estimated hueristics : ')
    else:
        print('Data with zero hueristics : ')
    print('Number of nodes explored :', explored_nodes_count)
    print('Number of nodes visited :', visited_nodes_count)
    print('Length of path :', len(path))
    print('Path to goal_state :', path)


#taking initial state from user
start_state = [int(x) for x in input('state: ').split(' ')]
goal_state = [1, 2, 3, 4, 5, 6, 7, 8, 0]

#hueristics type manhattan, displaced_tiles, any other for Zero hueristics
explored_nodes_count, visited_nodes_count, path = run_as(start_state, 'manhattan')
print_data('manhattan', explored_nodes_count, visited_nodes_count, path)
explored_nodes_count, visited_nodes_count, path = run_as(start_state, 'displaced_tiles')
print_data('displaced_tiles', explored_nodes_count, visited_nodes_count, path)
explored_nodes_count, visited_nodes_count, path = run_as(start_state, 'z')
print_data('z', explored_nodes_count, visited_nodes_count, path)
explored_nodes_count, visited_nodes_count, path = run_as(start_state, 'over_estimated')
print_data('over_estimated', explored_nodes_count, visited_nodes_count, path)