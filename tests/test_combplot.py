import matplotlib.pyplot as plt

from omero_screen_analysis.combplot import combplot


def test_combplot_with_real_data(filtered_data, tmp_path):
    """Test combplot using real cell cycle data"""
    conditions = ["NT", "SCR"]
    feature_col = "intensity_mean_p21_nucleus"

    combplot(
        df=filtered_data,
        conditions=conditions,
        feature_col=feature_col,
        feature_y_lim=8000,
        selector_val="RPE-1_WT",
        title_str="test",
        save=False,
    )
    plt.close("all")
