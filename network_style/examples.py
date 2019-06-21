"""
Order - 
WINDOW_SIZE, WIND_X, WIND_Y, OFFSET_X, OFFSET_Y,
WAIT_LENGTH, BASIC_CREATE_NODE_PROBABILITY, BASIC_RANGE_COEFFICIENT, CREATE_NODE_PROBABILITY_LOSS_RATE, NEW_NODE_CREATE_NODE_PROBABILITY_COEFFICIENT, NEW_NODE_RANGE_COEFFICIENT, AGE_COEFFICIENT,
CIRCLE_SIZE_COEFFICIENT, LINE_WIDTH, REDNESS, GREENNESS, BLUENESS
"""

DATA = {"starburst" : (1000, 0, 0, 0, 0,
                       0, 1, 1, 1.1, 2, 3, 0,
                       10, 2, 1, 1, 1),
        "fuzzball" :  (1000, 0, 0, 0, 0,
                       0, 1, 0.1, 1.1, 1.2, 1, 100,
                       10, 2, 1, 1, 1),
       }

def set(name):

    return DATA[name]
