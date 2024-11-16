'''
This module defines the product parser for the APIs.
'''

# External Imports
from bs4 import BeautifulSoup

# Constants
PAGE_CURRENCY = "₹"
PRICE_ELEMENT_SELECTIONS: list[str] = [
    ".price ins .woocommerce-Price-amount",     # for discounted products
    ".price .woocommerce-Price-amount"          # for non-discounted products
]

class ProductParser:
    ''' A class to parse HTML content and extract product data. '''

    @staticmethod
    def parse_products(request_id, html_content):
        ''' Parse HTML content and extract product data. '''

        soup = BeautifulSoup(html_content, "html.parser")
        products = []

        product_list = soup.select(".products li.product")

        for product in product_list:
            # Extract product title
            title_element = product.select_one(".woo-loop-product__title a")
            product_title = title_element.text.strip() if title_element else "N/A"

            # Extract product price
            price_element = None
            for price_element_selection in PRICE_ELEMENT_SELECTIONS:
                if price_element:
                    break
                price_element = product.select_one(price_element_selection)
            product_price = 0.0
            if price_element:
                product_price = float(price_element.text.replace(PAGE_CURRENCY, "").replace(",", "").strip())

            # Extract product image
            image_element = product.select_one(".mf-product-thumbnail img")
            product_image = image_element["src"] if image_element else ""

            # Append extracted product data to the products list
            products.append({
                "product_title": product_title,
                "product_price": product_price,
                "path_to_image": product_image
            })

        return products
