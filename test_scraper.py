import asyncio
import sys
import os
import json
sys.path.insert(0, os.path.join(os.getcwd(), 'outscraper-python'))
from scrapers.real_playwright import scrape_real_playwright

async def run():
    res = await scrape_real_playwright('Travel agent', 'Satellite, Ahmedabad', 5)
    with open('output.json', 'w') as f:
        json.dump(res, f, indent=2)

asyncio.run(run())
