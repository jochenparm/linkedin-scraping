import random
import time

import requests
from bs4 import BeautifulSoup
from scraper.output_sanitation.sanitizers import sanitize
from scraper.search_engines.engines import SearchEngine

HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:75.0) Gecko/20100101 Firefox/75.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate",
    "DNT": "1",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
    "Referer": "https://www.google.com/",
}


def get_raw_content(url_template, company, index, timeout=25):
    return requests.get(
        url_template.format(COMPANY=company, INDEX=index),
        headers=HEADERS,
        timeout=timeout,
        verify=False,  # noqa: S501
    ).text


def filter_captcha(raw_content):
    if "solving the above CAPTCHA" not in raw_content:
        return
    raise ValueError("Captcha triggered, stopping execution")


def extract_names(raw_content, html, employee_name_filter):
    soup = BeautifulSoup(raw_content, "lxml")
    names = []
    if soup.findAll(html[0], {html[1]: html[2]}):
        for person in soup.findAll(html[0], {html[1]: html[2]}):
            name = sanitize(employee_name_filter(person))
            names.append(name)
    return names


def scrape_names(search_engine: SearchEngine, company, depth, timeout):
    names = []
    for index in range(depth):
        raw_content = get_raw_content(
            search_engine.url, company, search_engine.idx(index), timeout
        )
        filter_captcha(raw_content)
        names += extract_names(
            raw_content, search_engine.html, search_engine.employee_name_filter
        )
        time.sleep(round(random.uniform(2.0, 5.0), 2))  # noqa: S311
    return names
