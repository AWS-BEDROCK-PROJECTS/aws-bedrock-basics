# Text Generation and Processing with AWS Bedrock

This module demonstrates various text generation and processing use cases using Amazon Bedrock's foundation models, including chatbots, code generation, meeting summarization, and conversation analysis.

## Overview

The text module provides examples for:
- **Interactive Chatbots**: Real-time conversational AI powered by Titan Text Express
- **Code Generation**: Automatic code generation from natural language instructions using Claude
- **Meeting Summarization**: Extract key points from meeting notes and transcripts
- **Conversation Analysis**: Summarize phone conversations and dialogues
- **Multi-Model Examples**: Comparing Titan and Llama model capabilities

## Project Structure

```
text/
├── chat_history.py                    # Interactive chatbot implementation
├── code_generator_lambda.py           # Lambda handler for code generation
├── generate.py                        # Multi-model demonstration (Titan & Llama)
├── meeting_summarization_lambda.py    # Lambda handler for meeting summaries
└── summary.py                         # Conversation summarization example
```

## Key Components

### chat_history.py

**Purpose:** Interactive chatbot with persistent conversation in a terminal

**Main Features:**

- Real-time user interaction
- Streaming responses from Titan Text Express model
- Configurable parameters for response quality
- Exit command for graceful shutdown

**Workflow:**

```python
1. Initialize Bedrock client
2. Display bot greeting
3. Wait for user input
4. Send user message to Titan model
5. Receive and display response
6. Repeat until user types "exit"
```

**Configuration:**

```python
textGenerationConfig = {
    "maxTokenCount": 4096,      # Maximum response length
    "stopSequences": [],        # Sequences to stop generation
    "temperature": 0,           # Deterministic responses (0)
    "topP": 1                   # No nucleus sampling
}
```

**Usage:**

```bash
python chat_history.py
```

**Interaction Example:**

```
Bot: Hello! I am a chatbot. I can help you with anything you want to talk about.
User: What is Python?
Bot: Python is a high-level programming language...
User: Tell me about machine learning
Bot: Machine learning is a subset of artificial intelligence...
User: exit
```

### generate.py

**Purpose:** Comparison and demonstration of multiple foundation models

**Models Demonstrated:**

**Titan Text Express:**
```python
model_id = "amazon.titan-text-express-v1"
config = {
    "inputText": prompt,
    "textGenerationConfig": {
        "maxTokenCount": 4096,
        "stopSequences": [],
        "temperature": 0,
        "topP": 1
    }
}
```

**Meta Llama 3 (70B):**
```python
model_id = "meta.llama3-70b-instruct-v1:0"
config = {
    "prompt": prompt,
    "max_gen_len": 512,
    "temperature": 0,
    "top_p": 0.9
}
```

**Usage:**

```bash
python generate.py
```

**Output:** Generates story about dragon, compares model responses

### code_generator_lambda.py

**Purpose:** AWS Lambda function for automated code generation

**Main Functions:**

- **`generate_code_using_bedrock(message, language)`** - Generates code in specified language
  - Uses Claude v2 model
  - Accepts natural language instructions
  - Returns generated code string
  - Temperature: 0.1 (low randomness for consistent code)

- **`save_code_to_s3_bucket(code, s3_bucket, s3_key)`** - Stores generated code in S3
  - Handles S3 connection
  - Includes error handling
  - Prints confirmation messages

- **`lambda_handler(event, context)`** - AWS Lambda entry point
  - Parses request body for message and language
  - Invokes code generation
  - Saves result to S3
  - Returns success/failure response

**Configuration:**

```python
body = {
    "prompt": prompt_text,
    "max_tokens_to_sample": 2048,  # Max code length
    "temperature": 0.1,             # Low randomness
    "top_k": 250,
    "top_p": 0.2,
    "stop_sequences": ["\n\nHuman:"]
}
```

**Workflow:**

```
1. API Gateway sends request to Lambda
2. Parse message (instructions) and language
3. Create Claude-formatted prompt
4. Invoke Claude v2 model
5. Extract generated code
6. Save to S3: s3://bucket/code-output/{timestamp}.py
7. Return success response
```

**Lambda Configuration:**

```python
Timeout: 300 seconds
Memory: 1024 MB (minimum recommended)
Region: {REGION_NAME}
Environment Variables:
  BUCKET_NAME: S3 bucket for code storage
  REGION_NAME: AWS region
```

**API Request:**

```json
{
  "body": "{\"message\": \"Create a function to sort a list\", \"key\": \"python\"}"
}
```

**Response:**

```json
{
  "statusCode": 200,
  "body": "Code generation"
}
```

