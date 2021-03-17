#----------------------------------------------------------------------------#
#                  Animation classes                                         #
#----------------------------------------------------------------------------#


import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


class Animation:
    """Create an animation of the epidemic.

    This creates a plot figure with two subplots:

        A colormap showing the status of the people.
        A line plot showing how many people are in each status.

    The resulting animation can either be shown on screen (with show()) or can
    be saved to a file (with save()).

    Example
    =======

    Create a simulation and animate it for 100 days showing the animation on
    screen:

    >>> sim = Simulation(10, 10, recovery=0.1, infection=0.2, death=0.05)
    >>> sim.infect_randomly(3)  # infect three people (chosen randomly)
    >>> anim = Animation(simulation, 100)
    >>> animshow()

    """

    def __init__(self, simulation, duration):
        self.simulation = simulation
        self.duration = duration

        self.figure = plt.figure(figsize=(8, 4))
        self.axes_grid = self.figure.add_subplot(1, 2, 1)
        self.axes_line = self.figure.add_subplot(1, 2, 2)

        self.gridanimation = GridAnimation(self.axes_grid, self.simulation)
        self.lineanimation = LineAnimation(self.axes_line, self.simulation, duration)

    def show(self):
        """Run the animation on screen"""
        animation = FuncAnimation(self.figure, self.update, frames=range(100),
                init_func = self.init, blit=True, interval=200)
        plt.show()

    def save(self, filename):
        """Run the animation and save to a video"""

        # NOTE: needs ffmpeg installed and on PATH
        animation = FuncAnimation(self.figure, self.update, frames=range(100),
                init_func = self.init, blit=True, interval=300)
        animation.save(filename, fps=30, extra_args=['-vcodec', 'libx264'])


    def init(self):
        """Initialise the animation (called by FuncAnimation)"""
        # We could generalise this to a loop and then it would work for any
        # numer of *animation objects.
        actors = []
        actors += self.gridanimation.init()
        actors += self.lineanimation.init()
        return actors

    def update(self, framenumber):
        """Update the animation (called by FuncAnimation)"""
        self.simulation.update()
        actors = []
        actors += self.gridanimation.update(framenumber)
        actors += self.lineanimation.update(framenumber)
        return actors


class GridAnimation:
    """Animate a grid showing status of people at each position"""

    def __init__(self, axes, simulation):
        self.axes = axes
        self.simulation = simulation
        rgb_matrix = self.simulation.get_rgb_matrix()
        self.image = self.axes.imshow(rgb_matrix)
        self.axes.set_xticks([])
        self.axes.set_yticks([])

    def init(self):
        return self.update(0)

    def update(self, framenum):
        day = framenum
        rgb_matrix = self.simulation.get_rgb_matrix()
        self.image.set_array(rgb_matrix)
        return [self.image]


class LineAnimation:
    """Animate a line series showing numbers of people in each status"""

    def __init__(self, axes, simulation, duration):
        self.axes = axes
        self.simulation = simulation
        self.duration = duration
        self.xdata = []
        self.ydata = {status: [] for status in simulation.STATUSES}
        self.line_mpl = {}
        for status, colour in simulation.COLOURMAP.items():
            [line] = self.axes.plot([], [], color=colour, label=status, linewidth=2)
            self.line_mpl[status] = line
        self.axes.legend(prop={'size':'x-small'}, loc='center right')
        self.axes.set_xlabel('days')
        self.axes.set_ylabel('%', rotation=0)

    def init(self):
        self.axes.set_xlim([0, self.duration])
        self.axes.set_ylim([0, 100])
        return []

    def update(self, framenum):
        percents = self.simulation.get_percentage_status()
        self.xdata.append(len(self.xdata))
        for status, percent in percents.items():
            self.ydata[status].append(percent)
            self.line_mpl[status].set_data(self.xdata, self.ydata[status])
        return list(self.line_mpl.values())
