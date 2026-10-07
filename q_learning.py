import pickle

from config import Q_TABLE_FILE
from actions import forward, turn_left, turn_right

# Positional states relative to the line
states = ['INNER', 'EDGE', 'OUTER']

# Semantic actions the agent can choose from
semantic_actions = ['GOTO_INNER', 'STAY', 'GOTO_OUTER']

# Which edge of the line the robot is following
INNER_EDGE = 'INNER_EDGE'
OUTER_EDGE = 'OUTER_EDGE'

# Transitions that identify which edge the robot is following
_inner_edge_transitions = [
    ('MIDDLE', 'turn_right', 'WHITE'), ('WHITE', 'turn_left', 'MIDDLE'),
    ('MIDDLE', 'turn_left', 'BLACK'), ('BLACK', 'turn_right', 'MIDDLE')
]
_outer_edge_transitions = [
    ('MIDDLE', 'turn_right', 'BLACK'), ('BLACK', 'turn_left', 'MIDDLE'),
    ('MIDDLE', 'turn_left', 'WHITE'), ('WHITE', 'turn_right', 'MIDDLE')
]


def new_q_table():
    Q_table = {}
    for state in states:
        for action in semantic_actions:
            Q_table[(state, action)] = 0
    return Q_table


def save_q_dict(q_dict):
    with open(Q_TABLE_FILE, 'wb') as file:
        pickle.dump(q_dict, file)


def load_q_dict():
    with open(Q_TABLE_FILE, 'rb') as file:
        return pickle.load(file)


def light_state_to_position(light_state):
    """Map raw sensor state to positional state relative to the line."""
    if light_state == 'BLACK':
        return 'INNER'
    elif light_state == 'WHITE':
        return 'OUTER'
    return 'EDGE'


def resolve_action(semantic_action, edge):
    """Convert a semantic action to a physical action based on which edge we're following.

    INNER_EDGE: line is to the left  -> turn_left = GOTO_INNER, turn_right = GOTO_OUTER
    OUTER_EDGE: line is to the right -> turn_right = GOTO_INNER, turn_left = GOTO_OUTER
    """
    if semantic_action == 'STAY':
        return forward
    if edge == INNER_EDGE:
        return turn_left if semantic_action == 'GOTO_INNER' else turn_right
    else:  # OUTER_EDGE
        return turn_right if semantic_action == 'GOTO_INNER' else turn_left


# Get reward for a given positional state
def get_reward(position):
    return -10 if position in ['INNER', 'OUTER'] else 10


# Get best semantic action for a given positional state
def get_best_action(Q_table, position):
    max_q = -float("inf")
    best_action = None
    for act in semantic_actions:
        q = Q_table[(position, act)]
        if q > max_q:
            best_action = act
            max_q = q
    return best_action, max_q


# Determine which edge the robot is following from the observed transition
def update_edge(edge, light_state, action, new_light_state):
    transition = (light_state, action.__name__, new_light_state)
    if transition in _inner_edge_transitions:
        return INNER_EDGE
    if transition in _outer_edge_transitions:
        return OUTER_EDGE
    return edge
