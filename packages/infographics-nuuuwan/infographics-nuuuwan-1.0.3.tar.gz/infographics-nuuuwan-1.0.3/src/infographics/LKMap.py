import colorsys
import math

import matplotlib.pyplot as plt
from geo import geodata

from infographics import Figure, plotx

MAX_LEGEND_ITEMS = 7


def _default_func_get_color_value(row):
    return row.population / row.area


def _default_func_value_to_color(density):
    log_density = math.log10(density)
    h = (1 - (log_density - 1) / 4) / 3
    (r, g, b) = colorsys.hsv_to_rgb(h, 0.8, 0.8)
    return (r, g, b)


def _default_func_format_color_value(color_value):
    return '{:,.0f} per km²'.format(color_value)


def _default_func_render_label(row, x, y, spany):
    r2 = spany / 40
    plotx.draw_text((x, y + r2), row['name'], fontsize=6)

    color_value = _default_func_get_color_value(row)
    rendered_color_value = _default_func_format_color_value(color_value)
    plotx.draw_text((x, y + r2 * 0.1), rendered_color_value, fontsize=8)


class LKMap(Figure.Figure):
    def __init__(
        self,
        region_id='LK',
        sub_region_type='province',
        figure_text='',
        func_get_color_value=_default_func_get_color_value,
        func_value_to_color=_default_func_value_to_color,
        func_value_to_color_surface=None,
        func_format_color_value=_default_func_format_color_value,
        func_render_label=_default_func_render_label,
        left_bottom=(0.1, 0.1),
        width_height=(0.8, 0.8),
    ):
        super().__init__(
            left_bottom=left_bottom,
            width_height=width_height,
            figure_text=figure_text,
        )

        self.region_id = region_id
        self.sub_region_type = sub_region_type
        self.figure_text = figure_text

        self.func_get_color_value = func_get_color_value
        self.func_value_to_color = func_value_to_color
        self.func_format_color_value = func_format_color_value
        self.func_render_label = func_render_label

        self.func_value_to_color_surface = (
            func_value_to_color_surface
            if func_value_to_color_surface
            else self.func_value_to_color
        )

        self.__data__ = LKMap.__prep_data__(self)

    def __prep_data__(self):
        gpd_df = geodata.get_region_geodata(
            self.region_id,
            self.sub_region_type,
        )

        (
            n_regions,
            minx,
            miny,
            maxx,
            maxy,
            spanx,
            spany,
            area,
        ) = plotx.get_bounds(gpd_df)

        color_values = []
        gpd_df['color'] = gpd_df['id'].astype(object)
        for i_row, row in gpd_df.iterrows():
            color_value = self.func_get_color_value(row)
            color_values.append(color_value)
            color = self.func_value_to_color_surface(color_value)
            gpd_df.at[i_row, 'color'] = color

        return (
            n_regions,
            minx,
            miny,
            maxx,
            maxy,
            spanx,
            spany,
            area,
            gpd_df,
            color_values,
        )

    def draw(self):
        super().draw()

        (
            n_regions,
            minx,
            miny,
            maxx,
            maxy,
            spanx,
            spany,
            area,
            gpd_df,
            color_values,
            *child_params,
        ) = self.__data__

        ax = plt.axes(self.left_bottom + self.width_height)
        gpd_df.plot(
            ax=ax,
            color=gpd_df['color'],
            edgecolor=plotx.DEFAULTS.COLOR_STROKE,
            linewidth=plotx.DEFAULTS.STROKE_WIDTH,
        )

        for i_row, row in gpd_df.iterrows():
            self.func_render_label(
                row,
                row.geometry.centroid.x,
                row.geometry.centroid.y,
                spany,
            )

        # color legend
        formatted_value_to_color = {}
        for color_value in color_values:
            color = self.func_value_to_color(color_value)
            formatted_value = self.func_format_color_value(color_value)
            formatted_value_to_color[formatted_value] = color

        formatted_value_and_color = sorted(
            formatted_value_to_color.items(),
            key=lambda x: x[0],
        )
        n_actual = len(formatted_value_and_color)
        n_legend_items = min(n_actual, MAX_LEGEND_ITEMS)

        labels = []
        handles = []
        for i in range(0, n_legend_items):
            if n_actual == 1:
                j = 0
            else:
                j = (int)(i * (n_actual - 1) / (n_legend_items - 1))

            formatted_value, color = formatted_value_and_color[j]
            labels.append(formatted_value)
            handles.append(plotx.get_color_patch(color))

        plt.legend(handles=handles, labels=labels)

        ax.axis('off')
