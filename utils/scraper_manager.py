'''
This module defines the scraper manager for the APIs.
'''

# External Imports
import os
import uuid
import time
from urllib.parse import urlparse
import requests

# Internal Project Imports
from utils.product_parser import ProductParser
from utils.cache_manager import CacheManager
from utils.data_manager import DataManager
from utils.notification_handler import NotificationHandler

class ScraperManager:
    ''' A class to manage the scraping of products. '''
    def __init__(self, req_id: str="", page_limit: int=0, proxy: str="", retries: int=3, backoff_factor: int=2):
        self.req_id: str = req_id
        self.page_limit: int = page_limit
        self.proxy: str = proxy
        self.retries: int = retries
        self.backoff_factor: int = backoff_factor
        self.cache_manager = CacheManager()
        self.notification_handler = NotificationHandler()
        self.image_folder = f"data/images/{self.req_id}/"

        os.makedirs(self.image_folder, exist_ok=True)

    def fetch_page(self, url):
        ''' Fetch a page from the URL. '''
        for attempt in range(self.retries):
            try:
                response = requests.get(
                    url,
                    proxies={"http": self.proxy, "https": self.proxy},
                    timeout=10
                )
                if response.status_code == 200:
                    return response
            except requests.exceptions.Timeout as e:
                print(f"Attempt {attempt + 1} failed: {e}")
                time.sleep(self.backoff_factor ** attempt)  # Exponential backoff
            except requests.RequestException as e:
                print(f"Attempt {attempt + 1} failed: {e}")
                time.sleep(self.backoff_factor ** attempt)  # Exponential backoff
        return None

    def download_image(self, image_url) -> str:
        ''' Download an image and save it locally, returning the local path. '''
        try:
            response = requests.get(image_url, timeout=10)
            if response.status_code == 200:
                # Extract the image filename from the URL
                ext = os.path.splitext(urlparse(image_url).path)[-1] or ".jpg"  # Default to .jpg
                unique_name: str = f"{uuid.uuid4()}{ext}"
                local_image_path: str = os.path.join(self.image_folder, unique_name)

                # Save the image to the local path
                with open(local_image_path, "wb") as image_file:
                    image_file.write(response.content)

                return local_image_path
            else:
                print(f"Failed to download image: {image_url}")
                return ''
        except requests.RequestException as e:
            print(f"Error downloading image {image_url}: {e}")
            return ''

    async def start_scraping(self):
        ''' Start the scraping process. '''
        scraped_data = []
        is_redis_connected: bool = await self.cache_manager.test_connection()

        # TODO_IF_TIME_PERMITS: Can be done in parallel using threads
        for page_num in range(1, self.page_limit + 1):
            page_url = f"https://dentalstall.com/shop/?page={page_num}"
            page_content = self.fetch_page(page_url)
            if page_content:
                html_content: str = page_content.text
                DataManager.save_html_content(self.req_id, html_content)
                products = ProductParser.parse_products(self.req_id, html_content)
                for product in products:
                    # Download image and update product with local path (if and only if the download was successful)
                    if product.get("path_to_image"):
                        local_image_path: str = self.download_image(product["path_to_image"])
                        if local_image_path:
                            product["path_to_image"] = local_image_path

                    # Check cache and only add products with updated prices
                    if is_redis_connected:
                        await self.cache_manager.is_price_changed(product)
                    scraped_data.append(product)

        # Save all scraped data at once to the JSON file
        DataManager.save_all_products(self.req_id, scraped_data)

        # Send notification
        self.notification_handler.notify(len(scraped_data))

        return scraped_data
