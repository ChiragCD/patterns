"""
Create star-topology like patterns, with a considerable random element.

Uses pygame for display,
     random to generate the pattern
     time as an option for slowing the program

The only external module here is pygame, this can be installed with ## arthur_dent@hitchhiker's_guide:~$ pip3 install pygame
The version used here is 1.9.4

The program starts with a single parent node, who, with each iteration, has an expand_probability of creating and connecting to a node, within expand_range,
the child node has a fraction (or multiple) of the parent's expand_ attributes, random colour. This node is kept in the parent's children list.
With each new child, the parent's expand_probability decreases.

As a result of this setup, each node is a parent of its own network, represented in its colour.
Each new "generation" is less likely to reproduce, to account for the increasing size of the generation.
Node's circle radius is proportional to its expand_probability.

Go ahead and experiment with options, and with the program itself. Feel free to send me screenshots, and PR modified versions into this folder. Suggestions
are welcome, please contribute toward solving the issues.
"""

import pygame, random, time

try:
    import examples
except:
    pass
"""
Initiating options
"""

WINDOW_SIZE = 1000                                  ## > 0 - Set as per your comfort
WIND_X = 0                                          ## Gives a "windy" effect, by "blowing" new nodes this many pixels East/right.
WIND_Y = 0                                          ## Similar, gives a Southward wind of this much intensity. Useful to draw weeping willows/tilting ghosts/chandeliers, etc.
OFFSET_X = 0                                        ## Place the original parent this many pixels right of centre.
OFFSET_Y = 0                                        ## Place the original parent this many pixels below centre.

"""
Runtime options
"""

WAIT_LENGTH = 0                                     ## > 0 - Wait this many seconds between iterations, useful if lag encountered with value 0, or for watching slowly.

BASIC_CREATE_NODE_PROBABILITY = 1                   ## > 0 - All subsequent expand_probabilities depend on this (Use in conjunction with NEW_NODE_CREATE_NODE_PROBABILITY_COEFFICIENT). Probability that the parent will reproduce in the first iteration.
                                                    ## Value between 0 and 1, above 1 is equivalent to 1, but gives bigger nodes (Node's circle radius is proportional to its expand_probability).
                                                    ## Adjust with CIRCLE_SIZE_COEFFICIENT.
                                                    ## Effective with non-zero wait, else simply slows the expansion. (for better understanding, study expectation of a binomial variable over 'n' tests).

BASIC_RANGE_COEFFICIENT = 1                         ## All subsequent ranges depend on this (Use in conjunction with NEW_NODE_RANGE_COEFFICIENT). Percentage of box (side length) to densely fill with pattern.
                                                    ## Effective between 0 and 1.

CREATE_NODE_PROBABILITY_LOSS_RATE = 1.1             ## For each child, a node's expand_probability is divided by this. Each new "generation" is less likely to reproduce, to account for the increasing size of the generation.
                                                    ## Typically between 1 and 1.5, below, growth is explosive, and creates some circular patterns (Node's circle radius is proportional to its expand_probability). Above, program stagnates quickly."""

NEW_NODE_CREATE_NODE_PROBABILITY_COEFFICIENT = 2    ## Child's initial expand_probability is parent's current expand_probability divided by this.
                                                    ## Typically greater than 1, else explosive growth.

NEW_NODE_RANGE_COEFFICIENT = 3                      ## Child's expand_range is parent's expand_range divided by this.
                                                    ## For > ~3, this creates connected "islands" of nodes., For lower values, a general mess is created.
AGE_COEFFICIENT = 0                                 ## Life is this many iterations.

"""
Display options
"""

CIRCLE_SIZE_COEFFICIENT = 10                        ## > 0 - Node's circle radius is proportional to its expand_probability, this is the proportionality constant.
LINE_WIDTH = 2                                      ## > 0, int - Width of connecting lines. Try 0, 10, 100 as well.
REDNESS = 1                                         ## 0 to 1 - reddishness of final pattern
GREENNESS = 0                                       ## 0 to 1 - greenishness of final pattern
BLUENESS = 1                                        ## 0 to 1 - bluishness of final pattern

"""
Example colouring - REDNESS, BLUENESS, GREENNESS -
1, 1, 1 - general mess.
0, 0, 0 - no, the program's not broken.
1, 0, 0 - Spiderman!
1, 1, 0 - violet lovers.
0, 0, 1 - Green Lantern.
1, 0, 1 - it's nice.
0, 1, 1 - peacock's tail
Try floats as well.
"""

