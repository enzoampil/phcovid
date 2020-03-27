import numpy as np
import pandas as pd
import matplotlib
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
        # Function removes empty/invalid dates and returns date_time dtype for valid dates.
        # Once data cleaning in get_cases() is finalized, we can depracate this fucntion and section
        try:
            date = pd.to_datetime(d)
            return date
        except ValueError:
            return np.nan

    case_dates = df[date_col]
    case_count = pd.DataFrame(case_dates[~case_dates.isnull()].unique())
    case_count.rename(columns={0: "date"}, inplace=True)
    # sort values on date
    case_count = case_count.sort_values("date", ascending = True)

    for row in case_count.itertuples():
        current_date = getattr(row, "date")
        index = getattr(row, "Index")

        # column 'case_count' stores cumulative number of cases less than specific date.
        case_count.loc[index, "case_count"] = len(df[df[date_col] <= current_date])

    # get values for first and latest confirmed date
    first_case = str(min(case_count["date"])).split(" ")[0]
    latest_case = str(max(case_count["date"])).split(" ")[0]
    

    # convert dates column to date time for better plot representation
    case_count["date"] = case_count["date"].apply(lambda x: pd.to_datetime(x))
    plt.figure(figsize=(10, 6))

    # plot
    plt.plot_date(matplotlib.dates.date2num(case_count["date"]), case_count["case_count"])
