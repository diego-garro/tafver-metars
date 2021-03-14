import logging
import os
from datetime import datetime

import click

from . import __version__
from .console import console
from .download import download_data_from_ogimet
from .exceptions import MonthError, YearError
from .logger import logger


def print_version(ctx, param, value):
    if not value or ctx.resilient_parsing:
        return
    click.echo(__version__)
    ctx.exit()


@click.group()
@click.option(
    "--version", is_flag=True, callback=print_version, expose_value=False, is_eager=True
)
def taf_ver():
    pass


@taf_ver.command()
@click.argument("station-icao", type=click.STRING)
@click.option("-m", "--month", type=click.INT, help="The month to download")
@click.option("-y", "--year", type=click.INT, help="The year to download")
def download(station_icao: str, month: int, year: int):
    log = open("logging.log", "w")
    log.close()

    try:
        os.mkdir(f"{station_icao}")
    except Exception as error:
        logger.warning(error)

    today = datetime.now()
    if month:
        if month > today.month and not year:
            raise MonthError()
            exit()

    if year:
        if year > today.year:
            raise YearError()
            exit()
        elif year < 2005:
            raise YearError(message="The year to download must be older than 2004")
            exit()

    if year != None and month != None:
        metars, tafs = download_data_from_ogimet(station_icao, month, year=year)
        month = f"{month}" if month >= 10 else f"0{month}"
    elif year:
        metars, tafs = download_data_from_ogimet(station_icao, today.month, year=year)
        month = f"{today.month}" if today.month >= 10 else f"0{today.month}"
    elif month:
        metars, tafs = download_data_from_ogimet(station_icao, month)
        month = f"{month}" if month >= 10 else f"0{month}"
        year = f"{today.year}"
    else:
        metars, tafs = download_data_from_ogimet(station_icao, today.month)
        year = f"{today.year}"
        month = f"{today.month}" if today.month >= 10 else f"0{today.month}"

    metars_file = open(f"./{station_icao}/{year}{month}METAR.txt", "w")
    tafs_file = open(f"./{station_icao}/{year}{month}TAF.txt", "w")

    for line in metars:
        metars_file.write(line + "\n")

    for line in tafs:
        tafs_file.write(line + "\n")

    metars_file.close()
    tafs_file.close()


if __name__ == "__main__":
    taf_ver()
