import scrapy
from scrapy.http import Response
from scrapy.linkextractors import LinkExtractor


class BlogContent(scrapy.Spider):
    name = "url_content_scraper"

    # start_urls = ['']

    def parse(self, response: Response):
        link_extractor = LinkExtractor(allow=('/blog/',))
        links = link_extractor.extract_links(response)

        for post_url in links:
            yield scrapy.Request(post_url.url, callback=self.parse_blog)

        next_page = response.xpath('//a[contains(@href, "/blog/")]/@href').get()
        if next_page:
            yield response.follow(next_page, self.parse)

    def parse_blog(self, response: Response):
        title = response.xpath('//title/text()').get()
        if title:
            title = title.strip()

        body_texts = response.xpath('//body//*[not(self::script or self::style)]/text()').getall()
        stripped_texts = [text.strip() for text in body_texts if text.strip()]

        yield {
            'URL': response.url,
            'title': title,
            'post': stripped_texts,
        }
