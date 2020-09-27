#!/usr/bin/env python3
import fire
from scraper.employee_scraper import EmployeeScraper
from typeguard import typechecked


@typechecked
def scrape(company: str, depth: int = 5, timeout: int = 25, output: str = "./") -> None:
    scraper = EmployeeScraper(company, depth=depth, timeout=timeout)
    scraper.loop.run_until_complete(scraper.run())
    print("\n\n[+] Number of employees identified: {}".format(len(scraper.employees)))
    with open(f"{output}/names.txt", "a") as f:
        for name in sorted(scraper.employees):
            f.write(f"{name}\n")


if __name__ == "__main__":
    fire.Fire(scrape)
