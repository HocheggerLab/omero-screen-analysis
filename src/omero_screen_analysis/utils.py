from pathlib import Path
from typing import Optional

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from matplotlib.axes import Axes
from matplotlib.figure import Figure


def save_fig(
    fig: Figure,
    path: Path,
    fig_id: str,
    tight_layout: bool = True,
    fig_extension: str = "pdf",
    resolution: int = 300,
) -> None:
    """
    Save a matplotlib figure to a file.

    Parameters
    ----------
    fig : Figure
        The figure to save.
    path : Path
        The path for saving the figure.
    fig_id : str
        The name of the saved figure.
    tight_layout : bool, optional
        Whether to use tight layout (default is True).
    fig_extension : str, optional
        The file extension for the saved figure (default is 'pdf').
    resolution : int, optional
        The resolution of the saved figure in dpi (default is 300).

    Returns
    -------
    None
        Saves the figure in the specified format.
    """

    dest = path / f"{fig_id}.{fig_extension}"
    print("Saving figure", fig_id)
    if tight_layout:
        fig.tight_layout()
    plt.savefig(
        dest,
        format=fig_extension,
        dpi=resolution,
        facecolor="white",
        edgecolor="white",
    )


def selector_val_filter(
    df: pd.DataFrame, selector_col: Optional[str], selector_val: Optional[str]
) -> Optional[pd.DataFrame]:
    """Check if selector_val is provided for selector_col and filter df"""
    if selector_col and selector_val:
        return df[df[selector_col] == selector_val].copy()
    elif selector_col:
        raise ValueError(f"selector_val for {selector_col} must be provided")
    else:
        return df.copy()


def get_repeat_points(
    df: pd.DataFrame, condition_col: str, y_col: str
) -> pd.DataFrame:
    return df.groupby(["plate_id", condition_col])[y_col].count().reset_index()


def show_repeat_points(
    df: pd.DataFrame,
    conditions: list,
    condition_col: str,
    y_col: str,
    ax: Axes,
) -> None:
    """Show repeat points"""

    sns.stripplot(
        data=df,
        x=condition_col,
        y=y_col,
        marker="o",
        size=2,
        color="gray",
        dodge=True,
        legend=False,
        order=conditions,
        ax=ax,
    )
