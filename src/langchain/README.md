# LangChain Integration with AWS Bedrock

This module demonstrates advanced LLM applications using LangChain with Amazon Bedrock's foundation models. It includes prompt chaining, basic retrieval-augmented generation (RAG), and PDF-based RAG implementations.

## Overview

LangChain is a framework for building applications with language models. This module showcases:
- **Prompt Chains**: Building composable workflows with prompts and models
- **Basic RAG**: Retrieval-augmented generation using in-memory data
- **PDF RAG**: Advanced RAG with PDF document loading and processing
- **Vector Embeddings**: Converting text to vectors for semantic search
- **Semantic Retrieval**: Finding relevant information using similarity matching

## Project Structure

```
langchain/
├── first_chain.py           # Basic prompt chaining example
├── basic_rag.py             # In-memory RAG with sample data
└── pdf_rag.py               # PDF-based RAG with document loading
```

## Key Concepts

### LangChain Components

**ChatBedrock**: LLM wrapper for Bedrock models
```python
model = ChatBedrock(
    model_id="amazon.nova-lite-v1:0",
    client=bedrock
)
```

**BedrockEmbeddings**: Converts text to vector embeddings
```python
embeddings = BedrockEmbeddings(
    model_id="amazon.titan-embed-text-v2:0",
    client=bedrock
)
```

**ChatPromptTemplate**: Creates dynamic prompts with variables
```python
template = ChatPromptTemplate.from_template(
    "Write a description for: {product_name}"
)
```

**FAISS Vector Store**: Stores and searches embeddings in memory
```python
vector_store = FAISS.from_texts(texts, embeddings)
```

**Retrievers**: Fetch relevant documents based on queries
```python
retriever = vector_store.as_retriever(search_kwargs={"k": 2})
```

## Key Components

### first_chain.py

**Purpose:** Introduction to LangChain prompt chains

**Main Function:**

- **`first_chain()`** - Demonstrates basic prompt templating and chaining

**Workflow:**

```python
1. Initialize Bedrock client
2. Create ChatBedrock model wrapper
3. Define ChatPromptTemplate with {product_name} variable
4. Create chain: prompt | model
5. Invoke chain with input
6. Extract and print response
```

**Key Features:**

- Simple prompt template with parameterization
- Model response extraction via .content
- Pipe operator (|) for chain composition

**Example:**

```bash
python first_chain.py
```

**Input:**
```python
prompt = "Write a short, compelling product description for: bicycle"
```

**Output:**
```
A lightweight, durable bicycle designed for commuting and recreational riding.
Features aluminum frame, 21-speed gears, and reliable braking system for safety
and comfort on any terrain.
```

### basic_rag.py

**Purpose:** Retrieval-augmented generation with in-memory data

**Workflow:**

```python
1. Initialize embeddings model (Titan Embed)
2. Create FAISS vector store from sample data
3. Set up retriever with k=2 (fetch 2 most similar items)
4. Query: "What does Anupam like to eat?"
5. Retrieve matching documents
6. Build chat template with context
7. Invoke model with question and context
8. Return answer based on retrieved information
```

**Data Processing:**

```python
my_data = [
    "The weather is nice today.",
    "Last night's game ended in a tie.",
    "Anupam likes to eat pizza",
    "Anupam likes to eat pasta.",
]

# These strings are converted to embeddings and stored in FAISS
vector_store = FAISS.from_texts(my_data, bedrock_embeddings)
```

**Retrieval Configuration:**

```python
retriever = vector_store.as_retriever(
    search_kwargs={"k": 2}  # Return top 2 most relevant docs
)
```

**Chat Template:**

```python
template = ChatPromptTemplate.from_messages([
    ("system", "Answer the users question based on the following context: {context}"),
    ("user", "{input}")
])
```

**Example:**

```bash
python basic_rag.py
```

**Query:** "What does Anupam like to eat?"

