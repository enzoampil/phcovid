from pandas.io.json import json_normalize
import re
import pandas as pd
import numpy as np

from .constants import NONE_ALIAS
from .constants import VAL_ALIAS
from .constants import RENAME_DICT
from .constants import DATE_COLS
from .constants import GSHEET_TARGET_COLUMNS
from .data_extractor import extract_arcgis_data
from .data_extractor import extract_dsph_gsheet_data


def extract_contact_info(travel_history):
    """
    Returns a dataframe containing the direct contacts of each case,
    and the number of direct contacts
    travel_history:
        Iterable from which to parse contacts of the form PHX
        ('travel_history' column from get_cases())
    """

    def get_contacts(s):
        try:
            return re.findall(r"\bPH\w+", s)
        except TypeError:
            return ""

    contacts = []
    num_contacts = []
    for case in travel_history:
        contacts_ = get_contacts(case)
        contacts.append(contacts_)
        num_contacts.append(len(contacts_))

    contact_info = pd.DataFrame({"contacts": contacts, "num_contacts": num_contacts,})
    return contact_info


def fix_dates(d):
    try:
        return pd.to_datetime(d)
    except ValueError:
        return np.nan


def parse_numeric(s):
    """
    For use in graph analysis,
    function returns list with [PHX] converted to numeric [X]
    """
    case_list = []
    for i in s:
        case_list = case_list + [i.split("H")[-1]]
    return case_list


def supplement_data(dataframe, targets):
    missing = extract_dsph_gsheet_data(target_columns=targets)
    supplement_ids = list(
        set(dataframe.case_no.values).intersection(missing.case_no.values)
    )
    targets_set = set(targets.values())
    existing_cols = list(targets_set.intersection(dataframe.columns))
    new_cols = list(targets_set.difference(existing_cols))

    # Replace target columns where gsheet data exists
    dataframe.loc[dataframe.case_no.isin(supplement_ids), existing_cols] = missing[
        existing_cols
    ]

    # Create new target columns
    dataframe[new_cols] = missing[new_cols]

    # Return adjusted columns
    return dataframe


def get_cases(
    rename_dict=RENAME_DICT,
    val_alias=VAL_ALIAS,
    none_alias=NONE_ALIAS,
    gsheet_target_cols=GSHEET_TARGET_COLUMNS,
):
    """
    Returns cleaned data from DOH COVID for PH
    https://www.facebook.com/notes/wilson-chua/working-with-doh-covid-data/2868993263159446/
    """
    raw = extract_arcgis_data()
    df = json_normalize(raw["features"])
    df_renamed = df[rename_dict.keys()].rename(columns=rename_dict)
    df_supplemented = supplement_data(df_renamed, gsheet_target_cols)
    df_aliased = df_supplemented.replace(val_alias, "for_validation").replace(
        none_alias, np.nan
    )
    df_aliased[["contacts", "num_contacts"]] = extract_contact_info(
        df_aliased.travel_history
    )

    df_aliased["case_no_num"] = (
        df_aliased["case_no"].apply(lambda x: x.split("H")[-1]).astype(int)
    )
    df_aliased["contacts_num"] = df_aliased["contacts"].apply(
        lambda x: parse_numeric(x)
    )

    for col in DATE_COLS:
        df_aliased[col] = df_aliased[col].apply(lambda x: fix_dates(x))

    return df_aliased


if __name__ == "__main__":
    print(get_cases().head())
