from datetime import date, datetime, timedelta, timezone
from collections import Counter
from dateutil import tz
import pandas as pd
import requests
import lxml.html
import unicodedata

"""
A study/reference material on dates handling

Content:
-------
Dates from a list of date objects
Dates from a parsed list of strings
Datetimes with timezones
Datetimes from a CSV file (dates handling with pandas)
Dates from the web (historical dates manual parsing)
"""


## Dates from a list of date objects
#  ---------------------------------
# 
## Independence dates for American countries
# 
## date()
## .strftime()
## .weekday() 
## .day .days .month .year
## .isoformat()
#
## others:  .sum(), .join(),
#           zip(), map(), range(), print(), sorted(), len(), min(), max()
#           collections.Counter(), list comprehension

independence_dates = [
    date(1776, 7, 4),
    date(1804, 1, 1),
    date(1811, 5, 15),
    date(1816, 7, 9),
    date(1818, 2, 12),
    date(1819, 7, 5),
    date(1819, 7, 20),
    date(1821, 9, 16),
    date(1822, 5, 24),
    date(1822, 9, 7),
    date(1824, 7, 28),
    date(1825, 8, 6),
    date(1828, 8, 27),
    date(1838, 7, 25),
    date(1838, 9, 15),
    date(1838, 9, 15),
    date(1838, 9, 15),
    date(1838, 9, 15),
    date(1865, 8, 16),
    date(1867, 7, 1),
    date(1898, 5, 20),
    date(1903, 11, 3),
    date(1962, 8, 6),
    date(1966, 5, 26),
    date(1966, 8, 31),
    date(1966, 11, 30),
    date(1973, 7, 10),
    date(1974, 7, 2),
    date(1975, 11, 25),
    date(1978, 11, 3),
    date(1979, 2, 22),
    date(1979, 10, 27),
    date(1981, 9, 21),
    date(1981, 11, 1),
    date(1983, 9, 19)
    ]

countries = [
    "EUA",
    "Haiti",
    "Paraguai",
    "Argentina",
    "Chile",
    "Venezuela",
    "Colômbia",
    "México",
    "Equador",
    "Brasil",
    "Peru",
    "Bolívia",
    "Uruguai",
    "Nicarágua",
    "Costa Rica",
    "El Salvador",
    "Guatemala",
    "Honduras",
    "República Dominicana",
    "Canadá",
    "Cuba",
    "Panamá",
    "Jamaica",
    "Guiana",
    "Trindade e Tobago",
    "Barbados",
    "Bahamas",
    "Granada",
    "Suriname",
    "Dominica",
    "Santa Lúcia",
    "São Vicente e Granadinas",
    "Belize",
    "Antígua e Barbuda",
    "São Cristóvão e Nevis"
]

countries_independence_dates = [*zip(countries, independence_dates)]
countries_independence_dates_dict = dict(countries_independence_dates)
_ = [print(country_independence_date[0], country_independence_date[1].strftime("%d/%m/%Y"), sep=": ", end=", ") for country_independence_date in countries_independence_dates]
print("\n")


weekdays_names = {0: "Monday", 1: "Tuesday", 2: "Wednesday", 3: "Thirsday", 4: "Friday", 5: "Saturday", 6: "Sunday"}
weekdays_names_ptBR = {0: "Segunda", 1: "Terça", 2: "Quarta", 3: "Quinta", 4: "Sexta", 5: "Sábado", 6: "Domingo"}
months_names_ptBR = {1: "Janeiro", 2: "Fevereiro", 3: "Março", 4: "Abril", 5: "Maio", 6: "Junho", 7: "Julho", 8: "Agosto", 9: "Setembro", 10: "Outubro", 11: "Novembro", 12: "Dezembro"}
weekdays = [*map(date.weekday, independence_dates)]
named_weekdays = [weekdays_names[day] for day in weekdays]
named_weekdays_ptBR = [weekdays_names_ptBR[day] for day in weekdays]
months = [independence_date.month for independence_date in independence_dates]
named_months_ptBR = [months_names_ptBR[month] for month in months]

