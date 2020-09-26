#!/usr/bin/env python3

import fire
from scraper.scraper import Scraper


def scrape(company, depth=5, timeout=25, output="./"):
    scraper = Scraper(company, depth=depth, timeout=timeout)
    scraper.loop.run_until_complete(scraper.run())
    print("\n\n[+] Names Found: %d" % len(scraper.employees))
    print("[*] Writing names to the following directory: %s" % output)
    with open("%s/names.txt" % (output), 'a') as f:
        for name in scraper.employees:
            f.write("%s\n" % name)


if __name__ == '__main__':
    fire.Fire(scrape)