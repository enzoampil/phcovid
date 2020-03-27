# phcovid
[![Build Status](https://travis-ci.com/enzoampil/phcovid.svg?branch=master)](https://travis-ci.com/github/enzoampil/phcovid)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg )](https://raw.githubusercontent.com/enzoampil/phcovid/master/LICENSE)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

## Setup
```
pip install phcovid
```
## Get PH COVID data in only two lines of code!
Source: PH DOH data shared in this [blog post](https://www.facebook.com/notes/wilson-chua/working-with-doh-covid-data/2868993263159446/)

```
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
