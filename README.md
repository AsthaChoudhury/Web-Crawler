# WebCrawler

WebCrawler is a Python-based web crawler designed to fetch, filter, and analyze links and metadata from a specified domain. It follows basic web crawling ethics by respecting the `robots.txt` file and avoiding disallowed paths.

---

## Features
- Fetches all hyperlinks from a target website.
- Extracts metadata like titles and descriptions from pages.
- Filters out unnecessary links such as images, CSS, JS, and PDFs.
- Respects `robots.txt` restrictions and avoids disallowed URLs.
- Tracks response times, total pages crawled, and skipped URLs.
- Exports all collected links to a CSV file.

---

## Prerequisites
Before running the project, ensure to run the following:
- The required Python libraries (install using `pip install -r requirements.txt`).

---

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/AsthaChoudhury/Web-Crawler.git
   cd Web-Crawler
2. Install the required dependencies:
    ```
    pip install -r requirements.txt

  ---

## Usage
1. Run the script:
   ```bash
   python web_crawler.py
2. Enter the target domain:
    ```
    Enter the domain >> https://example.com

---

## Configuration
1- Crawl Depth: Adjust the maximum depth of crawling by modifying the           max_depth parameter in the crawl function (default: 2).
2- Crawl Delay: Modify the crawl_delay variable to set a delay (in seconds)     between crawling consecutive links (default: 1 second).
3- File Extensions to Skip: Update the list of extensions in the                filter_links function to exclude additional types.
`
