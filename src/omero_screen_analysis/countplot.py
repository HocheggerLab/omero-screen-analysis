from pathlib import Path
from typing import Optional

import matplotlib.pyplot as plt
from matplotlib.axes import Axes
import pandas as pd
import seaborn as sns

from omero_screen_analysis.stats import set_significance_marks
from omero_screen_analysis.utils import (
    save_fig,
    selector_val_filter,
    show_repeat_points,
)

current_dir = Path(__file__).parent
style_path = (current_dir / "../../hhlab_style01.mplstyle").resolve()
plt.style.use(style_path)
prop_cycle = plt.rcParams["axes.prop_cycle"]
COLORS = prop_cycle.by_key()["color"]
pd.options.mode.chained_assignment = None

height = 3 / 2.54  # 2 cm


def norm_count(
    df: pd.DataFrame, norm_control: str, condition: str = "condition"
) -> pd.DataFrame:
    """Normalize count by control condition"""
    grouped = (
        df.groupby(["plate_id", condition])["experiment"].count().reset_index()
    )
    pivot_df = grouped.pivot(
        index="plate_id", columns=condition, values="experiment"
    )
    normalized_df = pivot_df.div(pivot_df[norm_control], axis=0)
    return normalized_df.reset_index().melt(
        id_vars="plate_id", value_name="normalized_count"
    )


def count_plot(
    df: pd.DataFrame,
    norm_control: str,
    conditions: list[str],
    condition_col: str = "condition",
    selector_col: Optional[str] = "cell_line",
    selector_val: Optional[str] = None,
    title: Optional[str] = None,
    colors: list[str] = COLORS,
    save: bool = True,
    path: Optional[Path] = None,
    ax: Optional[Axes] = None,
) -> None:
    """Plot normalized counts"""
    fig, ax = (
        plt.subplots(figsize=(height, height)) if ax is None else (None, ax)
    )
    df1 = selector_val_filter(df, selector_col, selector_val)
    assert df1 is not None
    counts = norm_count(df1, norm_control, condition=condition_col)
    sns.barplot(
        data=counts,
        x=condition_col,
        y="normalized_count",
        order=conditions,
        color=colors[-1],
        ax=ax,
    )
    ax.set_xticks(range(len(conditions)))  #
    ax.set_xticklabels(conditions, rotation=45, ha="right")

    show_repeat_points(
        counts, conditions, condition_col, "normalized_count", ax
    )
    if df1.plate_id.nunique() >= 3:
        set_significance_marks(
            ax,
            counts,
            conditions,
            condition_col,
            "normalized_count",
            ax.get_ylim()[1],
        )
    ax.set_xlabel("")
    if not title:
        title = f"counts {selector_val}"
    file_name = title.replace(" ", "_")
    fig.suptitle(title, fontsize=7, weight="bold", x=0, y=1.05, ha="left")
    if fig and save and path:
        save_fig(
            fig,
            path,
            file_name,
            tight_layout=False,
            fig_extension="pdf",
        )
