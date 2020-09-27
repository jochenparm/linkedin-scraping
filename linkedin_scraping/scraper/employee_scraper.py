import asyncio
from asyncio import AbstractEventLoop
from typing import List
from typing import Set

from scraper.scraper_pipeline import scrape_names
from scraper.search_engines.engines import BingEngine
from scraper.search_engines.engines import GoogleEngine
from scraper.search_engines.engines import SearchEngine
from scraper.search_engines.engines import YahooEngine
from typeguard import typechecked


class EmployeeScraper:
    loop: AbstractEventLoop = asyncio.get_event_loop()
    employees: Set = set()
    search_engines: List[SearchEngine] = [GoogleEngine, YahooEngine, BingEngine]

    @typechecked
    def __init__(self, company: str, depth: int = 5, timeout: int = 25) -> None:
        self.company = company
        self.depth = depth
        self.timeout = timeout

    @typechecked
    async def run(self) -> None:
        futures = [
            self.loop.run_in_executor(
                None, scrape_names, se, self.company, self.depth, self.timeout
            )
            for se in self.search_engines
        ]

        for data in asyncio.as_completed(futures):
            names = await data
            self.employees.update(names)
