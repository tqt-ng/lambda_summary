# lambda_summary

We use AWS Lambda and AWS Bedrock to summarize text documents. When a text file is uploaded to an S3 bucket, a Lambda function will be triggered to send the file content to a language model on AWS Bedrock. The language model will produce a summary of the content (including 3 keywords and a summary) which the Lambda function will output to another S3 bucket. 

This is a simplified version of the application built in the following course "Serverless LLM apps with Amazon Bedrock" by DeepLearning.AI https://www.deeplearning.ai/short-courses/.

Instructions:

1. Ensure you're in 'us-west-2' region. Please note we will use AWS Bedrock. See here for the supported regions https://docs.aws.amazon.com/bedrock/latest/userguide/bedrock-regions.html
2. In the AWS Bedrock console, request access for the model titan-text-express-v1.
3. Deploy lambda_function.py and prompt_template.txt as a Lambda function on AWS.
4. Create a Lambda layer and upload the lambda-bedrock-layer.zip.
5. Create two S3 buckets: input_bucket, output_bucket.
6. Add input_bucket as the trigger for the Lambda function, set output_bucket as an environment variable for the Lambda function, add the Lambda layer created above.
7. Ensure the Lambda function has the right permission to interact with AWS Bedrock and S3. A CloudFormation template lambda_role.yaml is included for your reference. You can use it to create the required role if needed.
8. Test by uploading a text file to input_bucket. 
