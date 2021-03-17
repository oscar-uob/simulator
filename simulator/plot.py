#
# Run simulation and plot the result
#


import matplotlib.pyplot as plt


def plot_simulation(simulation, duration):
    """Produce a plot showing grid status at different points in time.

    Creates a 5x3 grid of subplots showing the status at 15 different days
    throughout the simulation.

    Example
    =======

    >>> sim = Simulation(10, 10, recovery=0.1, infection=0.2, death=0.05)
    >>> sim.infect_randomly(3)  # infect three people (chosen randomly)
    >>> fig = plot_simulation(simulation, 100)
    >>> plt.show()

    """
    # NOTE: Maybe this should be configurable e.g. could be W and H or (W, H)
    # arguments to plot_simulation.
    W, H = 5, 3
    N = W*H

    fig = plt.figure()
    axes = fig.subplots(nrows=H, ncols=W).flat

    # Fix the spacing between subplots:
    fig.subplots_adjust(wspace=0.1, hspace=0.4)

    # Try to find days that are approximately equally spaced although N might
    # not divide duration exactly.
    days = [(duration * i) // (N - 1) for i in range(N)]

    for ax, day in zip(axes, days):
        while simulation.day < day:
            simulation.update()
        rgb_matrix = simulation.get_rgb_matrix()
        ax.imshow(rgb_matrix)
        ax.set_title('Day ' + str(day))
        ax.set_xticks([])
        ax.set_yticks([])

    # Return the figure. The caller of this function can decide whether to use
    # show (screen) or savefig (file).
    return fig
