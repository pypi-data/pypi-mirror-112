import matplotlib.pyplot as plt
import matplotlib.lines as lines
from . import style_css


def descriptive_plot(figsize=(8, 6), line_pos_x_axis=1, background_color=None):

    if background_color is None:
        background_color = style_css.get_background_color()

    fig, ax = plt.subplots(1, 1, figsize=figsize, facecolor=background_color)

    ax.set_facecolor(background_color)

    line = lines.Line2D([line_pos_x_axis, line_pos_x_axis], [0, 1], transform=fig.transFigure, figure=fig,
                        color='black', lw=0.4)
    fig.lines.extend([line])

    return fig, ax


def vertical_descriptive_plot(figsize=(6, 8), plots=3, plot_height=0.5, plot_width=0.75, background_color=None):
    if plot_width > 1.4:
        raise Exception('Plot width cannot be greater than 1.5')

    if background_color is None:
        background_color = style_css.get_background_color()

    fig = plt.figure(figsize=figsize, facecolor=background_color)
    axes = []

    initial_axis = 0
    for _ in range(plots):
        axis = fig.add_axes([0, initial_axis, plot_width, plot_height])
        axis.set_facecolor(background_color)
        axes.append(axis)
        initial_axis += plot_height + 0.1

    line_length = (plot_height + 0.1) * plots
    line = lines.Line2D([plot_width + 0.1, plot_width + 0.1], [0 - 0.1, line_length], transform=fig.transFigure,
                        figure=fig, color='black', lw=0.4)
    fig.lines.extend([line])

    return fig, axes


def horizontal_descriptive_plot(figsize=(8, 6), plots=3, plot_height=0.75, line_pos_y_axis=-0.1,
                                background_color=None):
    if plots not in [2, 3, 4]:
        raise Exception('Number of plots must be 2, 3 or 4')

    # Plot Position on X-axis
    increment = {2: 1, 3: 0.7, 4: 0.5}

    # Plot width based on number of plots required
    plot_width = {2: 0.9, 3: 0.6, 4: 0.43}

    if background_color is None:
        background_color = style_css.get_background_color()

    fig = plt.figure(figsize=figsize, facecolor=background_color)
    axes = []

    initial_axis = 0
    for _ in range(plots):
        axis = fig.add_axes([initial_axis, 0, plot_width[plots], plot_height])
        axis.set_facecolor(background_color)
        axes.append(axis)
        initial_axis += increment[plots]

    line_length = increment[plots] * (plots - 1) + plot_width[plots]
    line = lines.Line2D([0 - 0.1, line_length + 0.1], [line_pos_y_axis, line_pos_y_axis], transform=fig.transFigure,
                        figure=fig, color='black', lw=0.4)
    fig.lines.extend([line])

    return fig, axes
