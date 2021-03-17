#!/usr/bin/env python

from simulator.sir import Simulation
from simulator.plot import plot_simulation
import matplotlib.pyplot as plt


def main(filename=None):
    sim = Simulation(10, 10, recovery=0.1, infection=0.2, death=0.05)
    sim.infect_randomly(3)  # infect three people (chosen randomly)
    fig = plot_simulation(sim, 100)

    if filename is None:
        plt.show()
    else:
        fig.savefig(filename)


if __name__ == "__main__":
    import sys
    args = sys.argv[1:]
    main(*args)
