from config import OBSTACLE_DISTANCE
from hardware import ev3, robot, light_sensor, ir_sensor, get_light_state
from actions import turn_right, backward
from q_learning import load_q_dict, get_best_action, update_mode


def obstacle_avoidance(mode):
    backward(robot, light_sensor, mode)

def line_following(Q_table, mode, light_state):
    action = get_best_action(Q_table, mode,light_state)[0]  # Choose the action with the highest Q-value
    print("line following",mode, action.__name__, light_state)

    action(robot, light_state)  # Execute the action and wait for the robot to finish
    new_light_state = get_light_state() # Observe new state

    mode = update_mode(mode, light_state, action, new_light_state)

    return mode, new_light_state

def run():
    light_state = get_light_state()
    mode = True

    # Load Q-table
    Q_table = load_q_dict()
    print(Q_table)

    # Find mode
    action = turn_right
    action(robot, light_state)  # Execute the action and wait for the robot to finish
    new_light_state = get_light_state()
    mode = update_mode(mode, light_state, action, new_light_state)
    light_state = new_light_state

    # Run
    while True:
        if (ir_sensor.distance() < OBSTACLE_DISTANCE):
            print("obstacle")
            robot.stop()
            # ev3.speaker.say("Avoiding Obstacle")
            obstacle_avoidance(mode)
            mode = not mode
        else:
            mode, light_state = line_following(Q_table, mode, light_state)
