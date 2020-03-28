from urllib.request import urlopen
import json
from pandas.io.json import json_normalize
import re
import pandas as pd
import numpy as np

from .constants import URL
from .constants import NONE_ALIAS
from .constants import VAL_ALIAS
from .constants import RENAME_DICT
from .constants import DATE_COLS


def extract_contact_info(travel_history):
    """
    Returns a dataframe containing the direct contacts of each case, and the number of direct contacts
    travel_history:
        Iterable from which to parse contacts of the form PHX ('travel_history' column from get_cases())
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

    contact_info = pd.DataFrame({"contacts": contacts, "num_contacts": num_contacts})
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


def get_cases(
    url=URL, rename_dict=RENAME_DICT, val_alias=VAL_ALIAS, none_alias=NONE_ALIAS
):
    """
    Returns cleaned data from DOH COVID for PH (https://www.facebook.com/notes/wilson-chua/working-with-doh-covid-data/2868993263159446/)
    """
    raw = json.loads(urlopen(url).read())
    df = json_normalize(raw["features"])
    df_renamed = df[rename_dict.keys()].rename(columns=rename_dict)
    df_aliased = df_renamed.replace(val_alias, "for_validation").replace(
        none_alias, "none"
    )
    df_aliased[["contacts", "num_contacts"]] = extract_contact_info(
        df_aliased.travel_history
    )

    df["case_no_num"] = df["case_no"].apply(lambda x: x.split("H")[-1]).astype(int)
    df["contacts_num"] = df["contacts"].apply(lambda x: parse_numeric(x))

    for col in DATE_COLS:
        df_aliased[col] = df_aliased[col].apply(lambda x: fix_dates(x))

    return df_aliased


if __name__ == "__main__":
    print(get_cases().head())
