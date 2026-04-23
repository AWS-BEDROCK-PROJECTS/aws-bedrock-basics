# Image Generation with Stability AI Models via AWS Bedrock

This module demonstrates image generation using Stability AI's Stable Diffusion and Stable Image models through Amazon Bedrock, with both Lambda-based and local execution options.

## Overview

The images module provides:
- **Stability AI Model Integration**: Uses Stability AI's state-of-the-art diffusion models
- **Lambda Backend**: API Gateway-compatible Lambda handler for serverless deployment
- **Local Generation**: Standalone script for local testing and development
- **S3 Integration**: Automatic image upload and storage
- **Text-to-Image**: Generate images from natural language descriptions

## Project Structure

```
images/
├── stability.py                      # Local image generation script
└── stability_difussion_lambda.py     # Lambda handler for API integration
```

## Key Components

### stability.py

**Main Script:**

- Demonstrates local image generation using Stability AI models
- Generates a single image from a text prompt
- Saves output locally to PNG file
- No external dependencies beyond boto3

**Workflow:**

```python
1. Create Bedrock runtime client (us-west-2)
2. Configure image generation with prompt
3. Invoke Stable Image Core model
4. Decode base64 image response
5. Save to local file (dragon.png)
```

**Usage:**

```bash
python stability.py
```

**Output:**
- Creates `dragon.png` in current directory
- Image generated from prompt: "a photo of a dragon"

### stability_difussion_lambda.py

**Lambda Handler:**

- AWS Lambda function for serverless deployment
- Designed for API Gateway integration
- Reads user prompts from API requests
- Generates images using Stable Diffusion XL
- Automatically uploads images to S3
- Returns success response

**Workflow:**

```python
1. Parse event from API Gateway (body contains message)
2. Extract user message/prompt
3. Create Bedrock runtime client with extended timeout
4. Configure Stable Diffusion XL payload:
   - CFG Scale: 10 (guidance scale for prompt adherence)
   - Steps: 100 (inference steps, higher = better quality)
   - Seed: 0 (for reproducibility)
5. Invoke model with payload
6. Decode base64 image from response
7. Upload to S3 with timestamp-based key
8. Return success response
```

**Configuration:**

- **Region**: US West 2
- **Read Timeout**: 300 seconds (image generation can take time)
- **Max Retries**: 3
- **S3 Bucket**: 'bedrock-image-bucket'
- **S3 Path**: 'output-images/{timestamp}.png'

## Bedrock Models

### Stable Image Core (stability.py)

- **Model ID**: `stability.stable-image-core-v1:1`
- **Capability**: Fast, efficient image generation
- **Input**: Text prompts
- **Output**: Base64-encoded PNG
- **Region**: US West 2
- **Use Case**: Quick image generation, local testing

### Stable Diffusion XL (stability_difussion_lambda.py)

- **Model ID**: `stability.stable-diffusion-xl-v0`
- **Capability**: High-quality image generation
- **Input**: Text prompts with configuration
- **Output**: Base64-encoded PNG
- **Region**: US West 2
- **Use Case**: Production image generation, API services

## Configuration

### Common Parameters

```python
AWS_REGION = "us-west-2"  # Stability models require this region
```

### Stable Diffusion XL Payload

```json
{
  "text_prompts": [
    {
      "text": "user prompt here"
    }
  ],
  "cfg_scale": 10,
  "seed": 0,
  "steps": 100
}
```

**Parameters Explained:**

- **text_prompts**: List of text prompts (can have multiple)
- **cfg_scale** (0.0-35.0): How closely to follow the prompt
  - Lower = more creative/varied
  - Higher = adherence to prompt
  - Recommended: 7-15
- **steps** (10-100): Inference steps
  - Lower = faster but lower quality
  - Higher = slower but better quality
  - Recommended: 30-50 for balance, 100 for maximum quality
- **seed**: Seed for reproducibility
  - 0 = random
  - Fixed value = consistent results

### Lambda Configuration

