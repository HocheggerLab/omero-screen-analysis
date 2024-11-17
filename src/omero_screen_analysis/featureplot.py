from pathlib import Path
from typing import Optional

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from omero_screen_analysis.stats import set_significance_marks
from omero_screen_analysis.utils import (
    save_fig,
    select_datapoints,
    selector_val_filter,
    show_repeat_points,
)

height = 3.5 / 2.54  # 2 cm
current_dir = Path(__file__).parent
style_path = (current_dir / "../../hhlab_style01.mplstyle").resolve()
plt.style.use(style_path)
prop_cycle = plt.rcParams["axes.prop_cycle"]
COLORS = prop_cycle.by_key()["color"]




def feature_plot(
    df: pd.DataFrame,
    feature: str,
    conditions: list[str],
    condition_col: str = "condition",
    selector_col: str = "cell_line",
    selector_val: str = "",
    title_str: str = "",
    colors=COLORS,
    save: bool = True,
    path: Optional[Path] = None,
):
    """Plot a feature plot"""
    df_filtered = selector_val_filter(df, selector_col, selector_val)
    assert df_filtered is not None, "No data found"
    fig, ax = plt.subplots(figsize=(height, height))
    sns.boxenplot(
        data=df_filtered,
        x="condition",
        y=feature,
        color=colors[-1],
        order=conditions,
        showfliers=False,
        ax=ax,
    )
    color_list = [colors[2], colors[3], colors[4]]
    plate_ids = df_filtered.plate_id.unique()
    df_sampled = select_datapoints(df_filtered, conditions, condition_col)
    for idx, plate_id in enumerate(plate_ids):
        plate_data = df_sampled[df_sampled.plate_id == plate_id]
        sns.swarmplot(
            data=plate_data,
            x="condition",
            y=feature,
            color=color_list[idx],  # Use color from palette
            alpha=1,
            size=2,
            edgecolor="white",
            dodge=True,
            order=conditions,
            ax=ax,
        )
    if len(df.plate_id.unique()) >=3:
        df_median = (
            df_filtered.groupby(["plate_id", condition_col])[feature]
            .median()
            .reset_index()
            )
        show_repeat_points(df_median, conditions, condition_col, feature, ax)
        set_significance_marks(
            ax, df_median, conditions, feature, ax.get_ylim()[1]
        )
    ax.set_ylabel(feature)
    ax.set_xlabel("")
    ax.set_xticks(range(len(conditions)))
    ax.set_xticklabels(conditions, rotation=45, ha="right")
    match (title_str, selector_val):
        case ("", ""):
            title = feature
        case (_, ""):
            title = f"{title_str} {selector_val}"
        case ("", _):
            title = f"{feature} {selector_val}"
        case (_, _):
            title = f"{title_str} {selector_val}"
    ax.set_title(title, fontsize=8, loc="left", pad=10)
    file_name = title.replace(" ", "_")
    if save and path:
        save_fig(
            fig,
            path,
            file_name,
            tight_layout=False,
            fig_extension="pdf",
        )

