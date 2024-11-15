from pathlib import Path

import pandas as pd
import pytest


@pytest.fixture
def cell_cycle_data():
    """Load real cell cycle data for testing

    Dataset properties:
    - Contains conditions: ['DMSO', 'Drug1', ...]
    - Features: DAPI, EdU intensities
    - Cell cycle phases
    """
    data_path = Path(__file__).parent /"example_data.csv"
    return pd.read_csv(data_path)


@pytest.fixture
def filtered_data(cell_cycle_data):
    """Pre-filtered dataset with specific conditions"""
    conditions = ["NT", "SCR"]
    return cell_cycle_data[cell_cycle_data.condition.isin(conditions)]
