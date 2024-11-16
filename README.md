# ScraperAssignment
Web Scraper using FastAPI and Redis

# Requirements
[Requrement Document](https://goatlys.notion.site/BE-engineer-testing-assigment-f1890cf18af343f7b737ee95575f98dd)

# Technologies Used 
- Web Framework: FastAPI
- Caching: Redis

# API Endpoints
### User
- `/login`
    - Dummy Endpoint to return an OAuth Token
    - `{"access_token": FAKE_TOKEN, "token_type": "bearer"}`
### Scraping
- `/scrape`
    - Endpoint to scrape the webpage, with 2 optional parameters
    - `{"page_limit": 1, "proxy_string": ""}`

# Scraping Flow
1. Request `GET /scrape` with `page_limit` and `proxy_string` parameters
    - `page_limit` defaults to 1
    - `proxy_string` defaults to empty string // NOT YEST TESTED
2. For each of the webpages,
    1. Scrape the webpage using [Scraper Manager](#scraper-manager)
    2. For each of the parserd products,
        1. Download image locally
        2. Update Product JSON with local path
        3. Update Cache with product details using [Cache Manager](#cache-manager)
3. Save all the products at once to the JSON file using [Data Manager](#data-manager)
4. Send notifications using [Notification Handler](#notification-handler)

# Scope Restrictions
- `/login` just retruns the access token, irrespective of whether the credentials are valid or not.
- `/scrape` requires a valid access token, which will be provided by calling the `/login` endpoint.
- `/scrape` only allows 1 page at a time for now. Utilize threads for and parallel execution.
- `proxy_string` is not yet tested. Tried random proxies online, but got TimeOut errors.

# Directory Structure
- `data`: contains the scraped data. categoriezed by type: html, images, products
- `routers`: contains the routers. categoriezed by type: authentication, scrapper
- `utils`: contains the different helper classes: cache, dta, notification, product parser, request, scraper etc

# Helper Classes

## Cache Manager
- sets up Redis Client for caching.
- ability to test if Redis is up and running.
- ability to update the cache (if outdated) with the latest price.
- fetching data from Redis is out of scope of this project.

## Data Manager
- saves the html content of the product page scrapped to a file.
- saves the final products json to a file.
- can be extended to save the data to a database.

## Notification Handler
- prints the number of products scrapped to the console.
- can be extended to implement different notification services including emails, text messages etc.

## Product Parser
- ability to parse the HTML content to get the product lists
- this is the code that needs to be changed if the page structure changes, or a new website is added.

## Request Manager
- gets a `request_id` for a particular Scrape request.
- This `request_id` is then used for naming the files (html, images, and scraped json).

## Scraper Manager
- ability to fetch the entire page of the website.
- ability to download an image from a given `image_url`
- ability to start the scraping process
    - download the entire html of the webpage
    - parse the html to get the list of products
    - download the images and update the products with local path
    - update the cache
    - save the products to the json file
    - send notifications

# Tasks

- [x] **Authentication:** Authenticate using a static token
- [x] **Scrapper:** Scrape product name, price, and image.
- [x] **Scrapper:** Enable multi-page structure.
- [x] **Scrapper:** Test with number of pages query parameter.
- [ ] **Scrapper:** Test with proxy string query parameter.
- [x] **Scrapper:** Retry Mechanism
- [x] **Data Storage:** Store the Products JSON in a file locally.
- [x] **Notification Service:** Print the number of Products scrapped
- [x] **Coding Guidelines:** Use OOP for all helper classes
- [x] **Caching:** Impelement Caching using Redis

# Screenshots
### API
- **User Login**
    - ![User Login](./screenshots/API%20-%20login.png)
- **Scraping**
    - ![Scraping](./screenshots/API%20-%20scrape.png)
### Caching
- **Redis**
    - ![Redis](./screenshots/Caching%20-%20Redis.png)