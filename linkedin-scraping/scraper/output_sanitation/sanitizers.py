import re

ACCENTS = {
    "a": "[àáâãäå]",
    "e": "[èéêë]",
    "i": "[ìíîï]",
    "o": "[òóôõö]",
    "u": "[ùúûü]",
    "y": "[ýÿ]",
    "n": "[ñ]",
    "ss": "[ß]",
}

UNWANTED_TITLES = [
    ",.*",
    r"\(.+?\)",
    r"(Mr\.|Mrs\.|Ms\.|Dr\.|Prof\.)",
    "I[IV][I]?",
    "'",
    r"(Jr\.|Sr\.)",
]


def remove_accents(data):
    for k, v in ACCENTS.items():
        data = re.sub(f"{v}", k, data)
    return data


def remove_titles(data):
    for r in UNWANTED_TITLES:
        data = re.sub(r, "", data)
    data = re.sub(r"\.", " ", data)
    return re.sub(r"\s+", " ", data)


def misc_filters(data):
    chr_map = re.compile("[^a-zA-Z -]")
    data = chr_map.sub("", data)
    return data.strip()


def sanitize(data):
    pipeline = [remove_accents, remove_titles, misc_filters]
    for job in pipeline:
        data = job(data)
    return data
