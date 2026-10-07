from pybricks.ev3devices import ColorSensor, InfraredSensor, Motor
from pybricks.hubs import EV3Brick
from pybricks.parameters import Port
from pybricks.robotics import DriveBase

from config import WHITE_VALUE, BLACK_VALUE

# Initialize hardware components
ev3 = EV3Brick()
left_motor = Motor(Port.A)
right_motor = Motor(Port.D)
light_sensor = ColorSensor(Port.S2)
ir_sensor = InfraredSensor(Port.S4)
robot = DriveBase(left_motor, right_motor, wheel_diameter=40, axle_track=50)


def get_light_state():
    light_sensor_reading = light_sensor.reflection()
    if(light_sensor_reading >= WHITE_VALUE):
        return 'WHITE'
    if(light_sensor_reading <= BLACK_VALUE):
        return 'BLACK'
    return 'MIDDLE'
