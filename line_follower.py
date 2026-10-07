from config import OBSTACLE_DISTANCE
from hardware import ev3, robot, light_sensor, ir_sensor, get_light_state
from actions import turn_right, backward
from q_learning import (
    load_q_dict, get_best_action, update_edge, light_state_to_position,
    resolve_action, INNER_EDGE, OUTER_EDGE
)


def obstacle_avoidance(edge):
    backward(robot, light_sensor, edge)

def line_following(Q_table, edge, light_state):
    position = light_state_to_position(light_state)
    sem_action = get_best_action(Q_table, position)[0]  # Choose the best semantic action

    physical_action = resolve_action(sem_action, edge)
    print("line following", edge, sem_action, position)

    physical_action(robot, light_state)  # Execute the action and wait for the robot to finish
    new_light_state = get_light_state() # Observe new state

    edge = update_edge(edge, light_state, physical_action, new_light_state)

    return edge, new_light_state

def run():
    light_state = get_light_state()
    edge = INNER_EDGE

    # Load Q-table
    Q_table = load_q_dict()
    print(Q_table)

    # Find edge
    action = turn_right
    action(robot, light_state)  # Execute the action and wait for the robot to finish
    new_light_state = get_light_state()
    edge = update_edge(edge, light_state, action, new_light_state)
    light_state = new_light_state

    # Run
    while True:
        if (ir_sensor.distance() < OBSTACLE_DISTANCE):
            print("obstacle")
            robot.stop()
            # ev3.speaker.say("Avoiding Obstacle")
            obstacle_avoidance(edge)
            edge = OUTER_EDGE if edge == INNER_EDGE else INNER_EDGE
        else:
            edge, light_state = line_following(Q_table, edge, light_state)
