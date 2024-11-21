import requests
import re
import time
from urllib.parse import urljoin, urlparse
from fake_useragent import UserAgent
import pandas as pd
from bs4 import BeautifulSoup

# Input domain for crawling
url = input("Enter the domain >> ")
links = []
total_pages_crawled = 0
total_response_time = 0
skipped_urls = 0


def rotate_user_agent():
    ua = UserAgent()
    return ua.random

# Function for extracting links from the target website


def extract_content(response):
    soup = BeautifulSoup(response.text, 'html.parser')
    title = soup.find('title').text if soup.find('title') else 'No Title'
    description = soup.find('meta', attrs={'name': 'description'})
    description = description['content'] if description else 'No Description'
    return title, description


def extract_links_from(url):
    try:
        headers = {"User-Agent": rotate_user_agent()}
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        print(f"Fetching URL: {url}")

        title, description = extract_content(response)
        print(f"Title: {title}")
        print(f"Description: {description}")

        found_links = re.findall(r'href=[\'"]?([^\'" >]+)', response.text)
        print(f"Found links: {found_links}")
        return found_links
    except requests.RequestException as e:
        print(f"Failed to fetch URL: {url}, error: {e}")
        return []

# Function for filtering links


def filter_links(links):
    filtered_links = []
    for link in links:
        # Remove links with unwanted file extensions
        if not link.endswith((".jpg", ".png", ".css", ".js", ".pdf")):
            filtered_links.append(link)
    return filtered_links

# Function for fetching robots.txt file


def fetch_robots_txt(url):
    robots_txt_url = urljoin(url, "robots.txt")
    try:
        response = requests.get(robots_txt_url)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        print(f"Failed to fetch robots.txt: {e}")
        return None

# Function for parsing robots.txt file


def parse_robots_txt(robots_txt):
    disallowed_urls = []
    for line in robots_txt.splitlines():
        if line.lower().startswith("disallow:"):
            disallowed_url = line.split(":", 1)[1].strip()
            disallowed_urls.append(disallowed_url)
    return disallowed_urls

# Function for checking if a URL is disallowed


def is_disallowed(url, disallowed_urls):
    parsed_url = urlparse(url)
    path = parsed_url.path
    for disallowed in disallowed_urls:
        if path.startswith(disallowed):
            return True
    return False

# Function for storing links


def store_links(links):
    df = pd.DataFrame(links, columns=["link"])
    df.to_csv("links.csv", index=False)

# Function for crawling


def crawl(target_url, disallowed_urls, max_depth=2, current_depth=0):
    global total_pages_crawled, total_response_time, skipped_urls
    if current_depth > max_depth:
        return

    print(f"Crawling URL: {target_url}, Depth: {current_depth}")
    start_time = time.time()  # Start measuring response time
    href_links = extract_links_from(target_url)
    end_time = time.time()
    response_time = end_time - start_time
    total_response_time += response_time
    print(f"Response Time for {target_url}: {response_time:.2f} seconds")

    filtered_links = filter_links(href_links)

    for link in filtered_links:
        full_link = urljoin(target_url, link)
        full_link = full_link.split("#")[0]  # Remove fragments

        if full_link not in links and not is_disallowed(full_link, disallowed_urls):
            total_pages_crawled += 1
            links.append(full_link)
            print(f"Appending link: {full_link}")  # Debugging statement
            time.sleep(crawl_delay)
            crawl(full_link, disallowed_urls, max_depth, current_depth + 1)

        else:
            skipped_urls += 1

    print(f"Total pages crawled: {total_pages_crawled}")
    if total_pages_crawled > 0:
        average_response_time = total_response_time / total_pages_crawled
    else:
        average_response_time = 0
    print(f"Average response time: {average_response_time:.2f} seconds")
    print(f"Skipped URLs: {skipped_urls}")
    print(f"Remaining pages: {len(links) - total_pages_crawled}")


# Crawl delay
crawl_delay = 1  # seconds

# Exit
try:
    robots_txt = fetch_robots_txt(url)
    disallowed_urls = []
    if robots_txt:
        disallowed_urls = parse_robots_txt(robots_txt)
        print(f"Disallowed URLs: {disallowed_urls}")

    crawl(url, disallowed_urls)
    print("Crawling completed. Links found:")
    store_links(links)
    for link in links:
        print(link)
except KeyboardInterrupt:
    print("\rCtrl+C detected... Quitting...!!!")
    exit(0)
