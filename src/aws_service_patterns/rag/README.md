# Retrieval-Augmented Generation (RAG) with AWS Bedrock

This module demonstrates Retrieval-Augmented Generation (RAG) using Amazon Bedrock's Knowledge Base and Claude model to answer questions based on your own data sources.

## Overview

The RAG module provides a Lambda handler that:
- Accepts questions as input
- Retrieves relevant information from an AWS Knowledge Base
- Uses Claude 3 Haiku model to generate contextual answers
- Returns the generated answer based on your proprietary knowledge base

## Project Structure

```
rag/
├── rag.py           # Main handler for RAG queries
└── rag_test.py      # Test script for local testing
```

## Key Components

### rag.py

**Main Function:**

- **`handler(event, context)`** - Lambda handler that processes RAG queries
  - Input: Event with JSON body containing "question" field
  - Output: HTTP response with generated answer or error message
  - Uses Bedrock Agent Runtime to execute retrieve_and_generate operation

**Configuration:**

```python
AWS_REGION_BEDROCK = "us-east-1"  # Bedrock service region
```

**Key Parameters:**

- **Knowledge Base ID**: `V29QV5PDZH` - Your configured knowledge base
- **Model**: `anthropic.claude-3-haiku-20240307-v1:0` - Claude 3 Haiku for fast inference
- **Type**: `KNOWLEDGE_BASE` - Storage type for retrieval

## How RAG Works

1. **Question Input** - User provides a question
2. **Retrieval** - Knowledge Base searches for relevant documents/passages
3. **Augmentation** - Retrieved context is combined with the question
4. **Generation** - Claude model generates an answer using the context
5. **Response** - Answer is returned to the user

## Configuration

### AWS Services Required

- **Amazon Bedrock**: For model access and agent runtime
- **Amazon Bedrock Knowledge Base**: For document storage and retrieval
- **AWS Lambda**: For serverless execution

### Bedrock Model

- **Model Name**: Claude 3 Haiku
- **Model ID**: `anthropic.claude-3-haiku-20240307-v1:0`
- **Region**: US East 1
- **Reasoning**: Fast, efficient model suitable for real-time question answering

### Knowledge Base Configuration

```python
{
    "type": "KNOWLEDGE_BASE",
    "knowledgeBaseConfiguration": {
        "knowledgeBaseId": "V29QV5PDZH",
        "modelArn": "arn:aws:bedrock:us-east-1::foundation-model/anthropic.claude-3-haiku-20240307-v1:0"
    }
}
```

## Usage

### Local Testing

Run the test script to verify the setup:

```bash
python rag_test.py
```

**Test Input:**
```json
{
  "body": "{\"question\": \"What does GDPR stand for?\"}"
}
```

**Example Output:**
```json
{
  "statusCode": 200,
  "body": "{\"answer\": \"GDPR stands for General Data Protection Regulation. It is a European Union regulation that protects personal data and privacy...\"}"
}
```

### Lambda Invocation

```bash
aws lambda invoke \
  --function-name RAGHandler \
  --payload '{"body":"{\"question\":\"What is the company privacy policy?\"}"}' \
  response.json
```

## Request/Response Examples

### Successful Request

```python
event = {
    "body": json.dumps({
        "question": "What are the main features of our product?"
    })
}
```

**Response:**
```python
{
    "statusCode": 200,
    "body": json.dumps({
        "answer": "Based on our documentation, the main features include..."
    })
}
```

### Error Request (Missing Question)

```python
event = {
    "body": json.dumps({
        # Missing "question" field
    })
}
```

**Response:**
```python
{
    "statusCode": 400,
    "body": json.dumps({
        "error": "question needed"
    })
}
```

## Dependencies

### AWS SDKs

- **boto3**: AWS SDK for Python
  - `bedrock-agent-runtime`: For RAG operations
- **botocore**: Low-level service library

## IAM Permissions Required

