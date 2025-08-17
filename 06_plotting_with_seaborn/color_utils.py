"""
@File         : color_utils.py
@Author(s)    : Stephen CUI
@LastEditor(s): Stephen CUI
@CreatedTime  : 2025-08-17 10:58:23
@Email        : cuixuanstephen@gmail.com
@Description  :
"""

import re
from matplotlib.colors import ListedColormap
import numpy as np


def hex_to_rgb_color_list(colors: list[str] | str):
    if isinstance(colors, str):
        colors = [colors]

    for i, color in enumerate([color.replace("#", "") for color in colors]):
        hex_length = len(color)

        if hex_length not in [3, 6]:
            raise ValueError("Colors must be of the form #FFFFFF or #FFF")

        regex = "." * (hex_length // 3)

        colors[i] = [
            int(val * (6 // hex_length), 16) / 255 for val in re.findall(regex, color)
        ]

    return colors[0] if len(colors) == 1 else colors


def blended_map(rgb_color_list):
    if not isinstance(rgb_color_list, list):
        raise ValueError("Colors must be passed as a list.")
    elif len(rgb_color_list) < 2:
        raise ValueError("Must specify at least 2 colors.")
    elif (
        not isinstance(rgb_color_list[0], list)
        or not (isinstance(rgb_color_list[1], list))
    ) or ((len(rgb_color_list[0]) != 3 or len(rgb_color_list[1]) != 3)):
        raise ValueError("Each color should be a list of size 3.")

    N, entries = 256, 4  # red, green, blue, alpha
    rgbas = np.ones((N, entries))

    segment_count = len(rgb_color_list) - 1
    segment_size = N // segment_count
    remainder = N % segment_count

    for i in range(entries - 1):
        updates = []
        for seg in range(1, segment_count + 1):
            offset = 0 if not remainder or seg > 1 else remainder

            updates.append(
                np.linspace(
                    start=rgb_color_list[seg - 1][i],
                    stop=rgb_color_list[seg][i],
                    num=segment_size + offset,
                )
            )
        rgbas[:, i] = np.concatenate(updates)
    return ListedColormap(rgbas)


import matplotlib.pyplot as plt


def draw_cmap(cmap, values=np.array([[0, 1]]), **kwargs):

    img = plt.imshow(values, cmap=cmap)
    cbar = plt.colorbar(**kwargs)
    img.axes.remove()

    return cbar
