import asyncio
import sys
sys.path.append('C:\\Users\\admimn\\OneDrive\\Desktop\\MyScraperProject\\outscraper-python')
from scrapers.real_playwright import scrape_real_playwright

async def progress_update(p, m):
    print(f'PROG {p}: {m}')

async def run():
    try:
        res = await scrape_real_playwright('Travel agent', 'Satellite, Ahmedabad', 1, progress_update)
        print('RESULT', res)
    except Exception:
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    asyncio.run(run())
