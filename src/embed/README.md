# Text and Image Embeddings with AWS Bedrock

This module demonstrates how to use Amazon Bedrock's embedding models to convert text and images into vector embeddings, and perform similarity comparisons using cosine similarity.

## Overview

The embeddings module provides utilities and examples for:
- Converting text to numerical vector embeddings
- Converting images to numerical vector embeddings
- Computing cosine similarity between embeddings
- Finding similar content based on semantic meaning
- Building semantic search and recommendation systems

## Project Structure

```
embed/
├── text.py           # Text embedding and similarity comparison
├── image.py          # Image embedding and similarity comparison
├── similarity.py     # Cosine similarity utility functions
└── sample.py         # Simple text embedding example
```

## Key Components

### similarity.py

**Core Utility Functions:**

- **`dotProduct(embedding1, embedding2)`** - Calculates dot product of two embeddings
  - Returns: Sum of element-wise products
  - Used internally for similarity calculations

- **`cosineSimilarity(embedding1, embedding2)`** - Calculates cosine similarity between embeddings
  - Returns: Float value between -1 and 1 (typically 0 to 1 for normalized embeddings)
  - 1.0 = identical/highly similar
  - 0.0 = orthogonal/unrelated
  - -1.0 = opposite/dissimilar

**Mathematical Formula:**

$$\text{cosine similarity} = \frac{\vec{a} \cdot \vec{b}}{|\vec{a}| \times |\vec{b}|}$$

### text.py

**Main Function:**

- **`getEmbedding(input: str)`** - Generates embedding for text input
  - Invokes Titan Text Embedding model
  - Returns: Vector embedding array
  - Region: US West 2

**Workflow:**

1. Accepts a list of facts/texts
2. Generates embeddings for each fact
3. Generates embedding for query
4. Computes cosine similarity between query and all facts
5. Ranks and displays similarities

**Example:**

```python
facts = [
    'The first computer was invented in the 1940s.',
    'John F. Kennedy was the 35th President of the United States.',
    'The first moon landing was in 1969.',
    'The capital of France is Paris.',
    'Earth is the third planet from the sun.',
]

question = 'Who is the president of USA?'
# Returns similarities sorted by relevance
```

### image.py

**Main Function:**

- **`getImagesEmbedding(imagePath: str)`** - Generates embedding for image
  - Reads image file from disk
  - Encodes to base64
  - Invokes Titan Image Embedding model
  - Returns: Vector embedding array

**Workflow:**

1. Loads multiple images
2. Generates embeddings for each image
3. Loads test image and generates its embedding
4. Computes cosine similarity between test image and all images
5. Ranks and displays similarities

**Example:**

```python
images = [
    'images/1.png',
    'images/2.png',
    'images/3.png',
]

test_image = 'images/cat.png'
# Finds most similar images to cat.png
```

### sample.py

**Simple Example:**

- Demonstrates basic text embedding
- Encodes animal names to vectors
- Shows model response structure

## Configuration

### AWS Region

```python
AWS_REGION = "us-west-2"  # Embedding models available in this region
```

### Bedrock Models

**Text Embeddings:**
- **Model ID**: `amazon.titan-embed-text-v1`
- **Input**: Text string
- **Output**: Vector embedding (1536 dimensions)
- **Use Case**: Semantic search, text similarity, classification

**Image Embeddings:**
- **Model ID**: `amazon.titan-embed-image-v1`
- **Input**: Base64-encoded image
- **Output**: Vector embedding (1024 dimensions)
- **Supported Formats**: PNG, JPEG
- **Use Case**: Image search, visual similarity, recommendation

## Usage

### Text Embedding Example

```bash
python text.py
```

**Output:**
```
Similarities for fact: 'Who is the president of USA?' with:
  'John F. Kennedy was the 35th President of the United States.': 0.92
  'Earth is the third planet from the sun.': 0.45
  'The capital of France is Paris.': 0.42
  'The first moon landing was in 1969.': 0.38
  'The first computer was invented in the 1940s.': 0.35
```

### Image Embedding Example

```bash
python image.py
```

**Output:**
```
Similarities of 'images/cat.png' with:
  'images/2.png': 0.88
  'images/1.png': 0.76
  'images/3.png': 0.62
```

### Simple Embedding Example

```bash
python sample.py
```

**Output:**
```
[0.123, -0.456, 0.789, ..., 0.234]  # Vector embedding
```

## Use Cases

### 1. Semantic Search

Find relevant documents or content based on meaning, not keywords:

```python
# Search for articles similar to a query
query_embedding = getEmbedding("machine learning techniques")
article_embeddings = [getEmbedding(article) for article in articles]
similarities = [cosineSimilarity(query_embedding, emb) for emb in article_embeddings]
```

### 2. Duplicate Detection

Identify similar or duplicate content:

```python
# Compare new document with existing ones
new_doc_embedding = getEmbedding(new_document)
for existing_doc in existing_documents:
    similarity = cosineSimilarity(new_doc_embedding, getEmbedding(existing_doc))
    if similarity > 0.95:
        print(f"Potential duplicate found: {similarity}")
```

### 3. Recommendation Systems

Recommend similar products, articles, or images:

