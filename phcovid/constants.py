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
    # "casecode": "case_no",
    "age": "age",
    "sex": "sex",
    "location": "residence",
    "daterepconf": "confirmation_date",
    "latitude": "latitude",
    "longitude": "longitude",
    "removaltype": "status",
    "datereprem": "date",
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
