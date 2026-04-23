# Image Generation with AWS Bedrock

This module demonstrates how to use Amazon Bedrock's Titan Image Generator model to create images from text descriptions and store them in Amazon S3.

## Overview

The image generation module provides a Lambda handler that:
- Accepts text descriptions as input
- Invokes the Amazon Titan Image Generator v2 model via AWS Bedrock
- Converts the generated base64-encoded image to a file
- Stores the image in an S3 bucket
- Returns a pre-signed URL for accessing the image

## Project Structure

```
image/
├── image.py                 # Main handler and utility functions
├── image_test.py            # Test script for local testing
└── iaac/                    # Infrastructure as Code (CDK)
    ├── app.py               # CDK application entry point
    ├── iaac_stack.py        # CDK stack definition
    ├── requirements.txt     # CDK dependencies
    ├── requirements-dev.txt # Development dependencies
    ├── cdk.json             # CDK configuration
    ├── source.bat           # Windows environment setup
    └── tests/               # CDK unit tests
```

## Key Components

### image.py

**Main Functions:**

- **`handler(event, context)`** - Lambda handler that processes image generation requests
  - Input: Event with JSON body containing "description" field
  - Output: HTTP response with pre-signed S3 URL

- **`get_titan_config(description)`** - Builds the configuration for Titan Image Generator
  - Configures text-to-image generation
  - Sets dimensions to 512x512
  - Sets CFG scale to 8.0 (higher = more adherence to prompt)

- **`save_image_to_s3(base64_image)`** - Handles S3 operations
  - Decodes base64 image
  - Uploads to S3 bucket
  - Generates pre-signed URL (valid for 1 hour)

## Configuration

### Environment Variables

```python
AWS_REGION_BEDROCK = "us-east-1"  # Bedrock service region
S3_BUCKET = "images-bucket-999"   # S3 bucket for storing images
```

### Bedrock Model

- **Model ID**: `amazon.titan-image-generator-v2`
- **Region**: US East 1 (Bedrock is region-specific)

### Image Generation Settings

```json
{
  "taskType": "TEXT_IMAGE",
  "imageGenerationConfig": {
    "numberOfImages": 1,
    "height": 512,
    "width": 512,
    "cfgScale": 8.0
  }
}
```

## Usage

### Local Testing

Run the test script to verify the setup:

```bash
python image_test.py
```

**Test Input:**
```json
{
  "body": "{\"description\": \"A beautiful sunset\"}"
}
```

**Example Output:**
```json
{
  "statusCode": 200,
  "body": "{\"url\": \"https://images-bucket-999.s3.amazonaws.com/1624567890.jpg?...\"}"
}
```

### AWS Lambda Deployment

The module includes CDK infrastructure for automatic deployment:

1. **Deploy via CDK:**
   ```bash
   cd iaac
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate.bat
   pip install -r requirements.txt
   cdk deploy
   ```

2. **Invoke Lambda:**
   ```bash
   aws lambda invoke \
     --function-name ImageGeneratorFunction \
     --payload '{"body":"{\"description\":\"A futuristic city\"}"}' \
     response.json
   ```

## Request/Response Examples

### Request

```python
event = {
    "body": json.dumps({
        "description": "A majestic mountain landscape with snow peaks"
    })
}
```

### Response

```python
{
    "statusCode": 200,
    "body": json.dumps({
        "url": "https://images-bucket-999.s3.amazonaws.com/1623456789.jpg?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=..."
    })
}
```

## Dependencies

### Core AWS SDKs

- **boto3**: AWS SDK for Python
- **botocore**: Low-level service library

### Required AWS Services

- **Amazon Bedrock**: For model invocation (Titan Image Generator v2)
- **Amazon S3**: For image storage
- **AWS Lambda**: For serverless execution (if deployed)

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
      "Resource": "arn:aws:bedrock:us-east-1::model/amazon.titan-image-generator-v2"
    },
    {
      "Effect": "Allow",
      "Action": [
        "s3:PutObject",
        "s3:GetObject"
      ],
      "Resource": "arn:aws:s3:::images-bucket-999/*"
    }
  ]
}
```

## Error Handling

Current implementation includes:

- Validates presence of "description" in request body
- Returns error if description is missing (handler returns None implicitly)

**Recommended improvements:**
- Add try-catch blocks for Bedrock API failures
- Add try-catch blocks for S3 operations
- Return proper error responses with status codes
- Add logging for debugging

## Limitations

- Currently generates only 1 image per request
- Fixed image resolution (512x512)
- Fixed CFG scale value (8.0)
- Pre-signed URL expires after 1 hour
- Requires US East 1 region for Bedrock

## Future Enhancements

- [ ] Make image count configurable
- [ ] Support different image dimensions
- [ ] Add prompt enhancement/optimization
- [ ] Implement batch image generation
- [ ] Add request validation and error handling
- [ ] Support additional Bedrock image models
- [ ] Add CloudWatch metrics for monitoring
- [ ] Implement rate limiting and throttling

## References

- [AWS Bedrock Documentation](https://docs.aws.amazon.com/bedrock/)
- [Titan Image Generator v2 Guide](https://docs.aws.amazon.com/bedrock/latest/userguide/model-parameter-details-titan-image-generator.html)
- [AWS CDK Python Documentation](https://docs.aws.amazon.com/cdk/v2/guide/work-with-cdk-python.html)
- [boto3 Documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html)

