import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from omero_screen_analysis.utils import save_fig


def normalize_cell_counts(df, agent1, agent2):
    df1 = (
        df.groupby(["well", agent1, agent2])
        .size()
        .reset_index(name="cell_count")
    )
    max_cells = df1["cell_count"].max()
    min_cells = df1["cell_count"].min()
    df1["normalized_cell_count"] = (max_cells - df1["cell_count"]) / (
        max_cells - min_cells
    )
    # Create pivot table with the new column name
    df_pivot = df1.pivot(
        index=agent1, columns=agent2, values="normalized_cell_count"
    )
    return df1, df_pivot.astype(float)


def bliss_analysis(df, agent1, agent2):
    _, df_pivot = normalize_cell_counts(df, agent1, agent2)

    # Calculate expected effects
    effect_agent1 = df_pivot.loc[:, 0].astype(float)  # Effect of agent1 alone
    effect_agent2 = df_pivot.loc[0, :].astype(float)  # Effect of agent2 alone

    # Create expected combination effect matrix
    expected = pd.DataFrame(
        index=df_pivot.index, columns=df_pivot.columns, dtype=float
    )
    for i in df_pivot.index:
        for j in df_pivot.columns:
            if i == 0 or j == 0:
                expected.loc[i, j] = df_pivot.loc[i, j]
            else:
                expected.loc[i, j] = (
                    effect_agent1[i]
                    + effect_agent2[j]
                    - (effect_agent1[i] * effect_agent2[j])
                )

    # Calculate synergy scores and ensure numeric
    synergy_scores = (df_pivot - expected).astype(float)

    # Replace any infinite values with NaN and fill NaN with 0
    synergy_scores = synergy_scores.replace([np.inf, -np.inf], np.nan)
    synergy_scores = synergy_scores.fillna(0)

    return synergy_scores


def hsa_analysis(df, agent1, agent2):
    df1, df_pivot = normalize_cell_counts(df, agent1, agent2)
    max_single_agent = pd.DataFrame(
        index=df_pivot.index, columns=df_pivot.columns
    )
    for agent_conc in df1[agent1].unique():
        for ad1208_conc in df1[agent2].unique():
            max_single_agent.loc[agent_conc, ad1208_conc] = max(
                df_pivot.loc[agent_conc, 0], df_pivot.loc[0, ad1208_conc]
            )
    max_single_agent = max_single_agent.astype(float)
    return df_pivot - max_single_agent


def plot_synergies(df, agent1, agent2, title=None, save=False, path=None):
    if len(df.cell_line.unique()) > 1:
        raise ValueError("More than one cell line in the data")
    cell_line = df.cell_line.unique()[0]
    df_bliss = bliss_analysis(df, agent1, agent2)
    df_hsa = hsa_analysis(df, agent1, agent2)
    _, df_pivot = normalize_cell_counts(df, agent1, agent2)
    fig, ax = plt.subplots(ncols=3, figsize=(15, 6))
    sns.heatmap(
        df_pivot,
        ax=ax[0],
        annot=True,
        cmap="viridis",
        cbar_kws={"label": "Cell Count"},
    )
    ax[0].set_title("Observed Normalized Cell Counts", size=7)
    ax[0].set_xlabel(agent2)
    ax[0].set_ylabel(agent1)
    sns.heatmap(
        df_hsa,
        annot=True,
        cmap="RdYlBu_r",
        vmin=-1,  # Set minimum value
        vmax=1,  # Set maximum value
        center=0,
        cbar_kws={"label": "HSA Synergy Score"},
        ax=ax[1],
    )
    ax[1].set_title("HSA Synergy Scores", size=8, weight="regular")
    ax[1].set_xlabel(agent2)
    ax[1].set_ylabel(agent1)

    # Second heatmap: Bliss synergy scores
    sns.heatmap(
        df_bliss,
        annot=True,
        cmap="coolwarm",
        vmin=-1,  # Set minimum value
        vmax=1,  # Set maximum value
        center=0,
        cbar_kws={"label": "Bliss Synergy Score"},
        ax=ax[2],
    )
    ax[2].set_title("Bliss Synergy Scores", size=8, weight="regular")
    ax[2].set_xlabel(agent2)
    ax[2].set_ylabel(agent1)
    if title is None:
        title = f"{agent1} and {agent2} Synergy Analysis in {cell_line}"
    fig.suptitle(title, size=10, weight="bold", x=0.13)

    plt.tight_layout()
    if save and path:
        save_fig(fig, path, title)
    elif save:
        raise ValueError("Path must be provided if save is True")
    else:
        return fig