The Lambda execution role needs the following permissions:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "bedrock:InvokeModel",
        "bedrock:RetrieveAndGenerate"
      ],
      "Resource": "*"
    },
    {
      "Effect": "Allow",
      "Action": "bedrock-agent-runtime:RetrieveAndGenerate",
      "Resource": "*"
    },
    {
      "Effect": "Allow",
      "Action": "bedrock:Retrieve",
      "Resource": "arn:aws:bedrock:us-east-1::knowledge-base/V29QV5PDZH"
    }
  ]
}
```

## Setting Up a Knowledge Base

### Steps to Create a Knowledge Base

1. **Prepare Your Data**
   - Documents (PDF, TXT, DOCX)
   - Web URLs
   - Confluence/Notion pages
   - Database records

2. **Create Knowledge Base in AWS Console**
   - Navigate to Amazon Bedrock > Knowledge Base
   - Click "Create knowledge base"
   - Configure data source (S3, web crawler, etc.)
   - Select chunking strategy and chunk size

3. **Configure Embeddings**
   - Choose embedding model for semantic search
   - Select embedding dimension and model type

4. **Test Retrieval**
   - Use AWS Console to test queries
   - Verify relevant documents are retrieved

5. **Update Configuration**
   - Replace `V29QW5PDZH` with your Knowledge Base ID
   - Ensure model ARN matches your selected model

## Error Handling

Current implementation includes:

- Validates presence of "question" in request body
- Returns 400 status with error message if question is missing
- Returns 200 status with generated answer on success

**Recommended improvements:**
- Add try-catch for Bedrock API failures
- Add logging for debugging
- Implement retry logic for transient failures
- Add request validation and sanitization
- Handle knowledge base not found errors

## Performance Characteristics

- **Model**: Claude 3 Haiku (fast inference)
- **Typical Latency**: 2-5 seconds per query
- **Cost**: Lower cost per token compared to larger models
- **Accuracy**: Good balance between speed and quality

## Limitations

- Knowledge Base ID is hardcoded (not dynamic)
- Model selection is fixed to Claude 3 Haiku
- Only text-based questions supported
- No conversation history/context between requests
- Depends on Knowledge Base quality and content coverage
- Requires US East 1 region for Bedrock

## Advanced Features to Consider

- [ ] Multi-turn conversation with memory
- [ ] Dynamic model selection (Claude 3 Opus for complex queries)
- [ ] Custom chunking strategies
- [ ] Metadata filtering for retrieval
- [ ] Citation tracking (show source documents)
- [ ] Confidence scoring
- [ ] Query expansion and enhancement
- [ ] Fallback to general LLM when KB has no matches
- [ ] Monitoring and analytics dashboard
- [ ] Cost optimization with caching

## Troubleshooting

### Common Issues

**Knowledge Base Not Found**
```
Error: Could not find knowledge base: V29QW5PDZH
```
- Verify Knowledge Base ID is correct
- Check Knowledge Base is in US East 1
- Ensure IAM permissions include knowledge base access

**Model Not Available**
```
Error: Model not found: anthropic.claude-3-haiku-20240307-v1:0
```
- Verify model is available in your region
- Request model access in Bedrock console
- Check model name spelling

**No Relevant Documents Retrieved**
- Check Knowledge Base has data loaded
- Verify documents are properly indexed
- Try rephrasing the question
- Review chunking strategy in Knowledge Base settings

## References

- [AWS Bedrock Documentation](https://docs.aws.amazon.com/bedrock/)
- [Bedrock Knowledge Base Guide](https://docs.aws.amazon.com/bedrock/latest/userguide/knowledge-base.html)
- [Bedrock Agent Runtime API](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime.html)
- [Claude 3 Model Card](https://www.anthropic.com/research/claude)
- [boto3 Bedrock Documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agent-runtime.html)
- [RAG Best Practices](https://docs.aws.amazon.com/bedrock/latest/userguide/rag.html)

