import json
import boto3
from blogcontent import BlogContentScraper

s3 = boto3.client('s3')

def lambda_handler(event, context):
    start_url = event.get('start_url', 'https://support.funraisin.co/')

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
    results = list(scraper.parse(start_url))

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

