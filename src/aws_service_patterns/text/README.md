# Text Summarization with AWS Bedrock

This module demonstrates text summarization using Amazon Bedrock's Nova Lite model integrated with LangChain to create concise summaries of any text content.

## Overview

The text summarization module provides a Lambda handler that:
- Accepts text content and desired summary format as input
- Uses LangChain with AWS Bedrock to process the text
- Invokes Amazon's Nova Lite model for efficient summarization
- Returns a concise summary with a specified number of key points
- Optimized for fast, cost-effective summarization tasks

## Project Structure

```
text/
├── summary_lambda.py          # Main handler for text summarization
├── summary_lambda_test.py      # Test script with sample data
└── iaac/                       # Infrastructure as Code (CDK)
    ├── app.py                  # CDK application entry point
    ├── iaac_stack.py           # CDK stack definition
    ├── requirements.txt        # CDK dependencies
    ├── requirements-dev.txt    # Development dependencies
    ├── cdk.json                # CDK configuration
    ├── source.bat              # Windows environment setup
    ├── services/               # Lambda layer with dependencies
    │   ├── boto3/
    │   ├── langchain_aws/
    │   ├── langchain_core/
    │   └── ... (other dependencies)
    └── tests/                  # CDK unit tests
```

## Key Components

### summary_lambda.py

**Main Function:**

- **`handler(event, context)`** - Lambda handler for summarization requests
  - Input: 
    - JSON body with "text" field (content to summarize)
    - Query parameter "points" (number of summary points)
  - Output: HTTP response with generated summary

**Key Features:**

- **LangChain Integration**: Uses LangChain to build prompt chains
- **Dynamic Prompts**: Creates customizable prompts based on input parameters
- **Model Invocation**: Chains prompt template with Bedrock model

**Workflow:**

```python
1. Parse input (text and points)
2. Create prompt template: "Write a summary for {text} in {points} points."
3. Chain prompt with ChatBedrock model
4. Invoke chain with parameters
5. Extract and return summary content
```

## Configuration

### Environment Variables

```python
AWS_REGION_BEDROCK = "us-east-1"  # Bedrock service region
```

### Bedrock Model

- **Model Name**: Amazon Nova Lite
- **Model ID**: `amazon.nova-lite-v1:0`
- **Region**: US East 1
- **Reasoning**: Lightweight, fast model optimized for text processing tasks
- **Cost**: Cost-effective for high-volume summarization

### LangChain Components Used

- **ChatBedrock**: Interface to interact with Bedrock models
- **ChatPromptTemplate**: Dynamic prompt construction with parameters

## Usage

### Local Testing

Run the test script with sample text:

```bash
python summary_lambda_test.py
```

**Test Input:**
```json
{
  "body": "{\"text\": \"Professional wrestling began in the 19th century...\"}",
  "queryStringParameters": {"points": "3"}
}
```

**Expected Output:**
```
1. Professional wrestling evolved from 19th-century grappling contests to predetermined entertainment with storytelling.
2. The WWWF (later WWF) was established in 1963 in the Northeast, later expanding nationally under Vince McMahon in the 1980s.
3. WWE rebranded in 2002 and became a global entertainment company with streaming content and evolved women's divisions.
```

### AWS Lambda Deployment

Deploy via CDK:

```bash
cd iaac
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate.bat
pip install -r requirements.txt
cdk deploy
```

### Lambda Invocation

```bash
aws lambda invoke \
  --function-name TextSummaryFunction \
  --payload '{"body":"{\"text\":\"Your text here...\"}","queryStringParameters":{"points":"5"}}' \
  response.json

cat response.json
```

## Request/Response Examples

### Successful Request

```python
event = {
    "body": json.dumps({
        "text": "Your long text content here that needs to be summarized..."
    }),
    "queryStringParameters": {
        "points": "3"
    }
}
```

**Response:**
```python
{
    "statusCode": 200,
    "body": json.dumps({
        "summary": "1. First key point about the text.\n2. Second key point.\n3. Third key point."
    })
}
```

### Error Response (Missing Parameters)

```python
{
    "statusCode": 400,
    "body": json.dumps({
        "error": "text and points required!"
    })
}
```

## Dependencies

### Core AWS SDKs

