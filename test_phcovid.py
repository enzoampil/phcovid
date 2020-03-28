import pandas as pd
from phcovid import get_cases


def test_get_cases():
    df = get_cases()
    assert isinstance(df, pd.DataFrame)


def test_arcgis_extract():
    from phcovid.data_extractor import extract_arcgis_data
    assert extract_arcgis_data() != {}


def test_dsph_gsheet_extraction():
    from phcovid.data_extractor import extract_dsph_gsheet_data
    assert extract_dsph_gsheet_data() != []
