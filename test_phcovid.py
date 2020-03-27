import pandas as pd
from phcovid import get_cases

def test_get_cases():
    df = get_cases()
    assert isinstance(df, pd.DataFrame)