```python
# Image-based product recommendation
product_image_embedding = getImagesEmbedding("product.png")
for similar_product in similar_products:
    similarity = cosineSimilarity(product_image_embedding, getImagesEmbedding(similar_product))
```

### 4. Content Classification

Group similar content into categories:

```python
# Classify by finding closest category
document_embedding = getEmbedding(document)
category_embeddings = {cat: getEmbedding(cat_description) for cat in categories}
best_category = max(category_embeddings, 
                   key=lambda cat: cosineSimilarity(document_embedding, category_embeddings[cat]))
```

### 5. Visual Search

Find similar images in a database:

```python
# Find products similar to an image
query_image_embedding = getImagesEmbedding("query.png")
for product_image in product_images:
    similarity = cosineSimilarity(query_image_embedding, getImagesEmbedding(product_image))
```

## Dependencies

### AWS SDKs

- **boto3**: AWS SDK for Python
- **botocore**: Low-level service library

### Standard Libraries

- **json**: JSON handling
- **base64**: Base64 encoding for images

## IAM Permissions Required

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": "bedrock:InvokeModel",
      "Resource": [
        "arn:aws:bedrock:us-west-2::foundation-model/amazon.titan-embed-text-v1",
        "arn:aws:bedrock:us-west-2::foundation-model/amazon.titan-embed-image-v1"
      ]
    }
  ]
}
```

## Embedding Characteristics

### Titan Text Embeddings

- **Dimensions**: 1536
- **Max Input**: ~8,000 tokens per request
- **Normalized**: Yes (cosine similarity works well)
- **Language**: Supports multiple languages
- **Quality**: Good for semantic search and clustering

### Titan Image Embeddings

- **Dimensions**: 1024
- **Input Formats**: PNG, JPEG
- **Max Size**: Depends on Bedrock limits
- **Normalized**: Yes
- **Speed**: Fast inference for large batches
- **Quality**: Good for visual search and recommendation

## Performance Considerations

### Embedding Generation

- **Latency**: 100-500ms per embedding (text or image)
- **Throughput**: ~10-20 embeddings per second
- **Cost**: Pay per request/token

### Similarity Calculation

- **Cosine Similarity**: O(n) time complexity for n-dimensional vectors
- **Memory**: Minimal (just stores vectors)
- **Speed**: Very fast (microseconds per comparison)

### Optimization Tips

1. **Batch Processing**: Generate embeddings once and reuse
2. **Caching**: Store embeddings in vector database
3. **Approximate Search**: Use vector databases (e.g., FAISS, Pinecone) for large datasets
4. **Chunking**: For large texts, split into smaller chunks

## Limitations

- Text embeddings limited to ~8,000 tokens
- Image embeddings limited by Bedrock input constraints
- Requires US West 2 region for embeddings
- Current implementation does not persist embeddings
- No batch API (processes one at a time)
- Cosine similarity range depends on embedding normalization

## Advanced Features to Consider

- [ ] Vector database integration (FAISS, Pinecone, Weaviate)
- [ ] Batch embedding generation API
- [ ] Caching layer for frequently used embeddings
- [ ] Approximate nearest neighbor search (ANN)
- [ ] Dimension reduction (PCA, UMAP)
- [ ] Clustering with K-means or DBSCAN
- [ ] Multi-modal search (text + image)
- [ ] Embedding monitoring and analytics
- [ ] Model updates and versioning
- [ ] Fine-tuning for domain-specific embeddings

## Building a Vector Database

For production use with large datasets, combine Bedrock embeddings with a vector database:

### Example with FAISS

```python
import faiss
import numpy as np

# Generate embeddings
embeddings = []
for text in documents:
    embedding = getEmbedding(text)
    embeddings.append(embedding)

# Create FAISS index
embeddings = np.array(embeddings).astype('float32')
index = faiss.IndexFlatL2(len(embeddings[0]))
index.add(embeddings)

# Search
query_embedding = np.array([getEmbedding(query)]).astype('float32')
distances, indices = index.search(query_embedding, k=5)
```

## Troubleshooting

### Common Issues

**Model Not Found**
```
Error: Model not found: amazon.titan-embed-text-v1
```
- Verify you're in US West 2 region
- Request model access in Bedrock console
- Check model name spelling

**Invalid Base64 Image**
- Ensure image file exists
- Check image format (PNG/JPEG)
- Verify file path is correct

**Unexpected Similarity Scores**
- Check embeddings are properly normalized
- Verify cosine similarity formula is correct
- Try with different sample data

**Out of Memory**
- Process large batches in smaller chunks
- Use vector database for millions of embeddings
- Consider model quantization

## References

- [AWS Bedrock Documentation](https://docs.aws.amazon.com/bedrock/)
- [Titan Embeddings Guide](https://docs.aws.amazon.com/bedrock/latest/userguide/model-parameters-titan-embed.html)
- [Cosine Similarity Theory](https://en.wikipedia.org/wiki/Cosine_similarity)
- [Vector Databases Overview](https://www.pinecone.io/learn/vector-database/)
- [FAISS Library](https://github.com/facebookresearch/faiss)
- [boto3 Bedrock Documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-runtime.html)
- [Semantic Search Guide](https://docs.aws.amazon.com/bedrock/latest/userguide/knowledge-base.html)

