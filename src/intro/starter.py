"""
AWS Bedrock Foundation Models Exploration Script

This script demonstrates how to discover and explore available foundation models
in Amazon Bedrock. It provides functions to:
- List all available foundation models and their capabilities
- Get detailed information about a specific foundation model

Use this script to understand what models are available, their features,
pricing, and other metadata before building your applications.
"""

import boto3
import pprint

# Initialize Bedrock client - this is the main service client for interacting with Bedrock
# The Bedrock service (not bedrock-runtime) is used for model discovery and metadata operations
bedrock = boto3.client(
    service_name='bedrock',
    region_name='us-east-1')


# PrettyPrinter is used to format the JSON responses in a readable way
# depth=4 limits the nested structure display to 4 levels deep
pp = pprint.PrettyPrinter(depth=4)

def list_foundation_models():
    """
    Lists all available foundation models in Bedrock.
    
    This function retrieves the complete list of models you can use, including:
    - Model name and identifier
    - Provider (AWS, Anthropic, Meta, etc.)
    - Model capabilities (text, image, code, etc.)
    - Input and output modalities
    - Pricing information
    
    Returns: None (prints models to console via PrettyPrinter)
    """
    # Call the Bedrock API to get all available models
    models = bedrock.list_foundation_models()
    
    # Iterate through each model summary and display its information
    for model in models["modelSummaries"]:
        pp.pprint(model)
        pp.pprint("-------------------")

def get_foundation_model(modelIdentifier):
    """
    Gets detailed information about a specific foundation model.
    
    Args:
        modelIdentifier (str): The unique identifier of the model, e.g. 'anthropic.claude-v2'
    
    This function retrieves comprehensive details about a single model including:
    - Model features and capabilities
    - Input/output specifications
    - Supported parameters
    - Latency information
    - Pricing details
    
    Returns: None (prints model details to console via PrettyPrinter)
    """
    # Call the Bedrock API to get details for a specific model
    model = bedrock.get_foundation_model(modelIdentifier=modelIdentifier)
    pp.pprint(model)

# ============================================================================
# QUICK START - Uncomment the functions below to explore available models
# ============================================================================

# Uncomment this line to see ALL available foundation models and their details
# list_foundation_models()

# Uncomment this line to see detailed information about a specific model
# Get details for Claude v2 model
# get_foundation_model('anthropic.claude-v2')