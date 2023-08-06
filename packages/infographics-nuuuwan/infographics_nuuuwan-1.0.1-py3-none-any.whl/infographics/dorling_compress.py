"""Implements dorling."""
import math

from utils import ds

from infographics._utils import log


def _compress(points, bounds):
    (minx, miny, maxx, maxy) = bounds
    dt = 0.01
    n_points = len(points)

    n_epochs = 300
    for i_epochs in range(0, n_epochs):
        if i_epochs % (n_epochs / 10) == 0:
            log.debug('i_epochs = {:,}'.format(i_epochs))
        no_moves = True
        for i_a in range(0, n_points):
            x_a, y_a, r_a = ds.dict_get(
                points[i_a],
                ['x', 'y', 'r'],
            )

            d_minx = (x_a - r_a) - minx
            d_miny = (y_a - r_a) - miny
            d_maxx = maxx - (x_a + r_a)
            d_maxy = maxy - (y_a + r_a)

            if any([d_minx < 0, d_miny < 0, d_maxx < 0, d_maxy < 0]):
                if d_minx < 0:
                    x_a = minx + r_a
                if d_miny < 0:
                    y_a = miny + r_a

                if d_maxx < 0:
                    x_a = maxx - r_a
                if d_maxy < 0:
                    y_a = maxy - r_a
                points[i_a]['x'] = x_a
                points[i_a]['y'] = y_a
                no_moves = False
                continue

            sx, sy = 0, 0
            for i_b in range(0, n_points):
                if i_a == i_b:
                    continue

                x_b, y_b, r_b = ds.dict_get(
                    points[i_b],
                    ['x', 'y', 'r'],
                )
                dx, dy = x_b - x_a, y_b - y_a
                d2 = dx ** 2 + dy ** 2
                d = math.sqrt(d2)
                if d > r_a + r_b:
                    continue

                f_b_a = -(r_b ** 2) / d2
                s = dt * f_b_a
                theta = math.atan2(dy, dx)
                sx += s * math.cos(theta)
                sy += s * math.sin(theta)

            points[i_a]['x'] += sx
            points[i_a]['y'] += sy
            no_moves = False

        if no_moves:
            break
    return points
