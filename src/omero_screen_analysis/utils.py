from pathlib import Path

import matplotlib.pyplot as plt
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
