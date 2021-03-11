# TAFVER METARS

Simple command line tool to download METAR's and TAF's for a given station.

## Examples

To download data from the current month for JFK INT. Airport only run 

```
tafver_metars download kjfk
```

If you need older month but the same year run

```
tafver_metars download kjfk -m 2
```

where `-m 2` its an option and refers to february. Take in count that this value must be
earlier than the actual month for the same year.

If you need older year run

```
tafver_metars download kjfk -y 2020
```

where `-y 2020` its an option and refers to the year 2020. Take in count that year must be
older than 2004, only years from 2005 onwards are allowed. That's because only this years are
in databases of Ogimet.com. 