```python
timeout = 300  # seconds (image generation takes time)
memory = 1024  # MB (minimum recommended)
environment_variables = {
    'S3_BUCKET': 'bedrock-image-bucket'
}
```

## Usage

### Local Image Generation

**Simple Example:**

```bash
python stability.py
```

**Custom Prompt:**

```python
import boto3
import json
import base64

client = boto3.client(service_name='bedrock-runtime', region_name="us-west-2")

prompt = "a serene mountain landscape at sunset"
config = json.dumps({
    "prompt": prompt
})

response = client.invoke_model(
    body=config,
    modelId="stability.stable-image-core-v1:1",
    accept="application/json",
    contentType="application/json"
)

response_body = json.loads(response.get("body").read())
base64_image = response_body.get("images")[0]
image_data = base64.b64decode(base64_image)

with open("output.png", "wb") as f:
    f.write(image_data)
```

### Lambda Deployment

**Deploy Function:**

```bash
# Package the Lambda function
zip lambda_function.zip stability_difussion_lambda.py

# Deploy using AWS CLI
aws lambda create-function \
  --function-name ImageGenerationFunction \
  --runtime python3.11 \
  --role arn:aws:iam::ACCOUNT_ID:role/lambda-role \
  --handler stability_difussion_lambda.lambda_handler \
  --zip-file fileb://lambda_function.zip \
  --timeout 300 \
  --memory-size 1024 \
  --region us-west-2
```

**API Gateway Integration:**

```bash
# Create API Gateway endpoint that triggers Lambda
# Configure POST method pointing to ImageGenerationFunction
```

**Invoke via API:**

```bash
curl -X POST https://your-api-gateway-url/generate \
  -H "Content-Type: application/json" \
  -d '{
    "message": "a futuristic city with flying cars at night"
  }'
```

**Response:**

```json
{
  "statusCode": 200,
  "body": "Image Saved to s3"
}
```

## Request/Response Examples

### Local Script Input

```python
# stability.py generates image from hardcoded prompt
prompt = "a photo of a dragon"
# Output: dragon.png
```

### Lambda Input

```json
{
  "body": "{\"message\": \"a magnificent castle on a mountain peak\"}"
}
```

**Lambda Response:**

```json
{
  "statusCode": 200,
  "body": "Image Saved to s3"
}
```

### S3 Output

```
s3://bedrock-image-bucket/output-images/143022.png  # HH:MM:SS format
```

## Dependencies

### AWS SDKs

- **boto3**: AWS SDK for Python
- **botocore**: Low-level service library with configuration support

### Standard Libraries

- **json**: JSON handling
- **base64**: Base64 encoding/decoding
- **datetime**: Timestamp generation (Lambda only)

### Performance Configurations

```python
# Extended timeouts for image generation
botocore.config.Config(
    read_timeout=300,  # 5 minutes
    retries={'max_attempts': 3}
)
```

## IAM Permissions Required

### For Local Script

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": "bedrock:InvokeModel",
      "Resource": [
        "arn:aws:bedrock:us-west-2::foundation-model/stability.stable-image-core-v1:1"
      ]
    }
  ]
}
```

### For Lambda Function

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": "bedrock:InvokeModel",
      "Resource": [
        "arn:aws:bedrock:us-west-2::foundation-model/stability.stable-diffusion-xl-v0"
      ]
    },
    {
      "Effect": "Allow",
      "Action": [
        "s3:PutObject"
      ],
      "Resource": "arn:aws:s3:::bedrock-image-bucket/*"
    }
  ]
}
```

## Model Comparison

| Feature | Stable Image Core | Stable Diffusion XL |
|---------|------------------|-------------------|
| Speed | Faster | Slightly slower |
| Quality | Good | Excellent |
| Cost | Lower | Standard |
| Customization | Limited | Advanced |
| Best For | Quick generation | High-quality results |

## Performance Characteristics

### Latency

- **Stable Image Core**: 3-8 seconds typically
- **Stable Diffusion XL**: 5-15 seconds typically
- Varies based on step count and inference load