### meeting_summarization_lambda.py

**Purpose:** AWS Lambda function for meeting and conversation summarization

**Main Functions:**

- **`extract_text_from_multipart(data)`** - Parses multipart MIME messages
  - Handles email-style multipart data
  - Extracts plain text content
  - Supports both simple and complex formats

- **`generate_summary_from_bedrock(content)`** - Creates summary using Claude
  - Uses Claude v2 model
  - Accepts any text content
  - Temperature: 0.1 (consistent summaries)
  - Max tokens: 5000

- **`save_summary_to_s3_bucket(summary, s3_bucket, s3_key)`** - Stores summary in S3
  - Similar to code generator S3 function
  - Handles errors gracefully

- **`lambda_handler(event, context)`** - AWS Lambda entry point
  - Base64 decodes incoming body
  - Extracts text from multipart format
  - Generates summary
  - Saves to S3: s3://bucket/summary-output/{timestamp}.txt

**Configuration:**

```python
body = {
    "prompt": "Summarize the following meeting notes: {content}\nAssistant:",
    "max_tokens_to_sample": 5000,
    "temperature": 0.1,
    "top_k": 250,
    "top_p": 0.2,
    "stop_sequences": ["\n\nHuman:"]
}
```

**Workflow:**

```
1. API Gateway Base64 encodes meeting notes
2. Lambda decodes body
3. Extract text from multipart MIME (if applicable)
4. Create Claude prompt with meeting content
5. Invoke Claude v2 model
6. Extract summary from response
7. Save to S3
8. Return success response
```

**Lambda Configuration:**

```python
Timeout: 300 seconds
Memory: 1024 MB
Region: us-west-2
S3 Bucket: bedrock-course-bucket
```

**Input Format:**

```
Base64-encoded multipart message with meeting notes
```

### summary.py

**Purpose:** Conversation summarization example

**Features:**

- Demonstrates prompt engineering for summaries
- Shows constraint-based summarization (30 word limit)
- Uses Titan Text Express model
- Includes full conversation transcript

**Example Input:**

```
Phone conversation between Alex and Emily planning a picnic
14 conversational exchanges
Discussion of location, food, timing, attendees
```

**Configuration:**

```python
model_id = "amazon.titan-text-express-v1"
maxTokenCount = 4096
temperature = 0  # Deterministic
topP = 1
```

**Usage:**

```bash
python summary.py
```

**Expected Output:**

```
Alex and Emily plan a picnic at Riverside Park for Saturday at noon,
with Jordan and Casey invited. Emily will provide sandwiches and cookies;
Alex will bring drinks and fruit.
```

## Bedrock Models Used

| Model | Use Case | Parameters | Provider |
|-------|----------|-----------|----------|
| amazon.titan-text-express-v1 | Chatbots, summarization | Max 4096 tokens | AWS Titan |
| anthropic.claude-v2 | Code generation, analysis | Max 2048 tokens | Anthropic |
| meta.llama3-70b-instruct-v1:0 | General text generation | Max 512 tokens | Meta |

## Configuration Parameters Explained

### Temperature (0.0 - 1.0)

- **0.0**: Deterministic, same response every time (best for code, summaries)
- **0.7**: Balanced, some randomness
- **1.0**: Maximum randomness, creative responses

### Top P (Nucleus Sampling)

- **0.2**: Conservative, stick to likely tokens
- **0.9**: Broader generation, more variety
- **1.0**: No filtering, all tokens considered

### Top K

- Limits to top K most likely next tokens
- **50**: Conservative, common tokens only
- **250**: More variety, rarer tokens allowed

### Max Tokens

- Controls maximum response length
- Larger = longer responses, more cost
- Smaller = faster responses, concise output

## Usage Examples

### Chat with Bot

```bash
python chat_history.py
```

### Generate Code

**Via Lambda (API):**
```bash
curl -X POST https://your-api/generate-code \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Write a function that reverses a string",
    "key": "python"
  }'
```

**Response:** Code saved to S3, notification returned

### Summarize Meeting

**Via Lambda (API):**
```bash
curl -X POST https://your-api/summarize-meeting \
  --data-binary @meeting_notes.txt
```

**Response:** Summary saved to S3, confirmation returned

### Compare Models

```bash
python generate.py
```

### Summarize Conversation

```bash
python summary.py
```

## Dependencies

### AWS SDKs

- **boto3**: AWS SDK for Python
- **botocore**: Config and low-level operations

### Standard Libraries

- **json**: JSON parsing and generation
- **datetime**: Timestamp generation
- **email**: MIME message parsing
- **base64**: Base64 encoding/decoding
- **pprint**: Pretty-printing for debugging