time_deltas = [independence_dates[l+1] - independence_dates[l] for l in range(len(independence_dates)-1)]
dates_and_deltas = [*zip(independence_dates, time_deltas)]
print(" => ".join([f"{date_and_delta[0]} + ({date_and_delta[1].days} days)" for date_and_delta in sorted(dates_and_deltas)]))

date_strings = [independence_date.strftime("%d/%m/%Y") for independence_date in independence_dates]
print(", ".join(date_strings))


print(f"Shortest period between independences: {min(time_deltas).days}", f"Longest period between independencies: {max(time_deltas).days}", f"Mean period between independences: {int(sum([delta.days for delta in time_deltas])/len(time_deltas))} days (rounded)", sep=" days \n")
print("First independence date in America (ISO format):", min(independence_dates).isoformat())
print("Last independence date in America (convenient format):", max(independence_dates).strftime("%B (%Y)"))
print("Brazil's independence date (day of the year):", countries_independence_dates_dict["Brasil"].strftime("%jth day of %Y"), "\n")

print("Amount of independences on days of the week, months and years")
print("Dia da semana", Counter(named_weekdays_ptBR))
print("Mês", Counter(named_months_ptBR))
print("Ano", Counter([independence_date.year for independence_date in independence_dates]))



## Dates from a parsed list of strings
#  -----------------------------------
# 
## Speed record break dates for land vehicles
# 
## .strptime()
## .strftime()
#
## others:  .split()
#           print(), len(), 
#           list comprehension, nested functions, 

land_speed_record_dates_not_normalized = [
    "December 18, 1898",
    "January 17, 1899",
    "January 17, 1899",
    "January 27, 1899",
    "March 4, 1899",
    "April 29, 1899",
    "April 13, 1902",
    "August 5, 1902",
    "November 5, 1902",
    "November 17, 1902",
    "July 17, 1903",
    "November 5, 1903",
    "January 12, 1904",
    "March 31, 1904",
    "May 25, 1904",
    "July 21, 1904",
    "November 13, 1904",
    "December 30, 1905",
    "January 26, 1906",
    "November 8, 1909",
    "June 24, 1914",
    "May 17, 1922",
    "July 6, 1924",
    "July 12, 1924",
    "September 25, 1924",
    "July 21, 1925",
    "March 16, 1926",
    "April 27, 1926",
    "April 28, 1926",
    "February 4, 1927",
    "March 29, 1927",
    "February 19, 1928",
    "April 22, 1928",
    "March 11, 1929",
    "February 5, 1931",
    "February 24, 1932",
    "February 22, 1933",
    "March 07, 1935",
    "September 3, 1935",
    "November 19, 1937",
    "August 27, 1938",
    "September 15, 1938",
    "September 16, 1938",
    "August 23, 1939",
    "September 16, 1947",
    "August 5, 1963",
    "October 2, 1964",
    "October 5, 1964",
    "October 13, 1964",
    "October 15, 1964",
    "October 27, 1964",
    "November 2, 1965",
    "November 7, 1965",
    "November 15, 1965",
    "October 23, 1970",
    "October 4, 1983",
    "September 25, 1997",
    "October 15, 1997"
]

def add_zero_to_date_day(dates: list) -> list:
    def add_zero(date_to_add_zero):
        split_date =  date_to_add_zero.split()
        date_with_zero = split_date[0] + " 0" + split_date[1] + " " + split_date[2]
        return date_with_zero
    dates_with_zero = [add_zero(d) if len(d.split()[1]) == 2 else d for d in dates]
    return dates_with_zero

land_speed_record_dates = add_zero_to_date_day(land_speed_record_dates_not_normalized)
print("Recordes terrestres normalizados: ", land_speed_record_dates[:5])
DATE_FORMAT = "%B %d, %Y"
iso_land_speed_records_dates = [datetime.strptime(record_date, DATE_FORMAT) for record_date in land_speed_record_dates]
print(", ".join([record_date.strftime("%d/%m/%Y") for record_date in iso_land_speed_records_dates[:5]]))



