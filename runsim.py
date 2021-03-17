#!/usr/bin/env python3
"""

runsim.py
Oscar Benjamin
March 2021

This script runs simulations of an epidemic (e.g. coronavirus) spreading
around people on a 2-dimensional grid. The script can be used to:

    1. Show an animation of the simulation on screen
    2. Create a video of a simulation
    3. Show a plot of different stages of the epidemic
    4. Save a plot to a file

This is all done using the same simulation code which can also be imported
from this file and used in other ways.

The command line interface to the script makes it possible to run different
simulations without needing to edit the code e.g.:

    $ python runsim.py               # run simulation with default settings
    $ python runsim.py --cases=10    # have 10 initial cases
    $ python runsim.py --help        # show all command line options

It is also possible to create a video of the animation (if you install
ffmpeg):

    $ python runsim.py --file=simulation.mp4

NOTE: You need to install ffmpeg for the above to work. The ffmpeg program
must also be on PATH.
"""


import argparse

import matplotlib.pyplot as plt

from simulator.sir import Simulation
from simulator.animation import Animation
from simulator.plot import plot_simulation


def main(*args):
    """Command line entry point.

    $ python runsim.py                        # show animation on screen
    $ python runsim.py --file=video.mp4       # save animation to video
    $ python runsim.py --plot                 # show plot on screen
    $ python runsim.py --plot --file=plot.pdf # save plot to pdf

    """
    #
    # Use argparse to handle parsing the command line arguments.
    #   https://docs.python.org/3/library/argparse.html
    #
    parser = argparse.ArgumentParser(description='Animate an epidemic')
    parser.add_argument('--size', metavar='N', type=int, default=50,
                        help='Use a N x N simulation grid')
    parser.add_argument('--duration', metavar='T', type=int, default=100,
                        help='Simulate for T days')
    parser.add_argument('--recovery', metavar='P', type=float, default=0.1,
                        help='Probability of recovery (per day)')
    parser.add_argument('--infection', metavar='P', type=float, default=0.1,
                        help='Probability of infecting a neighbour (per day)')
    parser.add_argument('--death', metavar='P', type=float, default=0.005,
                        help='Probability of dying when infected (per day)')
    parser.add_argument('--cases', metavar='N', type=int, default=2,
                        help='Number of initial infected people')
    parser.add_argument('--plot', action='store_true',
                        help='Generate plots instead of an animation')
    parser.add_argument('--file', metavar='N', type=str, default=None,
                        help='Filename to save to instead of showing on screen')
    args = parser.parse_args(args)

    # Set up the simulation
    simulation = Simulation(args.size, args.size,
                            args.recovery, args.infection, args.death)
    simulation.infect_randomly(args.cases)

    # Plot or animation?
    if args.plot:
        fig = plot_simulation(simulation, args.duration)

        if args.file is None:
            #  python runsim.py --plot
            plt.show()
        else:
            #  python runsim.py --plot --file=plot.pdf
            fig.savefig(args.file)
    else:
        animation = Animation(simulation, args.duration)

        if args.file is None:
            #  python runsim.py
            animation.show()
        else:
            #  python runsim.py --file=animation.mp4
            #
            # NOTE: this needs ffmpeg to be installed.
            animation.save(args.file)


if __name__ == "__main__":
    #
    # CLI entry point. The main() function can also be imported and called
    # with string arguments.
    #
    import sys
    main(*sys.argv[1:])
