# phcovid
## Get clean PH COVID data in only two lines of code!
Source: PH DOH data shared by this [blog post](https://www.facebook.com/notes/wilson-chua/working-with-doh-covid-data/2868993263159446/)

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
