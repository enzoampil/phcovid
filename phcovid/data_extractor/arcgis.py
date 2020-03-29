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


def extract_arcgis_data():
    import json
    from urllib.request import urlopen

    return json.loads(urlopen(URL).read())
