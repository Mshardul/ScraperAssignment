'''
This module defines the scrapper routes for the API.
'''

from fastapi import APIRouter, Depends
from routers.authentication import authenticate_token
from utils.scraper_manager import ScraperManager
from utils.request_manager import get_request_id

router = APIRouter()

@router.get("/scrape")
async def scrape_products(
    page_limit: int = 1,
    proxy_string: str = "",
    token: str = Depends(authenticate_token),
    req_id: str = Depends(get_request_id),
) -> dict:
    ''' main method to scrape the webpage '''
    print("routers/scrapper/scrape_products/token: ", token)
    scraper = ScraperManager(req_id=req_id, page_limit=page_limit, proxy=proxy_string)
    scraped_data: list[dict] = await scraper.start_scraping()
    return {"status": "success", "scraped_data": scraped_data}
