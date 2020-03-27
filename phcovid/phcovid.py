from urllib.request import urlopen
import json
from pandas.io.json import json_normalize
import re
import pandas as pd

URL = "https://services5.arcgis.com/mnYJ21GiFTR97WFg/arcgis/rest/services/PH_masterlist/FeatureServer/0/query?f=json&where=1%3D1&returnGeometry=true&spatialRel=esriSpatialRelIntersects&outFields=%2A&outSR=102100&cacheHint=true&fbclid=IwAR1nboPFyAVQ5sgE0QmE31B9ZqveQcB3tUAlegIqUoqkV8057zWGHF2RsRU"
RENAME_DICT = {
    "attributes.PH_masterl": "case_no",
    "attributes.edad": "age",
    "attributes.kasarian": "sex",
    "attributes.nationalit": "nationality",
    "attributes.residence": "residence",
    "attributes.travel_hx": "travel_history",
    "attributes.symptoms": "symptoms",
    "attributes.confirmed": "confirmation_date",
    "attributes.facility": "facility",
    "attributes.latitude": "latitude",
    "attributes.longitude": "longitude",
    "attributes.status": "status",
    "attributes.epi_link": "epi_link",
    "attributes.petsa": "date",
}

VAL_ALIAS = [
    "For validation",
    "for validation",
    "for validation",
    "For Validation",
]  # ,
NONE_ALIAS = ["none", ""]


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
    return df_aliased


if __name__ == "__main__":
    print(get_cases().head())
