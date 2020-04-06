from pandas import json_normalize
import re
import pandas as pd
import numpy as np
from urllib.error import HTTPError

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

    for df_ in [dataframe, missing]:
        df_["case_no_num"] = (
            df_["case_no"].apply(lambda x: x.split("H")[-1]).astype(np.uint64)
        )

    # Make sure both dataframe and missing are sorted based on `case_no`
    dataframe = dataframe.sort_values(by="case_no_num", ascending=True)
    missing = missing.sort_values(by="case_no_num", ascending=True)

    # Create new rows in the dataframe for the missing ids
    missing_ids_diff = list(
        set(missing.case_no_num.values).difference(dataframe.case_no_num.values)
    )
    df_missing_ids = pd.DataFrame(
        np.nan, index=range(len(missing_ids_diff)), columns=dataframe.columns
    )
    df_missing_ids["case_no_num"] = missing_ids_diff

    # Add new rows to the dataframe
    dataframe = (
        pd.concat([dataframe, df_missing_ids])
        .sort_values(by="case_no_num")
        .reset_index(drop=True)
    )

    # We supplement each of the common rows (all should be common now from the above step)
    supplement_ids = list(
        set(dataframe.case_no_num.values).intersection(missing.case_no_num.values)
    )
    targets_set = set(targets.values())
    existing_cols = list(targets_set.intersection(dataframe.columns))
    new_cols = list(targets_set.difference(existing_cols))

    # Replace target columns where gsheet data exists
    dataframe.loc[dataframe.case_no_num.isin(supplement_ids), existing_cols] = missing[
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

    try:
        df_supplemented = supplement_data(df_renamed, gsheet_target_cols)
        df_aliased = df_supplemented.replace(val_alias, np.nan).replace(
            none_alias, np.nan
        )
    except (ValueError, KeyError, IndexError, HTTPError):
        # ignore if extract from datasheet fails
        df_aliased = df_renamed

    df_aliased[["contacts", "num_contacts"]] = extract_contact_info(
        df_aliased.travel_history
    )

    df_aliased["contacts_num"] = df_aliased["contacts"].apply(
        lambda x: parse_numeric(x)
    )

    df_aliased["age"] = df_aliased["age"].astype(int)
    df_aliased["sex"] = df_aliased["sex"].astype("category")

    for col in DATE_COLS:
        if col not in df_aliased.columns:
            continue

        df_aliased[col] = df_aliased[col].apply(lambda x: fix_dates(x))

    return df_aliased


if __name__ == "__main__":
    print(get_cases().head())
