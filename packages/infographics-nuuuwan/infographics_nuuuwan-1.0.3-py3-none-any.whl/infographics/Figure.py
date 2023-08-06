import matplotlib.pyplot as plt

from infographics import plotx


class Figure:
    def __init__(
        self,
        left_bottom=(0.1, 0.1),
        width_height=(0.8, 0.8),
        figure_text='',
    ):
        self.figure_text = figure_text
        self.left_bottom = left_bottom
        self.width_height = width_height

    def draw(self):
        ax = plt.axes(self.left_bottom + self.width_height)
        plotx.draw_text(
            (0.5, 0),
            self.figure_text,
            fontsize=12,
        )
        ax.axis('off')

    def set_position(
        self,
        left_bottom=(0.1, 0.1),
        width_height=(0.8, 0.8),
    ):
        self.left_bottom = left_bottom
        self.width_height = width_height
