"""Implements dorling."""
import colorsys
import math

import matplotlib.pyplot as plt
from utils import plotx

from cartogram import dorling_compress

N_LEGEND_VALUES = 5


def _default_func_get_radius_value(row):
    return row.population


def _default_func_format_radius_value(radius_value):
    return '{:,.0f}\npeople'.format(radius_value)


def _default_func_get_color_value(row):
    return row.population / row.area


def _default_func_value_to_color(density):
    log_density = math.log10(density)
    h = (1 - (log_density - 1) / 4) / 3
    (r, g, b) = colorsys.hsv_to_rgb(h, 0.8, 0.8)
    return (r, g, b, 0.8)


def _default_func_format_color_value(color_value):
    return '{:,.0f} per km²'.format(color_value)


def _default_func_render_label(ax, x, y, span_y, row):
    r2 = span_y / 40
    plotx.draw_text((x, y + r2), row['name'], fontsize=6)

    color_value = _default_func_get_color_value(row)
    rendered_color_value = _default_func_format_color_value(color_value)
    plotx.draw_text((x, y + r2 * 0.1), rendered_color_value, fontsize=8)

    radius_value = _default_func_get_radius_value(row)
    formatted_radius_value = _default_func_format_radius_value(radius_value)
    plotx.draw_text((x, y - r2), formatted_radius_value, fontsize=6)


def plot(
    geopandas_dataframe,
    left_bottom=(0.1, 0.1),
    width_height=(0.8, 0.8),
    func_get_radius_value=_default_func_get_radius_value,
    func_format_radius_value=_default_func_format_radius_value,
    func_get_color_value=_default_func_get_color_value,
    func_value_to_color=_default_func_value_to_color,
    func_format_color_value=_default_func_format_color_value,
    func_render_label=_default_func_render_label,
    compactness=0.3,
):
    """Plot Dorling Cartogram."""
    ax = plt.axes(left_bottom + width_height)

    n_regions = 0
    color_values = []
    radius_values = []
    bounds_list = []
    for _, row in geopandas_dataframe.iterrows():
        radius_values.append(func_get_radius_value(row))
        color_values.append(func_get_color_value(row))
        bounds_list.append(row.geometry.bounds)
        n_regions += 1
    minx = min(list(map(lambda m: m[0], bounds_list)))
    miny = min(list(map(lambda m: m[1], bounds_list)))
    maxx = max(list(map(lambda m: m[2], bounds_list)))
    maxy = max(list(map(lambda m: m[3], bounds_list)))
    area = (maxx - minx) * (maxy - miny)
    sum_radius_value = sum(radius_values)
    max_radius_value = max(radius_values)

    alpha = compactness * math.pi / 4
    beta = alpha * area / math.pi / sum_radius_value

    points = []
    for i_row, row in geopandas_dataframe.iterrows():
        points.append(
            {
                'x': row.geometry.centroid.x,
                'y': row.geometry.centroid.y,
                'r': math.sqrt(func_get_radius_value(row) * beta),
                'row': row,
            }
        )

    compressed_points = dorling_compress._compress(
        points,
        (minx, miny, maxx, maxy),
    )

    geopandas_dataframe.plot(
        ax=ax,
        color=plotx.DEFAULTS.COLOR_FILL,
        edgecolor=plotx.DEFAULTS.COLOR_STROKE,
        linewidth=plotx.DEFAULTS.STROKE_WIDTH,
    )
    span_x, span_y = maxx - minx, maxy - miny

    for point in compressed_points:
        x, y, r, row = point['x'], point['y'], point['r'], point['row']
        color_value = func_get_color_value(row)
        color = func_value_to_color(color_value)
        plotx.draw_circle((x, y), r, fill=color)
        if n_regions <= 30:
            func_render_label(ax, x, y, span_y, row)

    # radius legend
    x, y = (minx + span_x * 0.9), (miny + span_y * 0.75)
    radius_value = math.pow(10, round(math.log10(max_radius_value)))
    radius = math.sqrt(radius_value * beta)
    formatted_radius_value = func_format_radius_value(radius_value)
    plotx.draw_text((x, y), 'SCALE\n%s' % formatted_radius_value)
    plotx.draw_circle((x, y), radius)

    # color legend
    labels = []
    handles = []

    n_color_values = len(color_values)
    sorted_color_values = sorted(color_values, reverse=True)
    for i in range(0, N_LEGEND_VALUES):
        i_color_value = (int)(i * (n_color_values - 1) / (N_LEGEND_VALUES - 1))
        color_value = sorted_color_values[i_color_value]
        color = _default_func_value_to_color(color_value)
        labels.append(func_format_color_value(color_value))
        handles.append(plotx.get_color_patch(color))

    plt.legend(
        handles=handles,
        labels=labels,
    )
    plt.axis('off')
    return plt
