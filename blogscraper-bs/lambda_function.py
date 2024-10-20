import json
import boto3
from blogcontent import BlogContentScraper

s3 = boto3.client('s3')

def lambda_handler(event, context):
    # Get the start URL from the event or use a default
    start_url = event.get('url', 'https://support.funraisin.co/')

    if not start_url:
        return {
            'statusCode': 400,
            'headers': {
                'Content-Type': 'text/html'
            },
            'body': '<p>Error: start_url is required</p>'
        }

    # Initialize the scraper
    scraper = BlogContentScraper(start_url)

    # Store results
    results = []

    # Custom logic to collect results from the scraper
    class ResultCollector:
        def __init__(self):
            self.results = []

        def collect(self, data):
            self.results.append(data)

    collector = ResultCollector()

    # Run the scraper and collect the results
    scraper.parse(start_url)

    # Simulate storing results (in real scraper, you'd use yield instead of print)
    # Example structure of collected data
    results.append({
        'url': start_url,
        'results': collector.results
    })

    # Save results to S3
    s3.put_object(
        Bucket='scrapedurlresult',
        Key=f'{start_url.replace("https://", "").replace("/", "_")}_scraped_blog.json',
        Body=json.dumps(results)
    )

    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'text/html'
        },
        'body': f'<p>Submitted URL: {start_url} for scraping.</p>'
    }

