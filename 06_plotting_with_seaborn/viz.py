"""
@File         : viz.py
@Author(s)    : Stephen CUI
@LastEditor(s): Stephen CUI
@CreatedTime  : 2025-08-16 15:11:11
@Email        : cuixuanstephen@gmail.com
@Description  :
"""

import itertools
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


def reg_resid_plots(data: pd.DataFrame):
    num_cols = data.shape[1]
    permutation_count = num_cols * (num_cols - 1)
    fig, ax = plt.subplots(permutation_count, 2, figsize=(15, 8))

    for (x, y), axes, color in zip(
        itertools.permutations(data.columns, 2),
        ax,
        itertools.cycle(["royalblue", "darkorange"]),
    ):
        for subplot, func in zip(axes, (sns.regplot, sns.residplot)):
            func(x=x, y=y, data=data, ax=subplot, color=color)
            if func == sns.residplot:
                subplot.set_ylabel("residuals")

    return fig.axes


def std_from_mean_kde(data: pd.Series):

    mean_mag, std_mean = data.mean(), data.std()

    ax = data.plot(kind="kde")
    ax.axvline(mean_mag, color="b", alpha=0.2, label="mean")
    colors = ["green", "orange", "red"]
    multipliers = [1, 2, 3]
    signs = ["-", "+"]
    linestyles = [":", "-.", "--"]
    for sign, (color, multiplier, style) in itertools.product(
        signs, zip(colors, multipliers, linestyles)
    ):
        adjustment = multiplier * std_mean
        if sign == "-":
            value = mean_mag - adjustment
            label = "{} {}{}{}".format(r"$\mu$", r"$\pm$", multiplier, r"$\sigma$")
        else:
            value = mean_mag + adjustment
            label = None

        ax.axvline(value, color=color, linestyle=style, label=label, alpha=0.5)
    ax.legend()
    return ax