**Retrieved Context:**
- "Anupam likes to eat pizza"
- "Anupam likes to eat pasta."

**Output:**
```
Anupam likes to eat pizza and pasta.
```

### pdf_rag.py

**Purpose:** Advanced RAG with PDF document processing

**Advanced Features:**

1. **PDF Loading**: `PyPDFLoader` for document extraction
2. **Text Splitting**: `RecursiveCharacterTextSplitter` for chunking
3. **Similarity Score Threshold**: Only return results above confidence level
4. **System Messages**: Detailed instructions to prevent hallucinations
5. **Score-based Filtering**: Prevents returning irrelevant results

**Workflow:**

```python
1. Load PDF document using PyPDFLoader
2. Split documents into chunks (size=200, separator=". \n")
3. Convert chunks to embeddings
4. Create FAISS vector store from split documents
5. Set up retriever with:
   - similarity_score_threshold: 0.2
   - k: 5 (return up to 5 results)
6. Query the retriever
7. Format context with strict system prompt
8. Invoke model with enhanced instructions
9. Return response, or "I don't have enough information"
```

**PDF Processing:**

```python
# Load PDF
loader = PyPDFLoader("../assets/books.pdf")
docs = loader.load()

# Split into chunks
splitter = RecursiveCharacterTextSplitter(
    separators=[". \n"],      # Split on period + newline
    chunk_size=200            # Each chunk ~200 characters
)
splitted_docs = splitter.split_documents(docs)

# Create embeddings and vector store
vector_store = FAISS.from_documents(splitted_docs, bedrock_embeddings)
```

**Retrieval with Score Threshold:**

```python
retriever = vector_store.as_retriever(
    search_type="similarity_score_threshold",
    search_kwargs={
        "score_threshold": 0.2,  # Filter low-confidence results
        "k": 5                    # Return up to 5 results
    }
)
```

**System Prompt for Accuracy:**

```python
system_prompt = """You are a strict AI assistant.
Only answer using the provided context. You can be a bit descriptive if the context is right.
If the answer is not contained in the context, say:
"I am sorry, I don't have enough information in the provided context."
"""
```

**Example:**

```bash
python pdf_rag.py
```

**Query:** "Who is the creator of Gone With the Wind?"

**Output:**
- If found in PDF: "Margaret Mitchell is the creator of Gone with the Wind."
- If not found: "I am sorry, I don't have enough information in the provided context."

## Configuration

### Models Used

**Language Model:**
- **Model ID**: `amazon.nova-lite-v1:0`
- **Type**: Chat/Instruction-tuned
- **Region**: US East 1
- **Capabilities**: Fast inference, good for Q&A

**Embedding Model:**
- **Model ID**: `amazon.titan-embed-text-v2:0`
- **Type**: Text embeddings
- **Region**: US East 1
- **Dimensions**: High-dimensional vector space
- **Use**: Semantic similarity search

### LangChain Configuration

**FAISS Vector Store:**
```python
vector_store = FAISS.from_texts(texts, embeddings)
```

**Retriever Search Modes:**

1. **Default Search:**
   ```python
   retriever.as_retriever(search_kwargs={"k": 2})
   ```

2. **Similarity Score Threshold:**
   ```python
   retriever.as_retriever(
       search_type="similarity_score_threshold",
       search_kwargs={"score_threshold": 0.2, "k": 5}
   )
   ```

**Text Splitting:**
```python
splitter = RecursiveCharacterTextSplitter(
    separators=[". \n"],  # Preferred separator
    chunk_size=200,        # Target chunk size
    chunk_overlap=0        # No overlap between chunks
)
```

## Usage

### Basic Prompt Chain

```bash
python first_chain.py
```

