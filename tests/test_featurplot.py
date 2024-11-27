import matplotlib.pyplot as plt

from omero_screen_analysis.featureplot import feature_plot

conditions = ["NT", "SCR"]

def test_feature_plot(filtered_data):
    feature_plot(
        df=filtered_data,
        feature="intensity_mean_p21_nucleus",
        conditions=conditions,
        selector_col="cell_line",
        selector_val="RPE-1_WT",
        title="p21",
        save=False,
        )
    plt.close("all")