## IAM Permissions Required

### For Interactive Scripts

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": "bedrock:InvokeModel",
      "Resource": [
        "arn:aws:bedrock:us-west-2::foundation-model/amazon.titan-text-express-v1",
        "arn:aws:bedrock:us-west-2::foundation-model/meta.llama3-70b-instruct-v1:0"
      ]
    }
  ]
}
```

### For Lambda Functions

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": "bedrock:InvokeModel",
      "Resource": [
        "arn:aws:bedrock:us-west-2::foundation-model/anthropic.claude-v2"
      ]
    },
    {
      "Effect": "Allow",
      "Action": [
        "s3:PutObject"
      ],
      "Resource": "arn:aws:s3:::bedrock-course-bucket/*"
    }
  ]
}
```

## Performance Characteristics

### Latency

- **Chatbot**: 100-500ms per response
- **Code Generation**: 1-5 seconds (code is complex)
- **Summary**: 1-3 seconds (depends on content length)

### Cost Optimization

- Use temperature=0 for deterministic tasks (code, summaries)
- Set appropriate max tokens to avoid unnecessary computation
- Batch processing when possible
- Cache frequently generated responses

## Prompt Engineering Best Practices

### For Code Generation

```
Good: "Write a Python function that takes a list and returns it sorted in ascending order"
Bad: "write code"

Good: "Generate Python code for a login function with username/password validation"
Bad: "make login"
```

### For Summaries

```
Good: "Summarize the following meeting notes in maximum 50 words, highlighting action items"
Bad: "Summarize the meeting"
```

### For Chatbots

```
Good: "You are a helpful software engineer assistant..."
Bad: "Tell me about Python"
```

## Error Handling

### Current Implementation

- Try-catch blocks in Lambda functions
- Prints error messages for debugging
- Returns HTTP responses with status codes

### Recommended Improvements

```python
try:
    response = bedrock.invoke_model(...)
except bedrock.exceptions.ValidationException:
    return {"statusCode": 400, "body": json.dumps("Invalid request")}
except bedrock.exceptions.InternalServerException:
    return {"statusCode": 503, "body": json.dumps("Service unavailable")}
except Exception as e:
    return {"statusCode": 500, "body": json.dumps(f"Error: {str(e)}")}
```

## Limitations

- Models limited to specific regions (us-west-2)
- Token limits vary by model (512-5000)
- Temperature 0 may produce similar outputs repeatedly
- Large files require chunking for processing
- Base64 encoding adds overhead for binary data
- S3 buckets must be pre-created
- Meeting extraction assumes MIME format

## Advanced Features to Consider

- [ ] Multi-turn conversation with history storage
- [ ] Streaming responses for real-time updates
- [ ] Vector database integration for semantic search
- [ ] Custom prompt templates and optimization
- [ ] A/B testing different models
- [ ] Cost tracking and optimization
- [ ] Real-time error reporting and alerts
- [ ] Document parsing for varied formats
- [ ] Multi-language support
- [ ] Caching layer for repeated queries
- [ ] Webhook notifications for Lambda completion
- [ ] Session management for conversations

## From Using Different Models

### Choosing the Right Model

- **Titan Text Express**: Fast, good for chatbots and general tasks
- **Claude v2**: Better code generation, reasoning
- **Llama 3 70B**: Strong performance, good balance of speed/quality

## Troubleshooting

### Common Issues

**Model Not Found**
- Verify region is us-west-2
- Request model access in Bedrock console
- Check model ID spelling

**Lambda Timeout**
- Increase timeout to 300+ seconds
- Model inference takes time, especially for long outputs
- Monitor CloudWatch logs

**S3 Access Denied**
- Verify Lambda role has s3:PutObject permission
- Check S3 bucket exists and is accessible
- Verify bucket name in code

**Empty or Malformed Responses**
- Check model response format
- Verify JSON parsing
- Log raw response for debugging

## References

- [AWS Bedrock Documentation](https://docs.aws.amazon.com/bedrock/)
- [Titan Model Documentation](https://docs.aws.amazon.com/bedrock/latest/userguide/model-parameters-titan-text.html)
- [Claude Model Documentation](https://docs.aws.amazon.com/bedrock/latest/userguide/model-parameters-anthropic-claude.html)
- [Meta Llama Documentation](https://docs.aws.amazon.com/bedrock/latest/userguide/model-parameters-meta-llama.html)
- [Lambda Best Practices](https://docs.aws.amazon.com/lambda/latest/dg/best-practices.html)
- [Prompt Engineering Guide](https://platform.openai.com/docs/guides/prompt-engineering)
- [boto3 Bedrock Documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-runtime.html)

