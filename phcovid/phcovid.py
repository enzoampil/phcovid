from urllib.request import urlopen
import json
from pandas.io.json import json_normalize

URL = 'https://services5.arcgis.com/mnYJ21GiFTR97WFg/arcgis/rest/services/PH_masterlist/FeatureServer/0/query?f=json&where=1%3D1&returnGeometry=true&spatialRel=esriSpatialRelIntersects&outFields=%2A&outSR=102100&cacheHint=true&fbclid=IwAR1nboPFyAVQ5sgE0QmE31B9ZqveQcB3tUAlegIqUoqkV8057zWGHF2RsRU'
RENAME_DICT = {
    'attributes.PH_masterl': 'case_no',
    'attributes.edad': 'age',
    'attributes.kasarian': 'sex',
    'attributes.nationalit': 'nationality',
    'attributes.residence': 'residence',
    'attributes.travel_hx': 'travel_history',
    'attributes.symptoms': 'symptoms',
    'attributes.confirmed': 'confirmation_date',
    'attributes.facility': 'facility',
    'attributes.latitude': 'latitude',
    'attributes.longitude': 'longitude',
    'attributes.status': 'status',
    'attributes.epi_link': 'epi_link',
    'attributes.petsa': 'date',
}

VAL_ALIAS = ['For validation', 'for validation', 'for validation', 'For Validation'] #, 
NONE_ALIAS = ['none', '']

def get_cases(url=URL, rename_dict=RENAME_DICT, val_alias=VAL_ALIAS, none_alias=NONE_ALIAS):
    raw = json.loads(urlopen(url).read())
    df = json_normalize(raw['features'])
    df_renamed = df[rename_dict.keys()].rename(columns=rename_dict)
    df_aliased = df_renamed.replace(val_alias, 'for_validation').replace(none_alias, 'none')
    return df_aliased

if __name__ == '__main__':
    print(get_cases().head())