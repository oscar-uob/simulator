#----------------------------------------------------------------------------#
#                  Simulation class                                          #
#----------------------------------------------------------------------------#


import numpy as np
from numpy.random import random, randint


class Simulation:
    """Simulation of an epidemic on a 2D grid

    In this model there are four states:
    susceptible (S), infected (I), recovered (R) and dead (D).

    The people are arranged in a grid in each state so e.g. if we have a 4x4
    grid the initial state might be like:

    S S S S
    S S I S
    S S S S
    S S S S

    The update() method advances the simulation by one day. For example the
    new state might be:

    S S S S
    S I R S
    S S S I
    S S S S

    Here the person who was infected (I) is now recovered (R). However two of
    their neighbours who were susceptible (S) are now infected (I).

    The state update is not deterministic and is given by probabilities
    according to the following rules:

    1) Infected: an infected person might recover (-> R) with probability given
    by the recovery_probability parameter (default 0.1)

    2) Infected: if an infected person does not recover then they might die (-> D)
    with probability death_propability (default 0.005)

    3) Susceptible: a susceptible person might get infected (-> I) by one of
    their 8 neighbours in the grid. If N of their neighbours are infected then
    they will become infected with probability N*infection_probability where
    infection_probability is a simulation parameter (default 0.1)

    The methods get_rgb_matrix() and get_percentage_status() can be used to
    query the state of the simulation at any time.

    Example
    =======

    Create a simulation on a 10x10 grid (with 100 people) with probabilities
    0.1, 0.2 and 0.05 for recovery, infection and death and 3 people initially
    infected. Run the simulation for 10 days and then ask what percentage of
    people are in each state:

    >>> sim = Simulation(10, 10, recovery=0.1, infection=0.2, death=0.05)
    >>> sim.infect_randomly(3)  # infect three people (chosen randomly)
    >>> for n in range(10):     # advance the simulation through 10 days
    ...     sim.update()
    >>> sim.get_percentage_status()
    {'susceptible': 90.0, 'infected': 6.0, 'recovered': 3.0, 'dead': 1.0}

    """

    # Status codes to store in the numpy array representing the state.
    SUSCEPTIBLE = 0
    INFECTED = 1
    RECOVERED = 2
    DEAD = 3

    STATUSES = {
        'susceptible': SUSCEPTIBLE,
        'infected': INFECTED,
        'recovered': RECOVERED,
        'dead': DEAD,
    }
    COLOURMAP = {
        'susceptible': 'green',
        'infected': 'red',
        'recovered': 'blue',
        'dead': 'black',
    }
    COLOURMAP_RGB = {
        'red': (255, 0, 0),
        'green': (0, 255, 0),
        'blue': (0, 0, 255),
        'black': (0, 0, 0),
    }

    def __init__(self, width, height, recovery, infection, death):
        # Basic simulation parameters:
        self.day = 0
        self.width = width
        self.height = height
        self.recovery_probability = recovery
        self.infection_probability = infection
        self.death_probability = death

        # Initial state (everyone susceptible)
        self.state = np.zeros((width, height), int)
        self.state[:, :] = self.SUSCEPTIBLE

    def infect_randomly(self, num):
        """Choose num people randomly and make them infected"""
        for n in range(num):
            # Choose a random x, y coordinate and make that person infected
            # NOTE: This might select the same person twice...
            i = randint(self.width)
            j = randint(self.height)
            self.state[i, j] = self.INFECTED

    def update(self):
        """Advance the simulation by one day"""
        # Use a copy of the old state to store the new state so that e.g. if
        # someone recovers but was infected yesterday their neighbours might
        # still become infected today.
        old_state = self.state
        new_state = old_state.copy()
        for i in range(self.width):
            for j in range(self.height):
                new_state[i, j] = self.get_new_status(old_state, i, j)
        self.state = new_state
        self.day += 1

    def get_new_status(self, state, i, j):
        """Compute new status for person at i, j in the grid"""
        status = state[i, j]

        # Update infected person
        if status == self.INFECTED:
            if self.recovery_probability > random():
                return self.RECOVERED
            elif self.death_probability > random():
                return self.DEAD

        # Update susceptible person
        elif status == self.SUSCEPTIBLE:
            num = self.num_infected_around(state, i, j)
            if num * self.infection_probability > random():
                return self.INFECTED

        # Return the old status (e.g. DEAD/RECOVERED)
        return status

    def num_infected_around(self, state, i, j):
        """Count the number of infected people around person i, j"""

        # Need to be careful about people at the edge of the grid.
        # ivals and jvals are the coordinates of neighbours around i, j
        ivals = range(max(i-1, 0), min(i+2, self.width))
        jvals = range(max(j-1, 0), min(j+2, self.height))
        number = 0
        for ip in ivals:
            for jp in jvals:
                # Don't count self as a neighbour
                if (ip, jp) != (i, j):
                    if state[ip, jp] == self.INFECTED:
                        number += 1

        return number

    def get_percentage_status(self):
        """Dict giving percentage of people in each statue"""

        # NOTE: Maybe it's better to return counts rather than percentages...
        simgrid = self.state
        total = self.width * self.height
        percentages = {}
        for status, statusnum in self.STATUSES.items():
            count = np.count_nonzero(simgrid == statusnum)
            percentages[status] = 100 * count / total
        return percentages

    def get_rgb_matrix(self):
        """RGB matrix representing the statuses of the people in the grid

        This represents the state as an RGB (colour) matrix using the
        coloursceheme set in the class variables COLOURMAP and COLOURMAP_RGB.
        The resulting matrix is suitable to be used with e.g. matplotlib's
        imshow function.
        """
        rgb_matrix = np.zeros((self.width, self.height, 3), int)
        for status, statusnum in self.STATUSES.items():
            colour_name = self.COLOURMAP[status]
            colour_rgb = self.COLOURMAP_RGB[colour_name]
            rgb_matrix[self.state == statusnum] = colour_rgb
        return rgb_matrix
