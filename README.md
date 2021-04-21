runsim.py
Oscar Benjamin
March 2021

Note from Max I hope this is working 

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
