import boto3
import os
import json
from jinja2 import Template

s3_client = boto3.client('s3')
bedrock_runtime = boto3.client('bedrock-runtime', 'us-west-2')

def lambda_handler(event, context):
    
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']
    
    if ".txt" not in key: 
        print("This app only works with .txt files.")
        return

    try: 

        file_content = ""
        
        response = s3_client.get_object(Bucket=bucket, Key=key)
        
        file_content = response['Body'].read().decode('utf-8')

        print(f"Successfully read file {key}.")
        
        summary = bedrock_summarization(file_content)
        
        s3_client.put_object(
            Bucket=os.environ['OUTPUT_BUCKET'],
            Key=f"result-{key}",
            Body=summary,
            ContentType='text/plain'
        )
        
    except Exception as e:
        print(f"Error: {e}")
        return {
            'statusCode': 500,
            'body': json.dumps(f"Error: {e}")
        }

    return {
        'statusCode': 200,
        'body': json.dumps(f"Successfully summarized file {key}. Summary: {summary}")
    }
        

def bedrock_summarization(file_content):
    
    with open('prompt_template.txt', "r") as file:
        template_string = file.read()

    data = {
        'text': file_content,
    }
    
    template = Template(template_string)
    prompt = template.render(data)
    
    print(prompt)
    
    kwargs = {
        "modelId": "amazon.titan-text-express-v1",
        "contentType": "application/json",
        "accept": "*/*",
        "body": json.dumps(
            {
                "inputText": prompt,
                "textGenerationConfig": {
                    "maxTokenCount": 2048,
                    "stopSequences": [],
                    "temperature": 0,
                    "topP": 0.9
                }
            }
        )
    }
    
    response = bedrock_runtime.invoke_model(**kwargs)

    summary = json.loads(response.get('body').read()).get('results')[0].get('outputText')    
    return summary
    