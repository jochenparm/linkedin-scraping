import re
from abc import ABCMeta
from abc import abstractmethod
from abc import abstractproperty

import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class SearchEngineBase(metaclass=ABCMeta):
    @abstractproperty
    def employee_name_filter(self):
        raise NotImplementedError

    @abstractmethod
    def idx(self, depth_index):
        raise NotImplementedError

    @abstractproperty
    def name(self):
        raise NotImplementedError

    @abstractproperty
    def url(self):
        raise NotImplementedError

    @abstractproperty
    def html(self):
        raise NotImplementedError


class GoogleEngine(SearchEngineBase):
    @property
    def name(self):
        return "google"

    @property
    def url(self):
        return "https://www.google.com/search?q=site%3Alinkedin.com%2Fin%2F+%22at+{COMPANY}%22&start={INDEX}"

    @property
    def html(self):
        return ["h3", "class", "LC20lb"]

    def idx(self, depth_index):
        return depth_index * 10

    @property
    def employee_name_filter(self):
        return lambda x: re.sub(" (-|–|\xe2\x80\x93).*", "", x.getText())


class YahooEngine(SearchEngineBase):
    @property
    def name(self):
        return "yahoo"

    @property
    def url(self):
        return "https://search.yahoo.com/search?p=site%3Alinkedin.com%2Fin%2F+%22at+{COMPANY}%22&b={INDEX}"

    @property
    def html(self):
        return ["a", "class", "ac-algo fz-l ac-21th lh-24"]

    def idx(self, depth_index):
        return (depth_index * 10) + 1

    @property
    def employee_name_filter(self):
        return lambda x: re.sub(" (-|–|\xe2\x80\x93).*", "", x.getText())


class BingEngine(SearchEngineBase):
    @property
    def name(self):
        return "bing"

    @property
    def url(self):
        return "https://www.bing.com/search?q=site%3Alinkedin.com%2Fin%2F+%22at+{COMPANY}%22&first={INDEX}"

    @property
    def html(self):
        return ["li", "class", "b_algo"]

    def idx(self, depth_index):
        return depth_index * 14

    @property
    def employee_name_filter(self):
        return lambda x: re.sub(
            " (-|–|\xe2\x80\x93).*", "", x.findAll("a")[0].getText()
        )
