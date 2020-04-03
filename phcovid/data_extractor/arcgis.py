URL = "https://services5.arcgis.com/mnYJ21GiFTR97WFg/arcgis/rest/services/PH_masterlist/FeatureServer/0/query?f=json&where=1%3D1&resultType=standard&spatialRel=esriSpatialRelIntersects&outFields=%2A&outSR=102100&cacheHint=true&fbclid=IwAR1GLKbsmvS3ha9Hod61ZVgnApA2VW9dy9-RYwnYwJUYUKf97Oxj5EeVBCU"


def extract_arcgis_data():
    import json
    from urllib.request import urlopen

    return json.loads(urlopen(URL).read())