**Code Example:**
```python
from langchain_aws import ChatBedrock
from langchain_core.prompts import ChatPromptTemplate
import boto3

bedrock = boto3.client("bedrock-runtime", region_name="us-east-1")
model = ChatBedrock(model_id="amazon.nova-lite-v1:0", client=bedrock)

template = ChatPromptTemplate.from_template(
    "Generate 3 creative uses for {item}"
)
chain = template | model

response = chain.invoke({"item": "old bicycle"})
print(response.content)
```

### In-Memory RAG

```bash
python basic_rag.py
```

**Code Example:**
```python
from langchain_aws import ChatBedrock, BedrockEmbeddings
from langchain_community.vectorstores import FAISS
import boto3

bedrock = boto3.client("bedrock-runtime", region_name="us-east-1")
model = ChatBedrock(model_id="amazon.nova-lite-v1:0", client=bedrock)
embeddings = BedrockEmbeddings(model_id="amazon.titan-embed-text-v2:0", client=bedrock)

documents = ["Your documents here"]
vector_store = FAISS.from_texts(documents, embeddings)
retriever = vector_store.as_retriever(search_kwargs={"k": 2})

question = "Your question"
context = retriever.invoke(question)

# Use context in chat
```

### PDF RAG

```bash
python pdf_rag.py
```

**Prerequisites:**
```
- ../assets/books.pdf file must exist
- PDF should contain relevant information
```

**Customization:**
```python
# Change PDF path
loader = PyPDFLoader("path/to/your/document.pdf")

# Adjust chunk size
splitter = RecursiveCharacterTextSplitter(chunk_size=300)

# Adjust threshold
retriever = vector_store.as_retriever(
    search_kwargs={"score_threshold": 0.5, "k": 3}
)
```

## Dependencies

### LangChain Core

- **langchain-core**: Core abstractions
  - `ChatPromptTemplate`: Dynamic prompt building
  - `Document`: Data structure for documents

### LangChain AWS Integration

- **langchain-aws**: Bedrock integration
  - `ChatBedrock`: LLM wrapper
  - `BedrockEmbeddings`: Embedding model wrapper

### LangChain Community

- **langchain-community**: Additional tools
  - `FAISS`: Vector store implementation
  - `PyPDFLoader`: PDF document loading

### Text Processing

- **langchain-text-splitters**: Document chunking
  - `RecursiveCharacterTextSplitter`: Smart text splitting

### AWS SDKs

- **boto3**: AWS SDK
- **botocore**: Low-level AWS operations

### Standard Libraries

- **warnings**: Warning management

## IAM Permissions Required

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": "bedrock:InvokeModel",
      "Resource": [
        "arn:aws:bedrock:us-east-1::foundation-model/amazon.nova-lite-v1:0",
        "arn:aws:bedrock:us-east-1::foundation-model/amazon.titan-embed-text-v2:0"
      ]
    }
  ]
}
```

## Performance Characteristics

### Latency

- **first_chain.py**: 100-500ms (depends on prompt length)
- **basic_rag.py**: 200-800ms (retrieval + generation)
- **pdf_rag.py**: 300-1000ms (PDF loading + retrieval + generation)

### Memory Usage

**FAISS Vector Store:**
- In-memory storage of all embeddings
- Scales with number of documents
- Example: 1000 documents × 1536 dimensions × 4 bytes ≈ 6MB

### Quality vs Speed

- **Chunk Size**: Larger = more context, slower retrieval
- **K (top results)**: More results = better context, slower
- **Score Threshold**: Higher = more accurate, fewer results

## Prompt Engineering for RAG

### System Prompts

**Good - Strict and Accurate:**
```
You are a helpful assistant. Only answer based on the provided context.
If the answer is not in the context, say you don't know.
```

**Good - Allows Some Elaboration:**
```
You are a knowledgeable assistant. Answer based on the provided context.
You can add relevant elaboration, but do not make up facts.
```

**Bad - Allows Hallucinations:**
```
You are a helpful assistant. Use your knowledge to answer.
```

## Error Handling and Best Practices

### Handling Empty Results

```python
results = retriever.invoke(question)
if not results:
    print("No relevant documents found")
