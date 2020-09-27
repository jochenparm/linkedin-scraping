import re
from typing import Dict
from typing import List

ACCENTS: Dict = {
    "a": "[àáâãäå]",
    "e": "[èéêë]",
    "i": "[ìíîï]",
    "o": "[òóôõö]",
    "u": "[ùúûü]",
    "y": "[ýÿ]",
    "n": "[ñ]",
    "ss": "[ß]",
}

UNWANTED_TITLES: List[str] = [
    ",.*",
    r"\(.+?\)",
    r"(Mr\.|Mrs\.|Ms\.|Dr\.|Prof\.)",
    "I[IV][I]?",
    "'",
    r"(Jr\.|Sr\.)",
]


def remove_accents(data: str) -> str:
    for k, v in ACCENTS.items():
        data = re.sub(f"{v}", k, data)
    return data


def remove_titles(data: str) -> str:
    for r in UNWANTED_TITLES:
        data = re.sub(r, "", data)
    data = re.sub(r"\.", " ", data)
    return re.sub(r"\s+", " ", data)


def misc_filters(data: str) -> str:
    chr_map = re.compile("[^a-zA-Z -]")
    data = chr_map.sub("", data)
    return data.strip()


def sanitize(data: str) -> str:
    pipeline = [remove_accents, remove_titles, misc_filters]
    for job in pipeline:
        data = job(data)
    return data
