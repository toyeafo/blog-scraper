from datetime import datetime
import json
import boto3
import logging
from blogcontent import BlogContentScraper

logger = logging.getLogger()
logger.setLevel(logging.INFO)

s3 = boto3.client('s3')
dynamodb = boto3.client('dynamodb')

def lambda_handler(event, context):
    start_url = event.get('start_url')

    if not start_url:
        return {
            'statusCode': 400,
            'headers': {
                'Content-Type': 'text/html'
            },
            'body': '<p>Error: A valid URL is required</p>'
        }

    # Initialize the scraper
    scraper = BlogContentScraper(start_url)

    # Store results
    results = list(scraper.parse(start_url))

    s3_key = f'{start_url.replace("https://", "").replace("/", "_")}_scraped_blog.json'
    bucket_file_name = f'{start_url.replace("https://", "").replace("/", "_")}'
    # Save results to S3
    try:
        s3.put_object(
            Bucket='scrapedurlresult',
            Key=s3_key,
            Body=json.dumps(results)
        )
        logger.info(f"Successfully saved scraped data to S3 at {s3_key}")
    except Exception as e:
        logger.error(f"Failed to save data to S3: {e}")
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'text/html'
            },
            'body': '<p>Error saving data to S3</p>'
        }

    try:
        save_bucket_loc_to_dynamodb(start_url, s3_key, results, bucket_file_name)
    except Exception as e:
        logger.error(f"Failed to save bucket location to Database: {e}")
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'text/html'
            },
            'body': '<p>Error saving bucket location to Database</p>'
        }
    
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'text/html'
        },
        'body': f'<p>Submitted URL: {start_url} for scraping.</p>'
    }

def save_bucket_loc_to_dynamodb(url, s3_key, results, bucket_file_name):
    table_name = 'ScrapedBlogPost'
    current_date_time = datetime.now().strftime("%Y/%m/%d %H:%M:%S")

    item = {
        'URL': {'S': url},
        'Timestamp': {'S': str(current_date_time)},
        'S3Path': {'S': 'S3://scrapedurlresult/' + s3_key},
        'Title': {'S': bucket_file_name},
        'RecordCount': {'N': str(len(results))}
    }

    try:
        dynamodb.put_item(TableName=table_name, Item=item)
        logger.info(f"Successfully saved bucket location for {url} to DynamoDB.")
    except Exception as e:
        logger.error(f"Error saving bucket location to DynamoDB: {e}")
        raise