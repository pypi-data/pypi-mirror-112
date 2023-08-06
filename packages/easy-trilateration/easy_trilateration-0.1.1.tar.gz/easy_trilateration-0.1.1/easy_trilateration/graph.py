import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from random import randint

from easy_trilateration import model


def live_plotter(x_vec, y1_data, line1, identifier='', pause_time=0.1):
    if not line1:
        # this is the call to matplotlib that allows dynamic plotting
        plt.ion()
        fig = plt.figure(figsize=(13, 6))
        ax = fig.add_subplot(111)
        # create a variable for the line so we can later update it
        line1, = ax.plot(x_vec, y1_data, '-o', alpha=0.8)
        # update plot label/title
        plt.ylabel('Y Label')
        plt.title('Title: {}'.format(identifier))
        plt.show()

    # after the figure, axis, and line are created, we only need to update the y-data
    line1.set_ydata(y1_data)
    # adjust limits if new data goes beyond bounds
    if np.min(y1_data) <= line1.axes.get_ylim()[0] or np.max(y1_data) >= line1.axes.get_ylim()[1]:
        plt.ylim([np.min(y1_data) - np.std(y1_data), np.max(y1_data) + np.std(y1_data)])
    # this pauses the data so the figure/axis can catch up - the amount of pause can be altered above
    plt.pause(pause_time)

    # return line so we can update it again in the next iteration
    return line1


def demolive():
    plt.style.use('ggplot')
    size = 100
    x_vec = np.linspace(0, 1, size + 1)[0:-1]
    y_vec = np.random.randn(len(x_vec))
    line1 = []
    while True:
        rand_val = np.random.randn(1)
        y_vec[-1] = rand_val
        line1 = live_plotter(x_vec, y_vec, line1)
        y_vec = np.append(y_vec[1:], 0.0)


def create_circle(circle: model.Circle, target=False):
    color = matplotlib.cm.jet(randint(50, 100))
    if target:
        color = matplotlib.cm.jet(1000)
    add_shape(plt.Circle((circle.center.x, circle.center.y), color=color, fill=False, zorder=1, radius=circle.radius,
                         alpha=0.8))
    plt.scatter(circle.center.x, circle.center.y, color=color, s=100, zorder=2)


def create_point(point: model.Point, color=matplotlib.cm.jet(randint(0, 00))):
    plt.scatter(point.x, point.y, color=color, s=100, zorder=2)


def add_shape(patch):
    ax = plt.gca()
    ax.add_patch(patch)
    plt.axis('scaled')


def draw(drawlist):
    for item in drawlist:
        if isinstance(item, model.Circle):
            create_circle(item)
        if isinstance(item, model.Point):
            create_point(item)
    plt.show()



