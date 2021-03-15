"""Module to download METAR's and TAF's from Ogimet.com"""

import re
from calendar import monthrange
from datetime import datetime

from bs4 import BeautifulSoup
from requests import get

from .console import console
from .logger import logger
from .sanitize import sanitize_metar, sanitize_taf

TODAY = datetime.now()
OGIMET_LIMIT_MESAGE = "#Sorry, Your quota limit for slow queries rate has been reached"


class OgimetQuotaLimitError(Exception):
    """
    #Sorry, Your quota limit for slow queries rate has been reached

    The anterior message is raised by Ogimet.com when you get a request
    one after another. So, you must to wait at less five minutes to ensure
    succesful request of METAR data.

    This exception is raised when that message is detected.
    """

    def __init__(self, message=OGIMET_LIMIT_MESAGE):
        super().__init__(message + ". Wait a few minutes to execute a new request. :)")


def _join_line_separated_metars(metar_list: list, icao_code: str):
    """Joins the metar when it is separated in several lines

    Args:
        metar_list (list): The Metar list from file lines without fromating

    Returns:
        list: The correct Metar list, one Metar by item
    """
    metar = ""
    correct_metar_list = []
    for line in metar_list:
        metar += re.sub(r"^\s{2,}", " ", line)
        if "=" in line:
            sanitized = sanitize_metar(metar, icao_code)
            correct_metar_list.append(sanitized)
            # correct_metar_list.append(metar)
            metar = ""

    return correct_metar_list


def download_data_from_ogimet(icao_code: str, month: int, year=TODAY.year):
    metars = []
    tafs = []
    month_range = monthrange(year=year, month=month)

    if month >= 10:
        month = f"{month}"
    else:
        month = f"0{month}"

    url = f"https://www.ogimet.com/display_metars2.php?lugar={icao_code.lower()}&tipo=ALL&ord=DIR&nil=SI&fmt=txt&ano={year}&mes={month}&day=01&hora=00&anof={year}&mesf={month}&dayf={month_range[1]}&horaf=23&minf=59&enviar=Ver"

    try:
        res = get(url)
        html_soup = BeautifulSoup(res.text, "html.parser")
        data = html_soup.text.split("\n")

        # print(data)
        # print(f'DATA: {data[:50]}')
        # print(f'DATA: {data[-50:-1]}')

        if OGIMET_LIMIT_MESAGE in data:
            raise OgimetQuotaLimitError()
        elif "Fallo de consulta" in data[-1]:
            raise OgimetQuotaLimitError(message=data[-1])
        else:
            # Extract the METAR's from data
            for line in data[32:]:
                if line == "":
                    break
                metars.append(line)

            # Extract the TAF's from data
            for line in data[32 + len(metars) + 6 :]:
                line = sanitize_taf(line, icao_code)
                tafs.append(line.strip())

            # Rensemble METAR's separated in several lines
            metars = _join_line_separated_metars(metars, icao_code)

            return metars, tafs
    except Exception as error:
        logger.error("Some error ocurred: {}".format(error))
        exit()


if __name__ == "__main__":
    download_data_from_ogimet("mroc", 1)
