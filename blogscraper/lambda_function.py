import json, boto3
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from blogscraper.spiders.blogcontent import BlogContent

s3 = boto3.client('s3')

def lambda_handler(event, context):
    body = json.loads(event['body'])
    start_url = body.get('start_url')

    if not start_url:
        return {
            'statusCode': 400,
            'headers': {
                'Content-Type': 'text/html'
            },
            'body': '<p>Error: start_url is required</p>'
        }
    
    process = CrawlerProcess(get_project_settings())

    results = []

    def store_result(item):
        results.append(item)

    process.crawl(BlogContent, start_urls = [start_url], result_processor=store_result)
    process.start()

    s3.put_object(
        Bucket='scrapedurlresult/urlscraped',
        Key=f'{start_url.replace("https://", "").replace("/", "_")}_scraped_url.json',
        Body=json.dumps(results)
    )

    return {
        'statusCode': 200,
        'headers': {
            'COntent-Type': 'text/html'
        },
        'body': f'<p>Submitted submitted URL: {start_url} for scraping.</p>'
    }