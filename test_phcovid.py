import pandas as pd
from phcovid import get_cases
from phcovid import get_case_network

def test_get_cases():
    df = get_cases()
    assert isinstance(df, pd.DataFrame)

def test_get_case_network():
    df = get_cases()
    network_df = get_case_network(df)
    assert isinstance(network_df, pd.DataFrame)