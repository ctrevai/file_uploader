import * as cdk from 'aws-cdk-lib';
import { BackedDataSource } from 'aws-cdk-lib/aws-appsync';
import { Construct } from 'constructs';
import { join } from 'path';

export class UploaderInfraStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    //Create an API Gateway REST API
    const api = new cdk.aws_apigateway.RestApi(this, 'API');

    // Create a DynamoDB table to store file metadata
    const filesTable = new cdk.aws_dynamodb.Table(this, 'Files', {
      partitionKey: { name: 'PK', type: cdk.aws_dynamodb.AttributeType.STRING },
      sortKey: { name: 'SK', type: cdk.aws_dynamodb.AttributeType.STRING },
      billingMode: cdk.aws_dynamodb.BillingMode.PAY_PER_REQUEST,
    });

    // Create an S3 bucket with CORS enabled
    const bucket = new cdk.aws_s3.Bucket(this, 'Bucket', {
      cors: [
        {
          allowedMethods: [
            cdk.aws_s3.HttpMethods.GET,
            cdk.aws_s3.HttpMethods.PUT,
            cdk.aws_s3.HttpMethods.POST,
            cdk.aws_s3.HttpMethods.DELETE,
          ],
          allowedOrigins: ['*'],
          allowedHeaders: ['*'],
        },
      ],
    });

    // Create a container lambda function to upload a file
    const uploadFileLambda = new cdk.aws_lambda.Function(this, 'UploadFileLambda', {
      runtime: cdk.aws_lambda.Runtime.PYTHON_3_12,
      handler: 'uploader.lambda_handler',
      code: cdk.aws_lambda.Code.fromAsset(join(__dirname, '../../src/upload-file-lambda/')),
      environment: {
        BUCKET_NAME: bucket.bucketName,
        TABLE_NAME: filesTable.tableName,
      },
    });

    filesTable.grantReadWriteData(uploadFileLambda);
    bucket.grantPut(uploadFileLambda);
    bucket.grantPutAcl(uploadFileLambda);

    //Plug the Lambda function into the API Gateway
    const uploadFileResource = api.root.addResource('uploadFile');

    uploadFileResource.addMethod('POST', new cdk.aws_apigateway.LambdaIntegration(uploadFileLambda));
    uploadFileResource.addCorsPreflight({
      allowOrigins: ['*'],
      allowMethods: ['POST'],
    });

    // Create a container lambda function to list files
    const listFilesLambda = new cdk.aws_lambda.Function(this, 'ListFilesLambda', {
      runtime: cdk.aws_lambda.Runtime.PYTHON_3_12,
      handler: 'listfiles.lambda_handler',
      code: cdk.aws_lambda.Code.fromAsset(join(__dirname, '../../src/list-files-lambda/')),
      environment: {
        BUCKET_NAME: bucket.bucketName,
        TABLE_NAME: filesTable.tableName,
      },
    });

    filesTable.grantReadWriteData(listFilesLambda);
    bucket.grantPut(listFilesLambda);
    bucket.grantPutAcl(listFilesLambda);

    //Plug the Lambda function into the API Gateway
    const listFilesResource = api.root.addResource('listFiles');
    listFilesResource.addMethod('GET', new cdk.aws_apigateway.LambdaIntegration(listFilesLambda));
    listFilesResource.addCorsPreflight({
      allowOrigins: ['*'],
      allowMethods: ['GET'],
    });




  }
}
