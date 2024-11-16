"""
Plot a combined histogram and scatter plot from omero screen cell cycle data.
"""

from pathlib import Path
from typing import Optional

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from matplotlib import ticker
from matplotlib.axes import Axes
from matplotlib.gridspec import GridSpec

from omero_screen_analysis.utils import save_fig, selector_val_filter

current_dir = Path(__file__).parent
style_path = (current_dir / "../../hhlab_style01.mplstyle").resolve()
plt.style.use(style_path)
prop_cycle = plt.rcParams["axes.prop_cycle"]
COLORS = prop_cycle.by_key()["color"]
pd.options.mode.chained_assignment = None


# Functions to plot histogram and scatter plots
def plot_histogram(
    ax: Axes, i: int, data: pd.DataFrame, colors: list[str]
) -> None:
    """
    Plot a histogram of the integrated DAPI intensity.

    Parameters
    ----------
    ax : Axes
        The axes on which to plot the histogram.
    i : int
        The index of the histogram (used for labeling).
    data : pd.DataFrame
        The data containing the integrated DAPI intensity.
    colors : list[str]
        A list of colors to use for the histogram.

    Returns
    -------
    None
        This function does not return a value.
    """
    sns.histplot(
        data=data, x="integrated_int_DAPI_norm", ax=ax, color=colors[-1]
    )
    ax.set_xlabel("")
    ax.set_xscale("log", base=2)
    ax.set_xlim(1, 16)
    ax.xaxis.set_visible(False)
    if i == 0:
        ax.set_ylabel("Freq.", fontsize=6)
    else:
        ax.yaxis.set_visible(False)
    ax.tick_params(axis="both", which="major", labelsize=6)


def plot_scatter(
    ax: Axes,
    i: int,
    data: pd.DataFrame,
    conditions: list[str],
    colors: list[str],
) -> None:
    """
    Plot a scatter plot of the integrated DAPI intensity vs. the mean EdU intensity.

    Parameters
    ----------
    ax : plt.Axes
        The axes on which to plot the scatter plot.
    i : int
        The index of the scatter plot (used for labeling).
    data : pd.DataFrame
        The data containing the integrated DAPI intensity and mean EdU intensity.
    conditions : list[str]
        The conditions to use for the scatter plot.
    colors : list[str]
        A list of colors to use for the scatter plot.

    Returns
    -------
    None
        This function does not return a value.
    """
    phases = ["Sub-G1", "G1", "S", "G2/M", "Polyploid"]
    sns.scatterplot(
        data=data,
        x="integrated_int_DAPI_norm",
        y="intensity_mean_EdU_nucleus_norm",
        hue="cell_cycle",
        hue_order=phases,
        s=2,
        alpha=1,
        ax=ax,
    )
    ax.set_xscale("log")
    ax.set_yscale("log", base=2)
    ax.grid(False)
    ax.xaxis.set_major_formatter(
        ticker.FuncFormatter(lambda x, pos: str(int(x)))
    )
    ax.set_xticks([2, 4, 8])
    ax.set_xlim(1, 16)
    if i == len(conditions):
        ax.set_ylabel("norm. EdU int.", fontsize=6)
        ax.yaxis.set_major_formatter(
            ticker.FuncFormatter(lambda x, pos: str(int(x)))
        )
    else:
        ax.yaxis.set_visible(False)
    ax.legend().remove()
    ax.set_xlabel("")
    ax.axvline(x=3, color="black", linestyle="--")
    ax.axhline(y=3, color="black", linestyle="--")
    sns.kdeplot(
        data=data,
        x="integrated_int_DAPI_norm",
        y="intensity_mean_EdU_nucleus_norm",
        fill=True,
        alpha=0.3,
        cmap="rocket_r",
        ax=ax,
    )
    ax.tick_params(axis="both", which="major", labelsize=6)
    ax.set_xlabel("")


