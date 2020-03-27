def test_get_cases_headers():
    from phcovid import get_cases
    from phcovid import RENAME_DICT

    headers = list(RENAME_DICT.values())

    # include contacts and num_contacts headers
    headers += [
        "contacts",
        "num_contacts",
    ]

    cases = get_cases()

    for col in cases.columns:
        assert col in headers
