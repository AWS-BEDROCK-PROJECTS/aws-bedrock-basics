import boto3
import json

AWS_REGION_BEDROCK = "us-east-1"

client = boto3.client(
    service_name="bedrock-agent-runtime", region_name=AWS_REGION_BEDROCK
)

def handler(event, context):
    body = json.loads(event["body"])
    question = body.get("question")
    if question:
        response = client.retrieve_and_generate(
            input={"text": question},
            retrieveAndGenerateConfiguration={
                "type": "KNOWLEDGE_BASE",
                "knowledgeBaseConfiguration": {
                    "knowledgeBaseId": "V29QV5PDZH",
                    "modelArn": "arn:aws:bedrock:us-east-1::foundation-model/anthropic.claude-3-haiku-20240307-v1:0",
                },
            },
        )
        answer = response.get("output").get("text")
        return {
            "statusCode": 200,
            "body": json.dumps({"answer": answer}),
        }
    return {
            "statusCode": 400,
            "body": json.dumps({"error": "question needed"}),
        }