else:
    for result in results:
        print(result.page_content)
```

### Handling Low Confidence

```python
retriever = vector_store.as_retriever(
    search_type="similarity_score_threshold",
    search_kwargs={"score_threshold": 0.5, "k": 5}  # Higher threshold
)
```

### Error Handling for PDF Loading

```python
from langchain_community.document_loaders import PyPDFLoader

try:
    loader = PyPDFLoader("document.pdf")
    docs = loader.load()
except FileNotFoundError:
    print("PDF file not found")
except Exception as e:
    print(f"Error loading PDF: {e}")
```

## Limitations

- FAISS stores all embeddings in memory (not suitable for millions of docs)
- Model availability limited to us-east-1 region
- PDF loading requires file system access
- No persistence between runs (embeddings not saved)
- Chunk size and separator must be tuned per use case
- Score threshold is arbitrary and requires calibration

## Advanced Features to Consider

- [ ] Persistent vector database (Pinecone, Weaviate, Milvus)
- [ ] Hybrid search (keyword + semantic)
- [ ] Multi-query retrieval (multiple retrieval attempts)
- [ ] Re-ranking of retrieved documents
- [ ] Chain-of-thought prompting for complex reasoning
- [ ] Streaming responses with callbacks
- [ ] Custom document metadata and filtering
- [ ] Memory/conversation history management
- [ ] Agents with tools and dynamic routing
- [ ] Caching for repeated queries
- [ ] Document summarization before embedding
- [ ] Multi-modal RAG (images + text)

## Advanced Patterns

### Query Expansion RAG

```python
# Generate multiple queries for better retrieval
queries = [original_query, expanded_query_1, expanded_query_2]
results = []
for query in queries:
    results.extend(retriever.invoke(query))
```

### Re-ranking with LLM

```python
# Use LLM to re-rank retrieved documents
retrieved = retriever.invoke(question)
# Use model to judge relevance of each document
```

### Multi-turn Conversation

```python
# Add memory management
from langchain.memory import ConversationBufferMemory
memory = ConversationBufferMemory()
# Use in chain for multi-turn conversations
```

## Troubleshooting

### Common Issues

**PDF Not Found**
```
Error: FileNotFoundError: No such file or directory: '../assets/books.pdf'
```
- Verify PDF path is correct relative to script location
- Check file exists in the specified directory

**Model Not Available**
```
Error: Model not found: amazon.nova-lite-v1:0
```
- Verify region is us-east-1
- Request model access in Bedrock console
- Check model ID spelling

**Empty Retrieval Results**
- Increase `k` value to retrieve more documents
- Lower `score_threshold` if using similarity_score_threshold
- Check if query matches documents semantically
- Verify documents are properly split

**Memory Issues with Large PDFs**
- Reduce `chunk_size` for smaller chunks
- Use persistent vector database instead of FAISS
- Process documents in batches

**Slow Performance**
- Reduce `k` (fewer documents to retrieve)
- Increase `chunk_size` (fewer total chunks)
- Use faster embedding model
- Implement caching for repeated queries

## References

- [LangChain Documentation](https://python.langchain.com/)
- [LangChain AWS Integration](https://python.langchain.com/docs/integrations/llms/bedrock/)
- [LangChain Community Integrations](https://python.langchain.com/docs/integrations/vectorstores/faiss/)
- [AWS Bedrock Documentation](https://docs.aws.amazon.com/bedrock/)
- [FAISS Documentation](https://github.com/facebookresearch/faiss)
- [RAG Best Practices](https://python.langchain.com/docs/use_cases/question_answering/)
- [Prompt Engineering Guide](https://python.langchain.com/docs/guides/prompt_templates)
- [Text Splitters](https://python.langchain.com/docs/modules/data_connection/document_transformers/)

