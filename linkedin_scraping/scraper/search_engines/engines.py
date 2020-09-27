import re
from dataclasses import dataclass
from typing import Callable
from typing import List

import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


@dataclass
class SearchEngine:
    employee_name_filter: Callable
    idx: Callable
    name: str
    url: str
    html: List[str]


GoogleEngine = SearchEngine(
    name="google",
    url="https://www.google.com/search?q=site%3Alinkedin.com%2Fin%2F+%22at+{COMPANY}%22&start={INDEX}",
    html=["h3", "class", "LC20lb"],
    idx=lambda x: x * 10,
    employee_name_filter=lambda x: re.sub(" (-|–|\xe2\x80\x93).*", "", x.getText()),
)

YahooEngine = SearchEngine(
    name="yahoo",
    url="https://search.yahoo.com/search?p=site%3Alinkedin.com%2Fin%2F+%22at+{COMPANY}%22&b={INDEX}",
    html=["a", "class", "ac-algo fz-l ac-21th lh-24"],
    idx=lambda x: (x * 10) + 1,
    employee_name_filter=lambda x: re.sub(" (-|–|\xe2\x80\x93).*", "", x.getText()),
)

BingEngine = SearchEngine(
    name="bing",
    url="https://www.bing.com/search?q=site%3Alinkedin.com%2Fin%2F+%22at+{COMPANY}%22&first={INDEX}",
    html=["li", "class", "b_algo"],
    idx=lambda x: x * 14,
    employee_name_filter=lambda x: re.sub(
        " (-|–|\xe2\x80\x93).*", "", x.findAll("a")[0].getText()
    ),
)