## Datetimes with timezones
#  ------------------------
# 
## This exercise date and time. Brazil's UTC on selected days (of daylight saving shifts).
# 
## timedelta()
## timezone()
## .astimezone()
## .strptime()
## .strftime()
## .isoformat()
## .replace()
## tz.gettz()
## tz.datetime_ambiguous()
#
## others:  .join(), .split()
#           zip(), map(), range(), print(), sorted(), len(), 
#           collections.Counter(), list comprehension

dt = datetime(2017, 12, 31, 15, 19, 13)
dt_old = dt.replace(year=1917)
print(dt_old.isoformat(" "))
one_year = timedelta(days=365)
one_month = timedelta(days=30)
one_week = timedelta(days=7)
one_day = timedelta(days=1)
one_hour = timedelta(hours=1)
time_zone_brazil = timezone(timedelta(hours=-3))
time_zone_west_coast = timezone(timedelta(hours=-8))
datetime_of_this_exercise = datetime(2021, 11, 9, 19, 30, 0, tzinfo=time_zone_brazil)
print("Datahora do exercício", datetime_of_this_exercise.isoformat())
print("Datahora do exercício na West Coast", datetime_of_this_exercise.astimezone(time_zone_west_coast).isoformat())
updated_time_this_exercise = datetime_of_this_exercise.replace(minute=59)
print("Datahora do exercício modificada", updated_time_this_exercise.isoformat())

daylightsaving_shift_in_brazil = datetime(2000, 10, 18, tzinfo=tz.gettz("America/Sao_Paulo"))
daylightsaving_end_in_brazil = datetime(2000, 2, 16, tzinfo=tz.gettz("America/Sao_Paulo"))
print(", ".join([daylightsaving_shift_in_brazil.replace(year=y).strftime("%Y UTC%Z") for y in range(2001, 2021)]))
print(", ".join([daylightsaving_end_in_brazil.replace(year=y).strftime("%Y UTC%Z") for y in range(2001, 2021)]))
ambiguous_time = datetime(2017, 2, 18, 1, 30, 0, tzinfo=time_zone_brazil)
print("Horário ambíguo?", tz.datetime_ambiguous(ambiguous_time), "\n")



## Datetimes from a CSV file (dates handling with pandas)
#  ------------------------------------------------------
# 
## Accidents data from Ecoponte (Presidente Costa e Silva bridge, Ponte Rio-Niterói)
# 
## pd.read_csv(parse_dates, day_first)
## pd.to_datetime()
## .copy()
## .sort_values()
## .head()
## pd.Series
#
## others:  .sum()
#           max(), range(), len(), type(), print()
#           list comprehension

ecoponte = pd.read_csv("demostrativo_acidentes_ecoponte.csv", sep=";", encoding="latin-1", parse_dates=[['data', 'horario']], dayfirst=True)
# There was a need to specify the encoding. Windows pt-BR uses latin-1, so I went for it, and it worked.
ecoponte_datetime = pd.read_csv("demostrativo_acidentes_ecoponte.csv", sep=";", encoding="latin-1")
ecoponte_datetime["datahora"] = pd.to_datetime(ecoponte_datetime["data"]+ " " + ecoponte_datetime["horario"], format="%d/%m/%Y %H:%M:%S")

print(type(ecoponte_datetime["datahora"][1]))

print(ecoponte[["levemente_feridos", "moderadamente_feridos", "gravemente_feridos", "mortos"]].sum())
print("\n")
ecoponte_simple = ecoponte[["data_horario", "tipo_de_acidente", "tipo_de_ocorrencia"]].copy().sort_values(by=["data_horario"], ignore_index=True)
print(ecoponte_simple.head(20))
ecoponte_simple['tempo_entre_acidentes'] = pd.Series([ecoponte_simple["data_horario"][l+1] - ecoponte_simple["data_horario"][l] for l in range(len(ecoponte_simple["data_horario"])-1)])
print(ecoponte_simple[["data_horario", "tempo_entre_acidentes"]].head(20))
print(ecoponte_simple[ecoponte_simple["tempo_entre_acidentes"] == max(ecoponte_simple["tempo_entre_acidentes"])])



