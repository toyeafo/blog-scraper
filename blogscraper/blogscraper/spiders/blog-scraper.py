from typing import Any
import scrapy
from scrapy.http import Response
import pandas as pd

df = pd.read_csv('support.csv')
base_url = "https://support.funraisin.co"
urls = df['URL'].apply(lambda x: x if x.startswith('http') else base_url + x).drop_duplicates().to_list()

class BlogScraper(scrapy.Spider):
    name = "text_support"

    start_urls = urls

    def parse(self, response: Response, **kwargs: Any) -> Any:
        # Extract and strip the title
        title = response.xpath('//title/text()').get().strip() if response.xpath('//title/text()').get() else None
        
        # Extract and strip all text from the body
        body_texts = response.xpath('//body//*[not(self::script or self::style)]/text()').getall()
        stripped_texts = [text.strip() for text in body_texts if text.strip()]  # Strip and remove empty strings
        yield {
            'title': title,
            'post': stripped_texts, 
        }
        