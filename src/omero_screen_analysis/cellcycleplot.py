from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from omero_screen_analysis.stats import set_significance_marks
from omero_screen_analysis.utils import (
    save_fig,
    selector_val_filter,
    show_repeat_points,
)

# Define figure size in inches
width = 10 / 2.54  # 10 cm
height = 7 / 2.54  # 4 cm


current_dir = Path(__file__).parent
style_path = (current_dir / "../../hhlab_style01.mplstyle").resolve()
plt.style.use(style_path)
prop_cycle = plt.rcParams["axes.prop_cycle"]
COLORS = prop_cycle.by_key()["color"]
pd.options.mode.chained_assignment = None


def cc_phase(df: pd.DataFrame, condition: str = "condition") -> pd.DataFrame:
    """Calculate the percentage of cells in each cell cycle phase for each condition"""
    return (
        (
            df.groupby(["plate_id", "cell_line", condition, "cell_cycle"])[
                "experiment"
            ].count()
            / df.groupby(["plate_id", "cell_line", condition])[
                "experiment"
            ].count()
            * 100
        )
        .reset_index()
        .rename(columns={"experiment": "percent"})
    )


def cellcycle_plot(
    df: pd.DataFrame,
    conditions: list[str],
    condition_col="condition",
    selector_col: str | None = "cell_line",
    selector_val: str | None = None,
    title: str | None = None,
    colors: list[str] = COLORS,
    save: bool = True,
    path: Path | None = None,
) -> None:
    """Plot the cell cycle phases for each condition"""
    print(f"Plotting cell cycle quantifications for {selector_val}")
    df1 = selector_val_filter(df, selector_col, selector_val)
    assert df1 is not None
    df1 = cc_phase(df, condition=condition_col)
    fig, ax = plt.subplots(2, 2, figsize=(height * 0.7, height))
    ax_list = [ax[0, 0], ax[0, 1], ax[1, 0], ax[1, 1]]
    cellcycle = ["G1", "S", "G2/M", "Polyploid"]
    for i, phase in enumerate(cellcycle):
        axes = ax_list[i]
        df_phase = df1[
            (df1.cell_cycle == phase) & (df1[condition_col].isin(conditions))
        ]
        # y_max = df_phase["percent"].max() * 1.2

        sns.barplot(
            data=df_phase,
            x=condition_col,
            y="percent",
            color=colors[i + 1],
            order=conditions,
            ax=axes,
        )

        show_repeat_points(
            df_phase, conditions, condition_col, "percent", axes
        )
        if df1.plate_id.nunique() >= 3:
            set_significance_marks(
                axes, df_phase, conditions, "percent", axes.get_ylim()[1]
            )
        axes.set_title(f"{phase}", fontsize=6, pad=0)
        if i in [1, 3]:
            axes.set_ylabel(None)
        if i in [0, 1]:
            axes.set_xticklabels([])
        else:
            # Set the tick positions
            axes.set_xticks(range(len(conditions)))  #
            axes.set_xticklabels(conditions, rotation=45, ha="right")
        axes.set_xlabel(None)
        # Get the y-max for positioning significance markers
    if not title:
        title = f"Cellcycle Analysis {selector_val}"
    fig.suptitle(title, fontsize=8, weight="bold", x=0.3)
    fig_title = title.replace(" ", "_")
    if save and path:
        save_fig(
            fig,
            path,
            fig_title,
            tight_layout=False,
            fig_extension="pdf",
        )
