import re

def _sanitize_type(metar: str, icao_code: str):
    metar = metar.replace('SPECI', 'METAR')
    metar = metar.replace('COR', '')
    
    if metar.count('METAR') == 0:
        icao = icao_code.upper()
        metar = metar.replace(icao, f'METAR {icao}')
    
    return metar


def _sanitize_weather(metar: str):
    metar = re.sub(r'DZ|SHRA', 'RA', metar)
    metar = re.sub(r'BR|HZ|[BP][CR]FG', 'FG', metar)
    metar = re.sub(r'(FG\s){2,}', 'FG ', metar)
    metar = re.sub(r'VC[A-Z][A-Z]', '', metar)

    return metar


def _sanitize_visibility(metar: str):
    metar = metar.replace('CAVOK', '9999')
    metar = re.sub(r'9999\s{2,}', '9999 ', metar)
    
    return metar

def _sanitize_cloud(metar: str):
    metar = re.sub(r'VV///|NSC', '', metar)
    metar = re.sub(r'FW|FE|EW|GEW|FWE|HEW|FE[A-Z]W|F[A-Z]EW', 'FEW', metar)
    metar = re.sub(r'ST|SC|CT|ACT|STC|DCT|SC[A-Z]T|S[A-Z]CT', 'SCT', metar)
    metar = re.sub(r'BN|BK|KN|VKN|BNK|NNK|BK[A-Z]N|B[A-Z]KN', 'BKN', metar)
    metar = re.sub(r'OC|OV|IVC|PVC|OV[A-Z]C|O[A-Z]VC', 'OVC', metar)
    
    return metar

def sanitize_metar(metar: str, icao_code: str):
    metar = _sanitize_type(metar, icao_code)
    metar = _sanitize_weather(metar)
    metar = _sanitize_visibility(metar)
    metar = _sanitize_cloud(metar)
    
    return metar