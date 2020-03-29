from pandas.io.json import json_normalize
import re
import pandas as pd
import numpy as np

from .constants import NONE_ALIAS
from .constants import VAL_ALIAS
from .constants import RENAME_DICT
from .constants import DATE_COLS
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


def attach_target(current, data, headers):
    search_res = [d for d in data if current[headers[0]] == d[0]]
    if not len(search_res):
        # use data from original dataset if not none
        if current[headers[1]]:
            return current[headers[1]]

        return "none"

    # use data from supplement dataset
    return search_res[-1][1]


def parse_numeric(s):
    """
    For use in graph analysis,
    function returns list with [PHX] converted to numeric [X]
    """
    case_list = []
    for i in s:
        case_list = case_list + [i.split("H")[-1]]
    return case_list


def extract_supplement_data(dataframe, targets):
    missing = extract_dsph_gsheet_data(target_columns=targets)
    columns = {}

    for target in targets[1:]:
        columns[target] = dataframe[["case_no", target]].apply(
            lambda x: attach_target(
                x,
                [(d[0], d[targets.index(target)]) for d in missing],
                ["case_no", target],
            ),
            axis=1,
        )

    return pd.DataFrame(columns)


def get_cases(rename_dict=RENAME_DICT, val_alias=VAL_ALIAS, none_alias=NONE_ALIAS):
    """
    Returns cleaned data from DOH COVID for PH
    https://www.facebook.com/notes/wilson-chua/working-with-doh-covid-data/2868993263159446/
    """
    raw = extract_arcgis_data()
    df = json_normalize(raw["features"])
    df_renamed = df[rename_dict.keys()].rename(columns=rename_dict)
    df_aliased = df_renamed.replace(val_alias, "for_validation").replace(
        none_alias, "none"
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

    df_aliased[["status", "symptoms"]] = extract_supplement_data(
        df_aliased,
        targets=["case no.", "status", "symptoms"]
    )

    return df_aliased


if __name__ == "__main__":
    print(get_cases().head())
