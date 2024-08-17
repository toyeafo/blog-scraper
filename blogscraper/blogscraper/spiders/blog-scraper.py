from typing import Any
import scrapy
from scrapy.http import Response

class BlogScraper(scrapy.Spider):
    name = "support"

    start_urls = [
        'https://support.funraisin.co/blog/',
    ]

    def parse(self, response: Response, **kwargs: Any) -> Any:
        for post in response.css('div.blogItems a::attr(href)').getall():
            # yield {
            #     'Blog Title': post.css('div#blogIntro h3').getall(),
            #     'author': 'Funraisin',
            # }
            yield response.follow(post, callback=self.parse_articles)

        next_post = response.css('div#paginate a::attr(href)').get()
        if next_post is not None:
            yield response.follow(next_post, self.parse)

    def parse_articles(self, response: Response, **kwargs: Any) -> Any:
        for post in response.css('html'):
             # Extract and strip the title
            title = post.css('head title::text').get().strip() if post.css('head title::text').get() else None
        
            # Extract and strip all text from the body
            body_texts = post.css('body p::text, body h1::text').getall()
            stripped_texts = [text.strip() for text in body_texts if text.strip()]  # Strip and remove empty strings
            yield {
                'title': title,
                'post': stripped_texts, 
            }