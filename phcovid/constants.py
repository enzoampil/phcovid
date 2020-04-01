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


# Mapping between gsheet column names to be added and their corresponding name in the final dataframe
GSHEET_TARGET_COLUMNS = {
    "status": "status",
    "symptoms": "symptoms",
    "date of announcement to the public": "announcement_date",
    "sex": "sex",
    "age": "age",
    "nationality": "nationality",
    "residence in the philippines": "residence",
    "date of lab confirmation": "confirmation_date",
    "admission / consultation": "facility",
    "date of final status (recovered/expired)": "final_status_date",
}


DATE_COLS = ["confirmation_date", "date", "announcement_date", "final_status_date"]

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