- **boto3**: AWS SDK for Python
- **botocore**: Low-level service library

### LangChain Libraries

- **langchain-aws**: AWS integration for LangChain
- **langchain-core**: Core LangChain functionality
  - ChatPromptTemplate: For dynamic prompt construction
  - Chat interfaces: For model interaction

### Additional Dependencies

- **orjson**: JSON serialization (used by LangChain)
- **httpx**: HTTP client (used by LangChain)
- **pydantic**: Data validation (used by LangChain)
- **packaging**: Package utilities

### Development

- **aws-cdk-lib**: AWS CDK infrastructure library
- **constructs**: CDK constructs

## IAM Permissions Required

The Lambda execution role needs the following permissions:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": "bedrock:InvokeModel",
      "Resource": "arn:aws:bedrock:us-east-1::foundation-model/amazon.nova-lite-v1:0"
    }
  ]
}
```

## Error Handling

Current implementation includes:

- Validates both "text" and "points" are provided
- Returns 400 status with error message if parameters are missing
- Returns 200 status with summary on success

**Recommended improvements:**
- Add try-catch blocks for Bedrock API failures
- Validate text length before processing
- Validate points is a valid integer
- Add logging for debugging and monitoring
- Implement retry logic for transient failures
- Add input sanitization

## Performance Characteristics

- **Model**: Amazon Nova Lite (fast, efficient)
- **Typical Latency**: 1-3 seconds per request
- **Text Support**: Handles medium to large documents
- **Cost**: Lower cost per request compared to larger models
- **Throughput**: Suitable for batch processing

## Limitations

- Query parameters for "points" in event (not in body)
- Model ID is hardcoded to Nova Lite
- No dynamic chunking for very large texts (may hit token limits)
- Summary quality depends on text complexity and model capabilities
- Requires US East 1 region for Bedrock

## Advanced Features to Consider

- [ ] Support for different summary lengths (short, medium, long)
- [ ] Alternative model selection (Nova Pro for complex texts)
- [ ] Summary format options (bullet points, paragraphs, structured JSON)
- [ ] Multi-language support
- [ ] Key phrase extraction
- [ ] Sentiment analysis of original vs. summary
- [ ] Customizable summarization styles (technical, casual, formal)
- [ ] Streaming responses for large summaries
- [ ] Document preprocessing (PDF, DOCX parsing)
- [ ] Batch summarization API
- [ ] Quality scoring of generated summaries
- [ ] Caching for duplicate/similar texts

## Use Cases

### Document Management
- Summarize business documents for quick review
- Create abstracts for long reports
- Generate executive summaries

### Content Creation
- Summarize articles for newsletters
- Create social media snippets from long-form content
- Generate table of contents from documents

### Research
- Quickly understand research papers
- Summarize legal documents
- Extract key information from compliance documents

### Customer Support
- Summarize customer feedback
- Create concise ticket summaries
- Generate resolution summaries

## Troubleshooting

### Common Issues

**Model Not Available**
```
Error: Model not found: amazon.nova-lite-v1:0
```
- Verify Amazon Nova model is available in your region
- Request model access in Bedrock console
- Check model name spelling

**Missing Query Parameters**
```
Error: 'NoneType' object is not subscriptable
```
- Ensure queryStringParameters is included in event
- Verify "points" parameter is provided

**Text Too Long**
- Bedrock has token limits (check model documentation)
- Consider chunking very large documents
- Test with sample text first

**LangChain Import Errors**
- Ensure langchain_aws, langchain_core are installed in Lambda layer
- Verify requirements.txt includes all dependencies

## References

- [AWS Bedrock Documentation](https://docs.aws.amazon.com/bedrock/)
- [Amazon Nova Model Guide](https://docs.aws.amazon.com/bedrock/latest/userguide/model-parameters-nova.html)
- [LangChain AWS Integration](https://python.langchain.com/docs/integrations/llms/bedrock/)
- [LangChain Prompt Templates](https://python.langchain.com/docs/modules/model_io/prompts/)
- [LangChain Chains](https://python.langchain.com/docs/modules/chains/)
- [boto3 Bedrock Documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-runtime.html)
- [AWS CDK Python Guide](https://docs.aws.amazon.com/cdk/v2/guide/work-with-cdk-python.html)

