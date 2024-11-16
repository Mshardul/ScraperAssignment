'''
This module defines the data manager for the APIs.
'''

# External Imports
import os
import json

class DataManager:
    ''' A class to manage the data storage of products. '''

    @staticmethod
    def save_html_content(request_id, html_content):
        ''' Save HTML content to a file. '''
        # Create directory if it doesn't exist
        os.makedirs("data/html", exist_ok=True)

        # Generate a timestamp for the filename
        file_path = f"data/html/{request_id}.html"

        # Write HTML content to the file
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(html_content)

        print(f"utils/product_parse/save_html_content/file_path: {file_path}")

    @staticmethod
    def save_all_products(req_id, products):
        ''' Save all products to a JSON file. '''
        file_path = f"data/products/{req_id}.json"
        with open(file_path, "w", encoding="utf-8") as file:
            json.dump(products, file, indent=4)