def plot_scatter_col(
    ax: Axes,
    i: int,
    data: pd.DataFrame,
    conditions: list[str],
    col: str,
    y_lim: float,
    colors: list[str],
) -> None:
    """
    Plot a scatter plot of the integrated DAPI intensity vs. a specified column.


    Parameters
    ----------
    ax : plt.Axes
        The axes on which to plot the scatter plot.
    i : int
        The index of the scatter plot (used for labeling).
    data : pd.DataFrame
        The data containing the integrated DAPI intensity and the specified column.
    conditions : list[str]
        The conditions to use for the scatter plot.
    col : str
        The column to plot against the integrated DAPI intensity.
    colors : list[str]
        A list of colors to use for the scatter plot.
    """
    data.loc[:, "color"] = data[col].apply(
        lambda x: colors[0] if x < y_lim else colors[1]
    )
    sns.scatterplot(
        data=data,
        x="integrated_int_DAPI_norm",
        y=col,
        hue="color",
        palette=[colors[-1], colors[1]],
        hue_order=[colors[-1], colors[1]],
        s=2,
        alpha=1,
        ax=ax,
    )
    ax.set_xscale("log")
    ax.set_yscale("log", base=2)
    ax.grid(False)
    ax.xaxis.set_major_formatter(
        ticker.FuncFormatter(lambda x, pos: str(int(x)))
    )
    ax.set_xticks([2, 4, 8])
    ax.set_xlim(1, 16)

    # Set specific y-axis ticks and labels
    ax.set_yticks([2000, 4000, 8000, 16000])
    ax.set_yticklabels(["2", "4", "8", "16"])

    if i == len(conditions) * 2:
        ax.set_ylabel(col, fontsize=6)
        # Custom y-axis formatter to remove zeros
        ax.yaxis.set_major_formatter(
            ticker.FuncFormatter(lambda y, _: f"{y / 1000:g}")
        )
    else:
        ax.yaxis.set_visible(False)

    ax.legend().remove()
    ax.set_xlabel("")
    ax.axvline(x=3, color="black", linestyle="--")
    ax.axhline(y=3, color="black", linestyle="--")

    ax.tick_params(axis="both", which="major", labelsize=6)
    ax.set_xlabel("")


# Define figure size in inches
width = 10 / 2.54  # 10 cm
height = 7 / 2.54  # 4 cm


def combplot(
    df: pd.DataFrame,
    conditions: list[str],
    feature_col: str,
    feature_y_lim: float,
    condition_col: str = "condition",
    selector_col: Optional[str] = "cell_line",
    selector_val: Optional[str] = None,
    title_str: str | None = None,
    cell_number: int | None = None,
    colors: list[str] = COLORS,
    save: bool = True,
    path: Path | None = None,
) -> None:
    """
    Plot a combined histogram and scatter plot.

    Parameters
    ----------
    df : pd.DataFrame
        The data to plot.
    conditions : list[str]
        The conditions to plot.
    feature_col : str
        The feature column to plot.
    path : Path
        The path to save the figure.
    selector_col : str | None, optional
        The selector column to filter the data. Defaults to None.
    title_str : str | None, optional
        The title string. Defaults to None.
    cell_number : int | None, optional
        The number of cells to plot. Defaults to None.
    save : bool, optional
        Whether to save the figure. Defaults to True.
    """
    col_number = len(conditions)
    df1 = selector_val_filter(df, selector_col, selector_val)
    assert df1 is not None  # tells type checker df1 is definitely not None
    condition_list = conditions * 3

    fig = plt.figure(figsize=(width, height))
    gs = GridSpec(3, col_number, height_ratios=[1, 3, 3], hspace=0.05)
    ax_list = [(i, j) for i in range(3) for j in range(col_number)]
    y_max = df["intensity_mean_EdU_nucleus_norm"].quantile(0.99) * 1.5
    y_min = df["intensity_mean_EdU_nucleus_norm"].quantile(0.01) * 0.8
    y_max_col = df[feature_col].quantile(0.99) * 1.5
    y_min_col = df[feature_col].quantile(0.01) * 0.8

    for i, pos in enumerate(ax_list):
        data = df1[df1[condition_col] == condition_list[i]]
        if cell_number and len(data) >= cell_number:
            data_red = pd.DataFrame(
                data.sample(n=cell_number, random_state=42)
            )
        else:
            data_red = pd.DataFrame(data)
        ax = fig.add_subplot(gs[pos[0], pos[1]])

        if i < len(conditions):
            plot_histogram(ax, i, data_red, colors)
            ax.set_title(f"{condition_list[i]}", size=6, weight="regular")
        elif i < 2 * len(conditions):
            plot_scatter(ax, i, data_red, conditions, colors)
            ax.set_ylim(y_min, y_max)
        else:
            plot_scatter_col(
                ax, i, data_red, conditions, feature_col, feature_y_lim, colors
            )
            ax.set_ylim(y_min_col, y_max_col)

        ax.grid(visible=False)

    # Set common x-axis label
    fig.text(0.5, -0.07, "norm. DNA content", ha="center", fontsize=6)
    title = f"{selector_val}_{title_str}" if selector_val else f"{title_str}"
    fig.suptitle(title, fontsize=8, weight="bold", x=0.05)
    if save and path:
        save_fig(
            fig,
            path,
            title,
            tight_layout=False,
            fig_extension="png",
        )
