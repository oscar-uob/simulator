#----------------------------------------------------------------------------#
#                  Class design                                              #
#----------------------------------------------------------------------------#

# There are a number of classes here which could be combined in different
# ways.  The idea is that the same classes could be reused for other things.
# The classes are:
#
#    Simulation - stores and updates the simulation state
#    Animation - runs an animation of the simulation
#    GridAnimation - animates the epidemic on a grid
#    LineAnimation - animates a timeseries of the epidemic
#
# The idea is that the Animation class sets up a plot window and creates a
# GridAnimation and LineAnimation to manage the two different plot windows
# that are animated. Each of those has update() and init() methods which the
# Animation class will call to update the view. The Animation class also calls
# the update() method of the Simulation class. The Simulation class provides
# two ways to access the state of the simultion which are get_rgb_matrix() and
# get_percentage_status() and these are used by the *Animation classes to get
# the data that they need to display.
#
# The intention in this design is that the different pieces can be combined in
# different ways. For example it would be possible to make an alternative
# version of the Simulation class that simulated a different model of the
# epidemic. As long as it hsa the update(), get_rgb_matrix() and
# get_percentage_status() methods then it can work with all of the animation
# classes. Also it would be possible to create an alternative version of the
# Animation class that can still reuse e.g. LineAnimation even if it does not
# want to use GridAnimation. Finally other *Animation classes could be created
# as well and could easily be adapted to the scheme just by adding update()
# and init() methods.
