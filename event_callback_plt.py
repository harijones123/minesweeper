import numpy as np
import matplotlib.pyplot as plt

fig = plt.figure()
ax = fig.add_subplot(111, xlim=(-1, 2), ylim=(-1, 2))
polygon = plt.Polygon([[0, 0], [1, 0], [1, 1], [0, 1], [0, 0]])
ax.add_patch(polygon)

# set the picker to True, so that pick events are registered
polygon.set_picker(True)

# create a function to be bound to pick events: here the event has an
# attribute `artist` which points to the object which was clicked
def on_pick(event):
    event.artist.set_facecolor(np.random.random(3))
    fig.canvas.draw()

# bind pick events to our on_pick function
fig.canvas.mpl_connect('pick_event', on_pick)
plt.show()