# from pathlib import Path
# from typing import Optional

# import matplotlib.pyplot as plt
# import pandas as pd
# import seaborn as sns
# from matplotlib import ticker
# from matplotlib.axes import Axes
# from matplotlib.gridspec import GridSpec


# from omero_screen_analysis import (
#     count_plot,
#     feature_plot,
#     histogram_plot,
#     scatter_plot,
#     scatter_plot_feature,
#     cellcycle_plot,
# )
# from omero_screen_analysis.utils import save_fig, selector_val_filter

# def if_analysis_plot(
#     df: pd.DataFrame,
#     conditions: list[str],
#     feature_col: str,
#     feature_y_lim: float,
#     condition_col: str = "condition",
#     selector_col: Optional[str] = "cell_line",
#     selector_val: Optional[str] = None,
#     title_str: str | None = None,
#     cell_number: int | None = None,
#     colors: list[str] = COLORS,
#     save: bool = True,
#     path: Path | None = None,
# ) -> None:
#     """
    
#     """
#     col_number = len(conditions)
#     df1 = selector_val_filter(df, selector_col, selector_val)
#     assert df1 is not None  # tells type checker df1 is definitely not None
#     condition_list = conditions * 3

#     fig = plt.figure(figsize=(width, height))
#     # - The right spanning column has a ratio of condition_cols / 2.
#     width_ratios = [1] * col_number + [col_number / 2]
#     # Define height ratios for the three rows
#     height_ratios = [1, 3, 3]
#     gs = GridSpec(3, col_number, height_ratios=height_ratios, width_ratios=width_ratios, hspace=0.05)
    
#     ax_list = [(i, j) for i in range(3) for j in range(col_number)]
#     y_max = df["intensity_mean_EdU_nucleus_norm"].quantile(0.99) * 1.5
#     y_min = df["intensity_mean_EdU_nucleus_norm"].quantile(0.01) * 0.8
#     y_max_col = df[feature_col].quantile(0.99) * 1.5
#     y_min_col = df[feature_col].quantile(0.01) * 0.8

#     for i, pos in enumerate(ax_list):
#         data = df1[df1[condition_col] == condition_list[i]]
#         if cell_number and len(data) >= cell_number:
#             data_red = pd.DataFrame(
#                 data.sample(n=cell_number, random_state=42)
#             )
#         else:
#             data_red = pd.DataFrame(data)
#         ax = fig.add_subplot(gs[pos[0], pos[1]])

#         if i < len(conditions):
#             histogram_plot(ax, i, data_red, colors)
#             ax.set_title(f"{condition_list[i]}", size=6, weight="regular")
#         elif i < 2 * len(conditions):
#             scatter_plot(ax, i, data_red, conditions, colors)
#             ax.set_ylim(y_min, y_max)
#         else:
#             scatter_plot_feature(
#                 ax, i, data_red, conditions, feature_col, feature_y_lim, colors
#             )
#             ax.set_ylim(y_min_col, y_max_col)

#         ax.grid(visible=False)
#     ax = fig.add_subplot(gs[-1, :])
#     cellcycle_plot(
#         df=df,
#         conditions=conditions,
#         condition_col=condition_col,
#         selector_col=selector_col,
#         selector_val=selector_val,
#         title=title_str,
#         save=False,
#         ax=ax
#     )

#     # Set common x-axis label
#     fig.text(0.5, -0.07, "norm. DNA content", ha="center", fontsize=6)
#     title = f"{selector_val}_{title_str}" if selector_val else f"{title_str}"
#     fig.suptitle(title, fontsize=8, weight="bold", x=0.1)
#     if save and path:
#         save_fig(
#             fig,
#             path,
#             title,
#             tight_layout=False,
#             fig_extension="png",
#         )
