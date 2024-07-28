import boto3
import os
import json
from boto3.dynamodb.conditions import Key
s3_client = boto3.client('s3')
ddb_client = boto3.client('dynamodb')
ddb_resource = boto3.resource('dynamodb')
table_name = os.getenv('TABLE_NAME')
table = ddb_resource.Table(table_name)


def lambda_handler(event, context):
    #get event parameters
    body = event['body']
    user = json.loads(body)['user']
    print(user)

    print(table_name)
    #get item from userID 
    response = table.query(
        KeyConditionExpression=Key('userID').eq(user)
    )
    
    print(response['Items'])
    
    return {
        'statusCode': 200,
        'body': json.dumps(response['Items'])
    }
    
if __name__ == '__main__':
    event = {'body' : '{ "user": "localuser"}'}
    print(lambda_handler(event, None))