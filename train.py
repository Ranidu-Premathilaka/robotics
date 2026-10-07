import random

from config import ALPHA, GAMMA, E, TEMP
from hardware import ev3, robot, get_light_state
from q_learning import (
    new_q_table, save_q_dict, get_reward, get_best_action,
    update_edge, light_state_to_position, resolve_action,
    semantic_actions, INNER_EDGE
)


def learn():
    Q_table = new_q_table()
    light_state = get_light_state()
    edge = INNER_EDGE
    iterations = 0

    while True:
        # Exploration vs. Exploitation
        if (E**(iterations/-TEMP) < 0.01):
            save_q_dict(Q_table)
            break

        position = light_state_to_position(light_state)

        if random.uniform(0, 1) < E**(iterations/-TEMP):
            sem_action = random.choice(semantic_actions)  # Explore by choosing a random action
            print("random", sem_action, edge)
        else:
            sem_action = get_best_action(Q_table, position)[0]  # Exploit by choosing the best action
            print("greedy", sem_action, edge)

        # Resolve to physical action and execute
        physical_action = resolve_action(sem_action, edge)
        physical_action(robot, light_state)  # Execute the action and wait for the robot to finish

        new_light_state = get_light_state()
        new_edge = update_edge(edge, light_state, physical_action, new_light_state)
        new_position = light_state_to_position(new_light_state)

        # Calculate max Q-value for the new state
        max_q_next = get_best_action(Q_table, new_position)[1]

        # Calculate reward for the new state
        reward_next = get_reward(new_position)
        if sem_action == 'BACKWARD':
            reward_next -= 15  # Backward is a costly recovery action, penalise to ensure it's learned as suboptimal

        # Update Q-table
        Q_table[(position, sem_action)] += ALPHA * (reward_next + GAMMA * max_q_next - Q_table[(position, sem_action)])

        # Print iteration number on the EV3 screen
        ev3.screen.clear()
        ev3.screen.draw_text(30, 40, iterations)
        ev3.screen.draw_text(20, 50, E**(iterations/-TEMP))

        light_state = new_light_state
        edge = new_edge
        iterations += 1

        save_q_dict(Q_table)
