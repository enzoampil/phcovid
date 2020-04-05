# phcovid

[![Build Status](https://travis-ci.com/enzoampil/phcovid.svg?branch=master)](https://travis-ci.com/github/enzoampil/phcovid)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg )](https://raw.githubusercontent.com/enzoampil/phcovid/master/LICENSE)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

A `Python` library that allows extraction of pre-processed data for COVID-19 in the Philippines. The goal of the library is to make data accessible so that we do more with analyses and less on cleaning.

## Get PH COVID data in only two lines of code!

Using `phcovid` is as simple is importing it and calling `get_cases`!

```python
from phcovid import get_cases
df = get_cases()
print(get_cases().iloc[:5, :5])

#  case_no  age     sex nationality    residence
#0     PH1   38  Female     Chinese         None
#1     PH2   44    Male     Chinese         None
#2     PH3   60  Female     Chinese         None
#3     PH4   48    Male    Filipino  Taguig City
#4     PH5   62    Male    Filipino        Rizal
```

## Using the library

The package is installable through Python `pip` with the assumption that you're using `Python 3`.

```bash
pip install phcovid
```

### Cases

The `get_cases` function will take data stated from the [sources](#sources) that this library is integrated with.

```python
from phcovid import get_cases
df = get_cases()
```

The base of the data will come from the [DOH dataset](https://ncovtracker.doh.gov.ph). But with the increasing number of cases, some columns from the base dataset is incomplete. To remedy this, columns are completed from a crowdsourced dataset from the [Data Science Philippines curated COVID-19 dataset](https://www.facebook.com/groups/datasciencephilippines/permalink/909066746213492/) or DSPH GSheet Dataset. Below is the breakdown of the columns and where they're coming from.

| Column | Source |
| --- | --- |
| case_no | DOH |
| travel_history | DOH |
| latitude | DOH |
| longitude | DOH |
| epi_link | DOH |
| date | DOH |
| case_no_num | DOH |
| contacts | DOH |
| num_contacts | DOH |
| contacts_num | DOH |
| age | DSPH GSheet |
| sex | DSPH GSheet |
| nationality | DSPH GSheet |
| residence | DSPH GSheet |
| symptoms | DSPH GSheet |
| confirmation_date | DSPH GSheet |
| facility | DSPH GSheet |
| status | DSPH GSheet |
| announcement_date | DSPH GSheet |
| final_status_date | DSPH GSheet |

### Case Network

With the cases available, a `get_case_network` function is created to see how the pandemic is spreading amongst the cases.

```python
from phcovid import get_cases, get_case_network
df = get_cases()

# takes in the cases dataframe as input
case_network = get_case_network(df)
print(case_network)

# 	network_no	network_cases	network_num_cases
#0	0	        [1025]	        1
#1	1	        [1030]	        1
#2	2	        [1034]	        1
#3	3	        [1041]	        1
#4	4	        [1042]	        1
```

### Case Plot

```python
from phcovid import get_cases, get_case_plot
df = get_cases()

# takes in the cases dataframe
get_case_plot(df)
```

By default, the plot will be created from the `confirmation_date` column. This can be changed through `date_col` parameter.

```python
get_case_plot(df, date_col="new_col_to_plot")
```

Lastly, a `start_date` can also be set (it used all data by default). This date will be in the format `MM-DD-YY`.

```python
get_case_plot(df, start_date="03-02-20")
```

An example similar to image below should be the result.

![Case Plot from March 2 to March 23](./docs/assets/case_plot&#32;03-02-20&#32;to&#32;03-23-20.png)

## Contributing

### Getting Started

All tests are done on `Python 3` and may not work as expected on `Python 2`. As such, it is highly recommended that you have `Python 3` installed.

Make sure to install all libraries for development in your local.

```bash
pip install -r requirements.dev.txt
```
