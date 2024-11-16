""" main.py """

# External Imports
import os
from fastapi import FastAPI
from routers import authentication, scrapper

# data directory setup
def initialize_directories():
    """Create necessary data directories if they don't exist."""
    # TODO_IF_TIME_PERMITS: Move to env variables
    directories: list[str] = ["data/html", "data/products", "data/images"]
    for directory in directories:
        os.makedirs(directory, exist_ok=True)

# Call the function to set up directories
initialize_directories()

# app initialization
app = FastAPI()

# include routers
app.include_router(authentication.router)
app.include_router(scrapper.router)
