URL = (
    "https://services5.arcgis.com"
    "/mnYJ21GiFTR97WFg/arcgis/rest/services"
    "/PH_masterlist/FeatureServer/0/query"
    # url query params
    "?f=json&where=1%3D1"
    "&returnGeometry=true"
    "&spatialRel=esriSpatialRelIntersects"
    "&outFields=%2A"
    "&outSR=102100"
    "&cacheHint=true"
    "&fbclid=IwAR1nboPFyAVQ5sgE0QmE31B9ZqveQcB3tUAlegIqUoqkV8057zWGHF2RsRU"
)

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

NONE_ALIAS = [
    "none",
    "",
]
