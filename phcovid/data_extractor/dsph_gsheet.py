import re
import pandas as pd

URL = (
    "https://docs.google.com"
    "/spreadsheets/u/0/d"
    "/16g_PUxKYMC0XjeEKF6FPUBq2-pFgmTkHoj5lbVrGLhE"
    "/htmlview"
)

GSHEET_ID = {"case no.": "case_no"}


def _extract_by_targets(headers, data, targets):
    valid_idx = []
    for col in targets:
        valid_idx += [headers.index(col)]

    return _clean_html(soup_data=data, valid_idx=valid_idx)


def _clean_data_value(data):
    if isinstance(data, str) and bool(re.match(r"PH\d+", data)):
        case_no = data.split("PH")[-1]
        return "".join(["PH", case_no.lstrip("0")])

    if data is None or data == "":
        return "none"

    if data.lower().strip() == "for validation":
        return "for_validation"

    return data


def _clean_html(soup_data=None, headers=None, valid_idx=[]):
    if headers:
        soup_data = [headers]

    rows = [row.find_all("td") for row in soup_data]
    output = []
    for row in rows:
        if row[0].string is None:
            continue

        # extract all if empty valid_idx; else only extract if in valid_idx
        if valid_idx == []:
            output += [[_clean_data_value(td.string) for td in row]]
            continue

        output += [[_clean_data_value(row[idx].string) for idx in valid_idx]]

    if headers:
        return [o.lower() for o in output[-1]]

    return output


def extract_dsph_gsheet_data(target_columns):
    """
    Returns google sheets worksheet in pd.DataFrame format
    """
    from urllib.request import urlopen
    from bs4 import BeautifulSoup

    gsheet_html = urlopen(URL).read()
    soup = BeautifulSoup(gsheet_html, features="html.parser")

    # get from first sheet -- should work as long as `Cases` is the default tab
    soup = soup.find(id="0")

    # select table rows
    rows = soup.select("tbody > tr")
    headers = _clean_html(headers=rows[0])
    id_targets = list(GSHEET_ID.keys()) + list(target_columns.keys())
    data = _extract_by_targets(headers, rows[1:], targets=id_targets)
    id_targets_standard = list(GSHEET_ID.values()) + list(target_columns.values())
    df = pd.DataFrame(data, columns=id_targets_standard)

    return df
