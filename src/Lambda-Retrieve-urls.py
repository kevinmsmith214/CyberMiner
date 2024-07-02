import json
import boto3
from boto3.dynamodb.conditions import Attr

def lambda_handler(event, context):
    # Initialize a DynamoDB client
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('CYBERMINER-DB')
    
    # Parse the input query and mode from the API request body
    query = json.loads(event['body'])['query']
    mode = json.loads(event['body'])['mode']
    
    query_words = query.split()
    scan_kwargs = {}
    
    # Prepare the filter expression based on the search mode
    if mode == "OR":
        filter_expression = Attr('Title').contains(query_words[0])
        for word in query_words[1:]:
            filter_expression = filter_expression | Attr('Title').contains(word)
    elif mode == "AND":
        filter_expression = Attr('Title').contains(query_words[0])
        for word in query_words[1:]:
            filter_expression = filter_expression & Attr('Title').contains(word)
    elif mode == "NOT":
        filter_expression = ~Attr('Title').contains(query_words[0])
        for word in query_words[1:]:
            filter_expression = filter_expression & ~Attr('Title').contains(word)
    else:
        return {
            'statusCode': 400,
            'body': json.dumps('Invalid search mode specified')
        }

    # Perform the scan operation with the filter expression
    scan_kwargs['FilterExpression'] = filter_expression
    response = table.scan(**scan_kwargs)
    
    results = [{'title': item['Title'], 'url': item.get('URL', 'Not found')} for item in response.get('Items', [])]

    # Return the results
    return {
        'statusCode': 200,
        'body': json.dumps(results),
        'headers': {
            'Content-Type': 'application/json'
        }
    }
