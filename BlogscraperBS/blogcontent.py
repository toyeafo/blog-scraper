import requests
from bs4 import BeautifulSoup

class BlogContentScraper:
    def __init__(self, start_url):
        self.start_url = start_url

    def fetch_page(self, url):
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status() 
            return response.content
        except requests.RequestException as e:
            print(f"Failed to retrieve {url}: {e}")
            return None

    def parse(self, url):
        page_content = self.fetch_page(url)
        if page_content is None:
            return

        soup = BeautifulSoup(page_content, 'html.parser')

        links = soup.find_all('a', href=True)
        blog_links = [link['href'] for link in links if '/blog/' in link['href']]

        for post_url in blog_links:
            absolute_url = post_url if post_url.startswith('http') else self.start_url + post_url
            yield from self.parse_blog(absolute_url)

       
        next_page = soup.find('a', href=True, string=lambda x: '/blog/' in x if x else False)
        if next_page:
            next_page_url = next_page['href']
            absolute_next_page = next_page_url if next_page_url.startswith('http') else self.start_url + next_page_url
            yield from self.parse(absolute_next_page)
        else:
            print("No additional blog pages found to follow.")

    def parse_blog(self, post_url):
        page_content = self.fetch_page(post_url)
        if page_content is None:
            return

        soup = BeautifulSoup(page_content, 'html.parser')

        # Extract the title
        title = soup.title.string.strip() if soup.title else 'No Title'

        # Extract the body text (excluding scripts and styles)
        body_elements = soup.find_all(text=True)
        body_text = []
        for element in body_elements:
            if element.parent.name not in ['script', 'style'] and element.strip():
                body_text.append(element.strip())

        # Process the results
        yield {
            'URL': post_url,
            'title': title,
            'post': body_text
        }

# if __name__ == '__main__':
#     start_url = 'https://support.funraisin.co/'
#     scraper = BlogContentScraper(start_url)
#     scraper.parse(start_url)
