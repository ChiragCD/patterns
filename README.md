# patterns
Creates and displays random patterns using python and pygame.

Starburst - 

Create star-topology like patterns, with a considerable random element.

Uses pygame for display,
     random to generate the pattern
     time as an option for slowing the program

The only external module here is pygame, this can be installed with 
terminal:~$ pip3 install pygame
The version used here is 1.9.4

The program starts with a single parent node, who, with each iteration, has an expand_probability of creating and connecting to a node, within expand_range,
the child node has a fraction (or multiple) of the parent's expand_ attributes, random colour. This node is kept in the parent's children list.
With each new child, the parent's expand_probability decreases.

As a result of this setup, each node is a parent of its own network, represented in its colour.
Each new "generation" is less likely to reproduce, to account for the increasing size of the generation.
Node's circle radius is proportional to its expand_probability.

Go ahead and experiment with options, and with the program itself. Feel free to send me screenshots, and PR modified versions into this folder. Any fun patterns
you made can be PR'd by adding your parameters, with a name, in the examples.py database. Suggestions are welcome, please contribute toward solving the issues.

Examples:

![Starburst](/starburst_examples/starburst-violet.png)

![Starburst](/starburst_examples/starburst-greenyellow.png)
