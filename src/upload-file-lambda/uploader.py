import boto3
import os

def lambda_handler(event, context):
    s3_client = boto3.client('s3')
    file_name = event.get("file_name")
    
    # Generate a presigned URL for the S3 object
    presigned_url = s3_client.generate_presigned_url(
        'put_object',
        Params={
            'Bucket': os.getenv('BUCKET_NAME'),
            'Key': file_name,
            'Expires': 30
        },
        HttpMethod='PUT',
    )
    
    # Return the presigned URL
    return {
        'statusCode': 200,
        'body': presigned_url
    }
    
    
    