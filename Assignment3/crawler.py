import urllib.request
import urllib.parse
from bs4 import BeautifulSoup
from pymongo import MongoClient
from urllib.error import URLError, HTTPError
import re


class Frontier:
    def __init__(self):
        self.urls = set()
        self.visited = set()
        self.target_found = False

    def addURL(self, url):
        if url not in self.visited:
            self.urls.add(url)

    def nextURL(self):
        if not self.done():
            url = self.urls.pop()
            self.visited.add(url)
            return url
        return None

    def done(self):
        return len(self.urls) == 0 or self.target_found

    def clear_frontier(self):
        self.urls.clear()
        self.target_found = True


def normalize_url(base_url, url):
    try:
        # Remove any whitespace
        url = url.strip()

        # Skip invalid URLs and social media sharing links
        if not url or 'twitter.com' in url or 'facebook.com' in url or 'linkedin.com' in url:
            return None

        # Handle relative URLs
        if url.startswith('/'):
            return urllib.parse.urljoin(base_url, url)
        elif not url.startswith('http'):
            return urllib.parse.urljoin(base_url, '/' + url)

        # Encode URL properly
        parsed = urllib.parse.urlparse(url)
        return urllib.parse.urlunparse((
            parsed.scheme,
            parsed.netloc,
            urllib.parse.quote(parsed.path),
            parsed.params,
            parsed.query,
            parsed.fragment
        ))
    except Exception as e:
        print(f"Error normalizing URL {url}: {e}")
        return None


def is_valid_url(url):
    if not url:
        return False

    # Check if URL is within cpp.edu domain and is HTML/SHTML
    return ('cpp.edu' in url and
            not any(ext in url.lower() for ext in ['.pdf', '.jpg', '.png', '.gif', '.css', '.js']) and
            not any(pattern in url.lower() for pattern in ['javascript:', 'mailto:', 'tel:', '#']))


def retrieveHTML(url):
    try:
        # Encode URL if it contains spaces or special characters
        encoded_url = urllib.parse.quote(url, safe=':/?=&')

        headers = {'User-Agent': 'Mozilla/5.0'}
        request = urllib.request.Request(encoded_url, headers=headers)

        try:
            response = urllib.request.urlopen(request, timeout=10)
            return response.read().decode('utf-8')
        except UnicodeDecodeError:
            # Try different encoding if utf-8 fails
            return response.read().decode('latin-1')

    except (URLError, HTTPError) as e:
        print(f"Error retrieving {url}: {e}")
        return None
    except Exception as e:
        print(f"Unexpected error retrieving {url}: {e}")
        return None


def target_page(soup):
    # Check for the specific heading that indicates the target page
    h1_tag = soup.find('h1', class_='cpp-h1')
    return h1_tag and 'Permanent Faculty' in h1_tag.text


def parse(html, base_url):
    if not html:
        return [], False

    soup = BeautifulSoup(html, 'html.parser')
    urls = []

    # Extract all links
    for link in soup.find_all('a', href=True):
        url = link['href']
        normalized_url = normalize_url(base_url, url)
        if normalized_url and is_valid_url(normalized_url):
            urls.append(normalized_url)

    return urls, target_page(soup)


def storePage(url, html, db):
    if html:
        db.pages.insert_one({
            'url': url,
            'html': html,
            'is_target': target_page(BeautifulSoup(html, 'html.parser'))
        })


def flagTargetPage(url, db):
    db.pages.update_one(
        {'url': url},
        {'$set': {'is_target': True}}
    )


def crawlerThread(frontier, db):
    while not frontier.done():
        url = frontier.nextURL()
        print(f"Crawling: {url}")

        html = retrieveHTML(url)
        storePage(url, html, db)

        if html:
            urls, is_target = parse(html, url)

            if is_target:
                print(f"Target page found: {url}")
                flagTargetPage(url, db)
                frontier.clear_frontier()
            else:
                for new_url in urls:
                    frontier.addURL(new_url)


def main():
    # Connect to MongoDB
    client = MongoClient('mongodb://localhost:27017/')
    db = client['cs_faculty_db']

    # Initialize frontier with CS home page
    frontier = Frontier()
    frontier.addURL('https://www.cpp.edu/sci/computer-science/')

    # Start crawling
    crawlerThread(frontier, db)


if __name__ == "__main__":
    main()