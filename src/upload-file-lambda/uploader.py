import boto3
import os
import json
s3_client = boto3.client('s3')

def lambda_handler(event, context):
    body = event['body']
    user = json.loads(body)['user']
    file_name = json.loads(body)['filename']
    bucket_name = os.getenv('BUCKET_NAME')
    table_name = os.getenv('TABLE_NAME')
    #print(event)
    #print(file_name)
    
    #Generate a presigned URL for the S3 object
    presigned_url = s3_client.generate_presigned_url(
        'put_object',
        Params={
            'Bucket': bucket_name,
            'Key': file_name,
            'Expires': 30
        },
        HttpMethod='PUT',
    )
    response = {'user': str(user), 'filename': str(file_name), 'uploadurl': presigned_url}
    
    # Return the presigned URL
    return {
        'statusCode': 200,
        'body': json.dumps(response)
    }
    
if __name__ == '__main__':
    event = {'body' : '{ "user": "localuser", "filename": "local_test.pdf"}'}
    print(lambda_handler(event, None))
    