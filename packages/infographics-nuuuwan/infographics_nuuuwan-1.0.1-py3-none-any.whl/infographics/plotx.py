"""Various helpers for MatPlotLib"""

import logging

import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.patches import Patch

logging.basicConfig(level=logging.INFO)
log = logging.getLogger('utils.plotx')


class DEFAULTS:
    FONT_FAMILY = 'Futura'
    FONT_SIZE = 12
    COLOR = 'black'
    COLOR_STROKE = 'lightgray'
    COLOR_FILL = (0.9, 0.9, 0.9, 0.5)
    VERTICAL_ALIGNMENT = 'center'
    HORIZONTAL_ALIGNMENT = 'center'
    STROKE_WIDTH = 0.3


mpl.rc('font', family=DEFAULTS.FONT_FAMILY)


def get_bounds(gpd_df):
    n_regions = 0
    bounds_list = []
    for i_row, row in gpd_df.iterrows():
        n_regions += 1
        bounds_list.append(row.geometry.bounds)

    minx = min(list(map(lambda m: m[0], bounds_list)))
    miny = min(list(map(lambda m: m[1], bounds_list)))
    maxx = max(list(map(lambda m: m[2], bounds_list)))
    maxy = max(list(map(lambda m: m[3], bounds_list)))
    area = (maxx - minx) * (maxy - miny)
    spanx, spany = maxx - minx, maxy - miny

    return (
        n_regions,
        minx,
        miny,
        maxx,
        maxy,
        spanx,
        spany,
        area,
    )


def get_circle(
    cxy,
    r,
    fill=DEFAULTS.COLOR_FILL,
    stroke=DEFAULTS.COLOR_STROKE,
    stroke_width=DEFAULTS.STROKE_WIDTH,
):
    do_fill = fill is not None
    return plt.Circle(
        cxy,
        r,
        edgecolor=stroke,
        facecolor=fill,
        linewidth=stroke_width,
        fill=do_fill,
    )


def get_color_patch(color):
    """Draw color patch."""
    return Patch(color=color)


def draw_text(
    xy,
    text,
    verticalalignment=DEFAULTS.VERTICAL_ALIGNMENT,
    horizontalalignment=DEFAULTS.HORIZONTAL_ALIGNMENT,
    fontname=DEFAULTS.FONT_FAMILY,
    fontsize=DEFAULTS.FONT_SIZE,
    fontcolor=DEFAULTS.COLOR,
):
    """Draw text."""
    x, y = xy
    plt.text(
        x,
        y,
        text,
        verticalalignment=verticalalignment,
        horizontalalignment=horizontalalignment,
        fontsize=fontsize,
        fontname=fontname,
        color=fontcolor,
    )


def draw_circle(
    cxy,
    r,
    fill=DEFAULTS.COLOR_FILL,
    stroke=DEFAULTS.COLOR_STROKE,
    stroke_width=DEFAULTS.STROKE_WIDTH,
):
    """Draw circle."""
    ax = plt.gca()
    ax.add_patch(
        get_circle(
            cxy,
            r,
            stroke=stroke,
            fill=fill,
            stroke_width=stroke_width,
        )
    )


def draw_infographic(
    title,
    subtitle,
    footer_text,
    image_file,
    func_plot_inner,
):
    """Draw infographic."""
    plt.axes([0, 0, 1, 1])
    draw_text((0.5, 0.95), title, fontsize=24)
    draw_text((0.5, 0.9), subtitle, fontsize=12)
    draw_text((0.5, 0.05), footer_text, fontsize=8, fontcolor='gray')

    func_plot_inner()

    fig = plt.gcf()
    fig.set_size_inches(16, 9)

    plt.savefig(image_file)
    log.info('Saved infographic to %s', image_file)
