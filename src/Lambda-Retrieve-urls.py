import json
import boto3

# Initialize a DynamoDB client
dynamodb = boto3.resource('dynamodb')

def lambda_handler(event, context):
    # DynamoDB table name
    table_name = 'CYBERMINER-DB'
    table = dynamodb.Table(table_name)
    
    # Read the list of titles from the API request body
    titles = json.loads(event['body'])['titles']
    
    results = []
    
    # Query DynamoDB for each title
    for title in titles:
        response = table.get_item(Key={'Title': title})
        if 'Item' in response:
            results.append({'title': title, 'url': response['Item']['URL']})
        else:
            results.append({'title': title, 'url': 'Not found'})
    
    # Return the results
    return {
        'statusCode': 200,
        'body': json.dumps(results),
        'headers': {
            'Content-Type': 'application/json'
        }
    }
