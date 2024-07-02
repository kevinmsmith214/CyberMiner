import json
import boto3
from boto3.dynamodb.conditions import Key

'''
Expected input:
{
    "action":"login",
    "username":"YIA180000",
    "password":"login123",
    "user_type":"Admin"
}
    
'''


def lambda_handler(event, context):
    # DynamoDB setup
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('CYBERMINER-USERS')
    
    # Extract details from event
    action = json.loads(event['body'])['action']
    username = json.loads(event['body'])['username']
    password = json.loads(event['body'])['password']
    user_type = json.loads(event['body'])['user_type']

    print(f"{action}, {username}, {password}, {user_type}")
    # Basic validation
    if action == 'login' and username and password:
        # Query DynamoDB for the username
        response = table.get_item(Key={'Username': username})
        
        # Check if user exists
        if 'Item' in response:
            stored_password = response['Item']['Password']
            stored_user_type = response['Item']['UserType']
            
            # Validate password and user type
            if password == stored_password and user_type == stored_user_type:
                if response['Item']['UserType'] == "Admin":
                    return {
                        'statusCode': 200,
                        'body': json.dumps('Admin login successful!')
                    }
                if response['Item']['UserType'] == "Advertiser":
                    return {
                        'statusCode': 201,
                        'body': json.dumps('Advertiser login successful')
                    }
            else:
                return {
                    'statusCode': 403,
                    'body': json.dumps('Invalid username, user type or password.')
                }
        else:
            return {
                'statusCode': 404,
                'body': json.dumps('Username does not exist.')
            }
    else:
        return {
            'statusCode': 400,
            'body': json.dumps('Invalid request.')
        }

