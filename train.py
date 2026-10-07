import random

from config import ALPHA, GAMMA, E, TEMP
from hardware import ev3, robot, get_light_state
from actions import actions
from q_learning import new_q_table, save_q_dict, get_reward, get_best_action, update_mode


def learn():
    Q_table = new_q_table()
    light_state = get_light_state()
    mode = True
    iterations = 0
    action = None

    while True:
        # Exploration vs. Exploitation
        if (E**(iterations/-TEMP) < 0.01):
            save_q_dict(Q_table)
            break

        if random.uniform(0, 1) <  E**(iterations/-TEMP):
            action = random.choice(actions)  # Explore by choosing a random action
            print("random", action.__name__, mode)
        else:
            action = get_best_action(Q_table, mode,light_state)[0]  # Exploit by choosing the action with the highest Q-value
            print("greedy", action.__name__ , mode)

        action(robot, light_state)  # Execute the action and wait for the robot to finish

        new_light_state = get_light_state()
        new_mode = update_mode(mode, light_state, action, new_light_state)

        # Calculate max Q-value for the new state
        max_q_next = get_best_action(Q_table, new_mode, new_light_state)[1]

        # Calculate reward for the new state
        reward_next = get_reward(new_light_state)

        # Update Q-table
        Q_table[(mode, light_state, action)] += ALPHA * (reward_next + GAMMA * max_q_next - Q_table[( mode, light_state, action)])

        # Print iteration number on the EV3 screen
        ev3.screen.clear()
        ev3.screen.draw_text(30,40,iterations)
        ev3.screen.draw_text(20,50,E**(iterations/-TEMP))

        light_state = new_light_state
        mode = new_mode
        iterations += 1

        save_q_dict(Q_table)
