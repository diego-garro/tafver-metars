import re
from datetime import datetime

from metar import Metar

from .logger import logger


def _sanitize_type(metar: str, icao_code: str):
    metar = metar.replace("SPECI", "METAR")
    metar = metar.replace("COR", "")

    if metar.count("METAR") == 0:
        icao = icao_code.upper()
        metar = metar.replace(icao, f"METAR {icao}")

    return metar


def _sanitize_wind(metar: str):
    format = r"\s(?P<dir>\d{3})(?P<speed>\d{2})(?P<g>G?)(?P<gust>\d{2}?)(?P<units>(KT|MPS|KTS)?)\s"
    pattern = re.compile(format)

    matches = re.search(pattern, metar)

    if matches:
        if matches.group("g") is None and matches.group("gust") is not None:
            correct_format = f'{matches.group("dir")}{matches.group("speed")}G{matches.group("gust")}{matches.group("units")}'
            metar = re.sub(format, correct_format, metar)

    metar = re.sub(r"\d{3}V\d{3}", "", metar)

    return metar


def _sanitize_weather(metar: str):
    metar = re.sub(r"DZ|SHRA", "RA", metar)
    metar = re.sub(r"BR|HZ|[BP][CR]FG", "FG", metar)
    metar = re.sub(r"(FG\s){2,}", "FG ", metar)
    metar = re.sub(r"VC[A-Z][A-Z]", "", metar)
    metar = re.sub(r"\+|-", "", metar)

    return metar


def _sanitize_visibility(metar: str):
    metar = metar.replace("CAVOK", "9999")
    metar = re.sub(r"9999\s{2,}|99999", "9999 ", metar)
    metar = re.sub(r"\s\d{3,4}[NS]([ENSW])?([EW])?", "", metar)
    metar = re.sub(r"R\d{2}([A-Z])?/(P|M)?\d{4}(V(P|M)?\d{4})?(FT)?([NDU])?", "", metar)

    return metar


def _sanitize_cloud(metar: str):
    metar = re.sub(r"VV///|NSC", "", metar)
    metar = re.sub(r"\s(GEW|FWE|HEW|FE[A-Z]W|F[A-Z]EW)", " FEW", metar)
    metar = re.sub(r"\s(ACT|STC|DCT|SC[A-Z]T|S[A-Z]CT)", " SCT", metar)
    metar = re.sub(r"\s(VKN|BNK|NNK|BK[A-Z]N|B[A-Z]KN)", " BKN", metar)
    metar = re.sub(r"\s(IVC|PVC|OV[A-Z]C|O[A-Z]VC)", " OVC", metar)

    return metar


def _remove_suplementary_info(metar: str):
    metar = re.sub(
        r"\sWS\s?(R?(/|\s+)?\d{2,}|(ALL)?\s?R[WNU]+Y\s?\d{2,}).*", "=", metar
    )
    metar = re.sub(r"\sRE[A-Z]{2,}.*", "=", metar)

    return metar


def _remove_rmk_and_trend(metar: str):
    metar = re.sub(r"\s?RMK.+", "", metar)
    metar = re.sub(
        r"\s?(BECMG|BECMG(0|O|\??\s?\?+)|VECMG|BCMG|BECMG/|BECM/|BCMG/|BECOMG|BECGM|BECM\sG).+",
        "=",
        metar,
    )
    metar = re.sub(
        r"\s?(NOSIG|NOPSIG|NSIG|NPSIG|NOZIG|NOPZIG|NOSOG|MOSIG|NISIG|NOSGI|NOSI\sG|NOSIG0|NSOIG|NOSIIG).+",
        "=",
        metar,
    )
    metar = re.sub(r"\s?(TEMPO|TMPO|TEMPOO|TMEPO|TEMOP|TEMO|TEMP\sO).+", "=", metar)

    return metar


def parse_metar(metar: str):
    code = metar.replace("=", "")
    code = re.sub(r"^\d{12}\s", "", code)
    code = code.strip()

    date = datetime.strptime(metar[:12], "%Y%m%d%H%M")

    try:
        if not "NIL" in metar:
            metar_obj = Metar.Metar(code, month=date.month, year=date.year)
        else:
            pass
    except Metar.ParserError as error:
        print(error)
        logger.error(metar)


def sanitize_metar(metar: str, icao_code: str):
    metar = _remove_rmk_and_trend(metar)
    metar = _remove_suplementary_info(metar)
    metar = _sanitize_type(metar, icao_code)
    metar = _sanitize_wind(metar)
    metar = _sanitize_weather(metar)
    metar = _sanitize_visibility(metar)
    metar = _sanitize_cloud(metar)

    metar = re.sub(r"={2,}", "=", metar)
    metar = re.sub(r"\s{2,}", " ", metar)

    parse_metar(metar)

    return metar
