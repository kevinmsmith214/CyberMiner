import json
import boto3

# Initialize DynamoDB client
dynamodb = boto3.resource('dynamodb')

# Name of your DynamoDB table
table_name = 'CYBERMINER-DB'
table = dynamodb.Table(table_name)



def lambda_handler(event, context):
    # parse event string
    if isinstance(event, str):
        event = json.loads(event)
    
    # If triggered by API Gateway with a body, extract 'body' and load it as JSON
    if 'body' in event:
        data = json.loads(event['body'])
    else:
        data = event  # This assumes the event is the list of records directly if not from API Gateway

    idx = 0
    # Prepare the batch items
    with table.batch_writer() as batch:
        for record in data:
            # Add each item to the DynamoDB table
            batch.put_item(
                Item={
                    'Title': record['title'],  # Ensure these keys match the case in your JSON
                    'URL': record['url']
                }
            )
            idx += 1

    # Return a success message
    return {
        'statusCode': 200,
        'body': json.dumps(f'Batch write successful! {idx} items')
    }