### Quality Factors

- **Steps**: 30-50 good, 100 excellent
- **CFG Scale**: 7-15 balanced, higher for accuracy
- **Prompt Quality**: Detailed prompts produce better results

### Cost Optimization

- Use Stable Image Core for quick tests
- Batch requests when possible
- Cache results for repeated prompts
- Optimize step count vs. quality needs

## Prompt Engineering Tips

### Effective Prompts

**Good prompts include:**
- Style (photorealistic, painting, 3D render)
- Subject (what to generate)
- Details (colors, lighting, composition)
- Quality modifiers (high detail, 4K, professional)

**Examples:**

```
"a photorealistic portrait of a woman with blue eyes, professional lighting, sharp focus, 4K quality"

"an oil painting of a serene lake surrounded by mountains during golden hour"

"a sci-fi spaceship interior, sleek design, blue neon lighting, detailed architecture"
```

### Prompts to Avoid

- Vague descriptions
- Contradictory instructions
- Overly complex requests
- NSFW or prohibited content

## Error Handling

Current implementation includes basic error handling:

- Lambda has retry configuration (max 3 attempts)
- Extended read timeout for slow responses
- S3 upload with timestamp to prevent collisions

**Recommended improvements:**

```python
try:
    response = bedrock.invoke_model(...)
except bedrock.exceptions.ValidationException as e:
    return {
        "statusCode": 400,
        "body": json.dumps({"error": "Invalid prompt or configuration"})
    }
except bedrock.exceptions.InternalServerException as e:
    return {
        "statusCode": 503,
        "body": json.dumps({"error": "Service temporarily unavailable"})
    }
except Exception as e:
    return {
        "statusCode": 500,
        "body": json.dumps({"error": "Unexpected error generating image"})
    }
```

## Limitations

- Images are 512x512 or 1024x1024 (model default)
- Requires US West 2 region
- Image generation is time-intensive
- Base64 decoding adds overhead
- S3 bucket must exist and be accessible
- No image post-processing
- Limited to single image per request

## Advanced Features to Consider

- [ ] Batch image generation
- [ ] Image variations and upscaling
- [ ] Custom image dimensions
- [ ] Negative prompts (what to avoid)
- [ ] ControlNet for guided generation
- [ ] Image inpainting/editing
- [ ] Multi-prompt with weights
- [ ] Image-to-image generation
- [ ] Real-time streaming of generation
- [ ] WebSocket API for long-running requests
- [ ] Image caching and deduplication
- [ ] ML pipeline with validation

## Troubleshooting

### Common Issues

**Model Not Found**
```
Error: Model not found: stability.stable-diffusion-xl-v0
```
- Verify you're in us-west-2 region
- Request model access in Bedrock console
- Check model ID spelling

**S3 Access Denied**
- Verify S3 bucket exists
- Check Lambda IAM role has s3:PutObject permission
- Verify bucket name in code

**Lambda Timeout**
- Increase Lambda timeout to 300+ seconds
- Image generation takes time, especially with 100 steps
- Consider using asynchronous processing

**Base64 Decode Error**
- Verify response structure is correct
- Check image format is PNG/JPEG
- Log response for debugging

## References

- [AWS Bedrock Documentation](https://docs.aws.amazon.com/bedrock/)
- [Stability AI Models Guide](https://docs.aws.amazon.com/bedrock/latest/userguide/model-parameter-details.html#model-parameter-details-stability-diffusion)
- [Stable Diffusion XL Documentation](https://platform.stability.ai/docs/api-reference)
- [Bedrock Lambda Integration](https://docs.aws.amazon.com/bedrock/latest/userguide/service-quotas.html)
- [boto3 Bedrock Documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-runtime.html)
- [Prompt Engineering Guide](https://platform.stability.ai/docs/features/prompt-engineering)
- [AWS Lambda Best Practices](https://docs.aws.amazon.com/lambda/latest/dg/best-practices.html)

