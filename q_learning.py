import pickle

from config import Q_TABLE_FILE
from actions import actions, actions_by_name

modes = [True,False]
light_states = ['WHITE','MIDDLE','BLACK']

# Transitions that reveal which side of the line the robot is on
m_y = [('MIDDLE','turn_right','BLACK'),('BLACK','turn_left','MIDDLE'),('MIDDLE','turn_left','WHITE'),('WHITE','turn_right','MIDDLE')]
m_x = [('MIDDLE','turn_right','WHITE'),('WHITE','turn_left','MIDDLE'),('MIDDLE','turn_left','BLACK'),('BLACK','turn_right','MIDDLE')]


def new_q_table():
    Q_table = {}
    for mode in modes:
        for act in actions:
            for light in light_states:
                Q_table[(mode,light, act)] = 0
    return Q_table

def save_q_dict(q_dict):
    temp = {}
    for key,value in q_dict.items():
        temp[(key[0],key[1],key[2].__name__)] = value
    with open(Q_TABLE_FILE, 'wb') as file:
        pickle.dump(temp, file)

def load_q_dict():
    # Reading the dictionary from the file
    with open(Q_TABLE_FILE, 'rb') as file:
        temp = pickle.load(file)
    q_dict = {}
    for key,value in temp.items():
        q_dict[(key[0],key[1],actions_by_name[key[2]])] = value
    return q_dict

# Get reward for a given state
def get_reward(light_state):
    return -10 if light_state in ['BLACK','WHITE'] else 10

# Get best action for a given state
def get_best_action(Q_table, mode, light_state):
    max_q = -float("inf")
    best_action = None
    for act in actions:
        q = Q_table[(mode, light_state, act)]
        if q > max_q:
            best_action = act
            max_q = q
    return best_action, max_q

# Work out the new mode from the transition the last action caused
def update_mode(mode, light_state, action, new_light_state):
    if((light_state,action.__name__,new_light_state) in m_x):
        return True
    if((light_state,action.__name__,new_light_state) in m_y):
        return False
    return mode
