# Run mode: True to train a new Q-table before running, False to only run
TRAINING = False

# Light sensor thresholds (reflection %)
WHITE_VALUE = 25
BLACK_VALUE = 8

# Movement
TURN_ANGLE = 2
DRIVE_SPEED = 20

# Q-learning parameters
ALPHA = 0.1  # Learning rate
EPSILON = 1  # Exploration rate
GAMMA = 0.9  # Discount factor
E = 2.7321
TEMP = 1000  # Exploration decay rate

# Obstacle detection (IR sensor proximity)
OBSTACLE_DISTANCE = 15

# Q-table file
Q_TABLE_FILE = 'q_table.pkl'
