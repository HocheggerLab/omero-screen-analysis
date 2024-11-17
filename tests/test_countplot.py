import matplotlib.pyplot as plt

from omero_screen_analysis.countplot import count_plot, norm_count


def test_norm_count(filtered_data):
    df = norm_count(filtered_data, norm_control="NT")
    assert df["normalized_count"].sum() == 2.0


def test_count_fig(filtered_data):
    count_plot(
        filtered_data,
        norm_control="NT",
        conditions=["NT", "SCR", "CCNA2", "CDK4"],
        selector_col="cell_line",
        selector_val="RPE-1_WT",
        title_str="test",
        save=False,
    )
    plt.close("all")
