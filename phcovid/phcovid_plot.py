import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def get_case_plot(df, date_col="confirmation_date"):
    """
    This function a.) plots the growth of cases in the given df
    and prints the date of first and latest confirmed case.
    
    df:
        full extract or slice of original dataframe from get_cases()
    date_col:
        column name of date attribute
        current decision is to use column 'confirmation date.'
        since column 'date' has more missing values. 
    """

    def get_date_part(d):
        # Function removes empty/invalid dates
        # Once data cleaning in get_cases() is finalized, we can depracate this fucntion and section
        try:
            date = pd.to_datetime(d)
            return d
        except ValueError:
            return np.nan

    case_dates = df[date_col]
    case_dates = case_dates.apply(lambda x: get_date_part(x))
    case_count = pd.DataFrame(case_dates[~case_dates.isnull()].unique())
    case_count.rename(columns={0: "date"}, inplace=True)

    for row in case_count.itertuples():
        current_date = getattr(row, "date")
        index = getattr(row, "Index")

        # column 'case_count' stores number of cases in that specific date.
        case_count.loc[index, "case_count"] = len(df[df[date_col] == current_date])

        # create cumulative sum of case_count
        if index == 0:
            case_count.loc[index, "case_count"] = 0
        else:
            case_count.loc[index, "case_count"] += case_count.loc[
                index - 1, "case_count"
            ]

    # print first and latest confirmed date
    print(
        "First Confirmed Case: ",
        str(min(pd.to_datetime(case_count["date"]))).split(" ")[0],
    )
    print(
        "Latest Confirmed Case: ",
        str(max(pd.to_datetime(case_count["date"]))).split(" ")[0],
    )

    # plot
    plt.plot(case_count["date"], case_count["case_count"])
