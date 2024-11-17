import matplotlib.pyplot as plt

from omero_screen_analysis.cellcycleplot import cc_phase, cellcycle_plot


def test_cc_phase(filtered_data):
    df_cc = cc_phase(filtered_data)
    assert df_cc.shape == (20, 5)
    assert df_cc.percent.mean() == 20.0


def test_cellcycle_plots(filtered_data):
    conditions = ["NT", "SCR"]
    cellcycle_plot(
        df=filtered_data,
        conditions=conditions,
        selector_col="cell_line",
        selector_val="RPE-1_WT",
        condition_col="condition",
        save=False,
    )
    plt.close("all")
