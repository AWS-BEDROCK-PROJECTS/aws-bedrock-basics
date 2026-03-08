import boto3
import json
from langchain_aws import ChatBedrock
from langchain_core.prompts import ChatPromptTemplate

AWS_REGION_BEDROCK = "us-east-1"

client = boto3.client(service_name="bedrock-runtime", region_name=AWS_REGION_BEDROCK)

model = ChatBedrock(
    model_id="amazon.nova-lite-v1:0",
    client=client
)

def handler(event, context):
    body = json.loads(event["body"])
    text = body.get("text")
    points = event["queryStringParameters"]["points"]
    if text and points:
        prompt = ChatPromptTemplate.from_template(
        "Write a summary for {text} in {points} points."
        )
        chain = prompt | model
        response = chain.invoke({"text": text, "points": points})
        response_content = response.content
        #print(response_content)
        return {
            "statusCode": 200,
            "body": json.dumps({"summary": response_content}),        
        }
    return {
        "statusCode": 400,
        "body": json.dumps({"error": "text and points required!"}),  
    }