class node(object):

    def __init__(self, position, expand_probability, expand_range):

        self.position = position                                            ## 2-tuple - (x, y) Note - pygame y is inverted, with origin at top left.
        self.expand_probability = expand_probability
        self.expand_range = min(expand_range,                               ## passed from parent
                                position[0],                                ## do not cross left edge,
                                WINDOW_SIZE - position[0],                  ## right edge,
                                position[1],                                ## top,
                                WINDOW_SIZE - position[1])                  ## bottom
        self.color = (int((REDNESS * 255) * random.random()), int((GREENNESS * 255) * random.random()), int((BLUENESS * 255) * random.random()))    ## final form - (0, 0, 0) to (255, 255, 255)
        self.remaining_life = AGE_COEFFICIENT
        self.children = []

    def update(self):

        """
            Return: node object child, if one is created, else False, to fail a later if condition.
        """

        self.remaining_life -= 1
        rand = random.random()
        if(rand < self.expand_probability):                                 ## Monte Carlo simulation
            new_x = int(self.position[0] + WIND_X + self.expand_range * (2 * random.random() - 1))      ## Random within a box centred at self.position, of side length 2 * self.expand_range, offset by WIND_X
            new_y = int(self.position[1] + WIND_Y + self.expand_range * (2 * random.random() - 1))      ## Random within a box centred at self.position, of side length 2 * self.expand_range, offset by WIND_X
            child = node((new_x, new_y), self.expand_probability / NEW_NODE_CREATE_NODE_PROBABILITY_COEFFICIENT, self.expand_range / NEW_NODE_RANGE_COEFFICIENT)
            self.children.append(child)
            return child
        return False

class program(object):

    def __init__(self):

        self.parent_node = node((int(WINDOW_SIZE / 2 + OFFSET_X), int(WINDOW_SIZE / 2 + OFFSET_Y)), BASIC_CREATE_NODE_PROBABILITY, int(BASIC_RANGE_COEFFICIENT * WINDOW_SIZE / 2)) ## Default parent, modify as you wish.
        self.basic_parents = [self.parent_node]
        self.all_nodes = [self.parent_node]
        self.output_manager = output()          ## Create output instance.
        self.main()

    def main(self):

        while(True):
            self.run()                          ## Run logic, and
            self.output_manager.display(self)   ## display result.

    def run(self):

        new_nodes = []
        for node in self.all_nodes:
            result = node.update()
            if(result):                         ## If a child was created,
                new_nodes.append(result)
                node.expand_probability /= CREATE_NODE_PROBABILITY_LOSS_RATE ## Lose some parent expand_probability
            if(not(node.remaining_life)):
                self.all_nodes.remove(node)
                try:
                    self.basic_parents.remove(node)
                except:
                    pass
                self.basic_parents.extend(node.children)
        self.all_nodes.extend(new_nodes)

class output(object):

    def __init__(self):
        
        screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
        pygame.display.set_caption("Starburst")
        self.screen = screen

    def display(self, program):

        self.screen.fill((0, 0, 0))             ## Optional, good practice. Start frame with blank screen, black.
        for node in program.all_nodes:
            self.draw_nodes(node)
        for node in program.basic_parents:
            self.draw_connections(node)
        pygame.display.flip()                   ## Display update occurs here, till now we were preparing the new display.
        time.sleep(WAIT_LENGTH)                 ## Pause program for WAIT_LENGTH.

    """
    NOTE - The following two functions do not update the screen, they simple prepare the next frame in the animation. The frame change occurs above, at pygame.display.flip(), in display.
       Also, new drawings are made on top of old ones, new frames aren't cleared by default. Use self.screen.fill((0, 0, 0)) to clear the frame.
    """

    def draw_nodes(self, node):

        pygame.draw.circle(self.screen, node.color, node.position, int(node.expand_probability * CIRCLE_SIZE_COEFFICIENT))  ## Last argument is radius.

    def draw_connections(self, parent_node):

        if(parent_node.children):
            for child in parent_node.children:
                pygame.draw.line(self.screen, parent_node.color, parent_node.position, child.position, LINE_WIDTH)
                self.draw_connections(child)                               ## Recursively draw connections of each child.

def use_example(name):

    global WINDOW_SIZE, WIND_X, WIND_Y, OFFSET_X, OFFSET_Y
    global WAIT_LENGTH, BASIC_CREATE_NODE_PROBABILITY, BASIC_RANGE_COEFFICIENT, CREATE_NODE_PROBABILITY_LOSS_RATE, NEW_NODE_CREATE_NODE_PROBABILITY_COEFFICIENT, NEW_NODE_RANGE_COEFFICIENT, AGE_COEFFICIENT
    global CIRCLE_SIZE_COEFFICIENT, LINE_WIDTH, REDNESS, GREENNESS, BLUENESS    
    (WINDOW_SIZE, WIND_X, WIND_Y, OFFSET_X, OFFSET_Y,
     WAIT_LENGTH, BASIC_CREATE_NODE_PROBABILITY, BASIC_RANGE_COEFFICIENT, CREATE_NODE_PROBABILITY_LOSS_RATE, NEW_NODE_CREATE_NODE_PROBABILITY_COEFFICIENT, NEW_NODE_RANGE_COEFFICIENT, AGE_COEFFICIENT,
     CIRCLE_SIZE_COEFFICIENT, LINE_WIDTH, REDNESS, GREENNESS, BLUENESS) = examples.set(name)

## use_example("fuzzball")

if(__name__ == "__main__"):
    program()
