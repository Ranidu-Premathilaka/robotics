from pybricks.tools import wait

from config import TURN_ANGLE, WHITE_VALUE, BLACK_VALUE
from hardware import light_sensor, get_light_state


# Robot actions
def forward(robot, previous_light_state):
    speed = min(max(100,(robot.state()[1]))+5,180)
    robot.drive(speed,0)
    wait(250)

def turn_left(robot, previous_light_state):
    while previous_light_state == get_light_state() :
        robot.drive(10,-110)
        wait(100)

def turn_right(robot,previous_light_state):
    while previous_light_state == get_light_state():
        robot.drive(10,110)
        wait(100)

def backward(robot, previous_light_state,mode):
    for i in range(5):
        robot.turn((-1 if mode else 1) *TURN_ANGLE * 10)
    #     ev3.speaker.beep()
    # ev3.speaker.beep()

    while not (
        light_sensor.reflection() > BLACK_VALUE
        and light_sensor.reflection() < WHITE_VALUE
    ):
        robot.turn((-1 if mode else 1) * TURN_ANGLE*10)
        # ev3.speaker.beep()


# Actions the agent can choose from (order matters for tie-breaking)
actions = [forward, turn_left, turn_right]

# Lookup used when loading a saved Q-table, which stores actions by name
actions_by_name = {act.__name__: act for act in actions}
