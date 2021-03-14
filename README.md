# TAFVER METARS

Simple command line tool to download METAR's and TAF's for a given station.

## Requirements

This package requires:

* [Python ^3.6][python-home]
* [Git ^2.0.0][git-home]

[python-home]: https://www.python.org
[git-home]: https://git-scm.com

Python because it was developed on that version and Git for discriminate the use
and choose the logging level for that use.

## Installation

For install only run this command from your terminal

```
pip install tafver-metars
```

### Update

Update with `pip` adding the option --upgrade

```
pip install --upgrade tafver-metars
```

## Examples

To download data from the current month for JFK INT. Airport only run 

```
tafver download kjfk
```

If you need older month but the same year run

```
tafver download kjfk -m 2
```

where `-m 2` its an option and refers to february. Take in count that this value must be
earlier than the actual month for the same year.

If you need older year run

```
tafver download kjfk -y 2020
```

where `-y 2020` its an option and refers to the year 2020. Take in count that the year must be
older than 2004, only years from 2005 onwards are allowed. That's because only this years are
available in databases of Ogimet.com. 