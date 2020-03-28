URL = (
    "https://docs.google.com"
    "/spreadsheets/u/0/d"
    "/16g_PUxKYMC0XjeEKF6FPUBq2-pFgmTkHoj5lbVrGLhE"
    "/htmlview"
)

TARGET_COLUMNS = (
    "case no.",
    "status",
    "symptoms",
)


def _extract_by_targets(headers, data, targets):
    valid_idx = []
    for col in targets:
        valid_idx += [headers.index(col)]

    return _clean_html(soup_data=data, valid_idx=valid_idx)


def _clean_data_value(data):
    if data is None or data == "":
        return "none"

    if data.lower().strip() == "for validation":
        return "for_validation"

    return data


def _clean_html(soup_data=None, headers=None, valid_idx=[]):
    if headers:
        soup_data = [headers]

    rows = [row.find_all("td") for row in soup_data]
    output = [
        [
            _clean_data_value(td.string)
            for idx, td in enumerate(row)
            # extract all if empty valid_idx; else only extract if in valid_idx
            if not len(valid_idx) or idx in valid_idx
        ]
        for row in rows
        if row[0].string is not None
    ]

    if headers:
        return [o.lower() for o in output[-1]]

    return output


def extract_dsph_gsheet_data(target_columns=TARGET_COLUMNS):
    from urllib.request import urlopen
    from bs4 import BeautifulSoup
    gsheet_html = urlopen(URL).read()
    soup = BeautifulSoup(gsheet_html, features="html.parser")

    # get from first sheet -- should work as long as `Cases` is the default tab
    soup = soup.find(id="0")

    # select table rows
    rows = soup.select("tbody > tr")
    headers = _clean_html(headers=rows[0])
    data = _extract_by_targets(
        headers,
        rows[1:],
        targets=target_columns
    )

    return data
