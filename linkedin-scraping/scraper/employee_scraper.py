import asyncio
from typing import List

from scraper.scraper_pipeline import scrape_names
from scraper.search_engines.engines import BingEngine
from scraper.search_engines.engines import GoogleEngine
from scraper.search_engines.engines import SearchEngine
from scraper.search_engines.engines import YahooEngine


class EmployeeScraper:
    loop = asyncio.get_event_loop()
    employees = set()
    search_engines: List[SearchEngine] = [GoogleEngine, YahooEngine, BingEngine]

    def __init__(self, company, depth=5, timeout=25):
        self.company = company
        self.depth = depth
        self.timeout = timeout

    async def run(self):
        futures = [
            self.loop.run_in_executor(
                None, scrape_names, se, self.company, self.depth, self.timeout
            )
            for se in self.search_engines
        ]

        for data in asyncio.as_completed(futures):
            names = await data
            self.employees.update(names)
