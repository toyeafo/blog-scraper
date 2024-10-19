import scrapy
from scrapy.http import Response
import requests
import pandas as pd
from typing import Any


# Utility function to generate valid URLs from raw data
# def generate_valid_url(url_data, base_url):
#     df = pd.read_json(url_data)
#     urls = df['URL'].apply(lambda x: x if x.startswith('http') else base_url + x).drop_duplicates().to_list()
#     valid_urls = [url for url in urls if is_valid_url(url)]
#     return valid_urls


# Combined Spider that performs both URL scraping and blog content extraction
class BlogContent(scrapy.Spider):
    name = "url_content_scraper"

    start_urls = ['https://support.funraisin.co/']

    def parse(self, response: Response):
        # Extract all URLs containing '/blog/' from the response
        blog_urls = response.xpath('//a[contains(@href, "/blog/")]/@href').getall()

        for post_url in blog_urls:
            # Yield each blog URL and follow the URL to parse the blog content
            full_url = response.urljoin(post_url)
            yield scrapy.Request(full_url, callback=self.parse_blog)

        # Handle pagination or next page if needed
        next_page = response.xpath('//a[contains(@href, "/blog/")]/@href').get()
        if next_page:
            yield response.follow(next_page, self.parse)

    def parse_blog(self, response: Response):
        # Extract and strip the title
        title = response.xpath('//title/text()').get().strip() if response.xpath('//title/text()').get() else None

        # Extract and strip all text from the body
        body_texts = response.xpath('//body//*[not(self::script or self::style)]/text()').getall()
        stripped_texts = [text.strip() for text in body_texts if text.strip()]

        # Yield the title and content for each blog post
        yield {
            'URL': response.url,
            'title': title,
            'post': stripped_texts,
        }