## Dates from historical dates, from the web
#  -----------------------------------------
#
## Dates of independence of all countries, as they are commonly written ("th century", "CE")
## No support for BCE yet.
#
#


url = "https://www.thoughtco.com/independence-birthday-for-every-country-1435141"
# no user-agent header needed in this one
dates_xpath = '//p[@class="comp mntl-sc-block mntl-sc-block-html"]/text()'
dates2_xpath = '//p[@class="comp mntl-sc-block mntl-sc-block-html"]/a/text()'
request =  requests.get(url=url)
# We found a '\xA0', that seem to be HTML codes like &bdquo &nbsp converted to "?" or "xA0" (hex values).
# Decoding it as latin-1 didn't do the trick this time, so I had to normalize it, and that did it for the hex.
# We still need some more strips (or regex replace, but that would be an overkill here imh).
# For future reference, the capture regex would be along the lines of r'[^\x00-\x7F]+'
response = lxml.html.fromstring(unicodedata.normalize("NFKD", request.text))
raw = response.xpath(dates_xpath)[6:]
raw2 = response.xpath(dates2_xpath)[3:]
raws = [*filter(None,[*[s.strip() for s in raw], *[s.strip() for s in raw2]])]

def create_datetime_with_some_common_writting_support(date_in_str: str) -> datetime.date:
    def add_zero_with_century(date_to_add_zero):
        if len(date_to_add_zero[1]) == 3:
            s = date_to_add_zero[0] + " " + date_to_add_zero[1] + " " + date_to_add_zero[2]
            return s
        if date_to_add_zero[1].lower() == "century":
            g = "January 01, 0" + str((int(split_date[0].replace("th", ""))-1)*100)
            return g
        date_with_zero = date_to_add_zero[0] + " 0" + date_to_add_zero[1] + " " + date_to_add_zero[2]
        return date_with_zero
    DATE_FORMAT = "%B %d, %Y"
    split_date = date_in_str.split()
    if split_date[0].isdigit():
        if int(split_date[0]) == split_date[0]:
            if len(split_date) == 2:
                if split_date[1] == "CE":
                    k = date(year=int(split_date[0]), month=1, day=1)
                    return k
        if len(split_date) == 1:
            m = date(year=int(*split_date), month=1, day=1)
            return m
        if (len(split_date) == 2) and (split_date[1] == "CE"):
            m = date(year=int(split_date[0]), month=1, day=1)
            return m
        return date(year=1, month=1, day=1)
    else:
        if len(split_date) == 3:
            j = datetime.strptime(add_zero_with_century(split_date), DATE_FORMAT).date()
            return j
        if len(split_date) == 2:
            if split_date[1].lower() == "century":
                if len(split_date[0]) == 3:
                    h = "January 01, 0" + str((int(split_date[0].replace("th", ""))-1)*100)
                elif len(split_date[0]) == 4:
                    h = "January 01, " + str((int(split_date[0].replace("th", ""))-1)*100)
                else:
                    h = split_date
                return datetime.strptime(h , DATE_FORMAT).date()
 

all_countries_independence_dates = [ (c.split(":")[1].strip(), create_datetime_with_some_common_writting_support(c.split(":")[0].strip())) if (len(c.split(":")) == 2) else None for c in raws]

all_countries_independence_dates_sorted_by_date = sorted(all_countries_independence_dates, key=lambda x: x[1])[2:]
japan_china_correction = "Japan: 660 BCE, China: 221 BCE,"

print(japan_china_correction, ", ".join([f"{d[0]}: {d[1].strftime('%d/%m/%Y')}" for d in all_countries_independence_dates_sorted_by_date]))