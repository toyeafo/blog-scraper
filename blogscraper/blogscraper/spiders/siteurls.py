from typing import Any
import scrapy
from scrapy.http import Response

class SiteUrlScraper(scrapy.Spider):
    name = "SupportURL"

    start_urls = [
        'https://support.funraisin.co/',
    ]

    def parse(self, response: Response, **kwargs: Any) -> Any:
        for post in response.xpath('//a[contains(@href, "/blog/")]/@href').getall():
            yield {
                'URL': post, 
            }

        next_post = response.xpath('//a[contains(@href, "/blog/")]/@href').get()
        if next_post is not None:
            yield response.follow(next_post, self.parse)