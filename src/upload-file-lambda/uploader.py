import boto3
import os
import json
s3_client = boto3.client('s3')
ddb_client = boto3.client('dynamodb')

def lambda_handler(event, context):
    #get event parameter
    body = event['body']
    user = json.loads(body)['user']
    file_name = json.loads(body)['filename']
    
    #get env variables
    bucket_name = os.getenv('BUCKET_NAME')
    table_name = os.getenv('TABLE_NAME')
    #print(event)
    #print(file_name)
    
    #create table entry
    ddb_client.put_item(
        TableName=table_name,
        Item={
            'userID': {'S': user},
            'fileName': {'S': file_name}
        }
    )
    
    #Generate a presigned URL for the S3 object
    response = s3_client.generate_presigned_post(
        bucket_name, 
        file_name, 
        ExpiresIn=300)
    print(response)
    # Return the presigned URL
    return {
        'statusCode': 200,
        'body': json.dumps(response)
    }
    
if __name__ == '__main__':
    event = {'body' : '{ "user": "localuser", "filename": "local_test.pdf"}'}
    response = lambda_handler(event, None)
    print(response)
    