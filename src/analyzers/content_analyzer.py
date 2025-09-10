import boto3
import json
import os
import numpy as np
from dotenv import load_dotenv

load_dotenv()

# Create a client to interact with the Bedrock API
bedrock_client = boto3.client(
    service_name='bedrock-runtime', 
    region_name=os.getenv("AWS_REGION", "us-east-1") # Default to us-east-1
)

def analyze_qae_score(content: str) -> int:
    """Calculates a simple QAE score by counting question marks."""
    if not content:
        return 0
    question_count = content.count('?')
    print(f"Content Analysis: Found {question_count} question marks.")
    return question_count

def generate_embedding_for_long_text(content: str) -> np.ndarray:
    """
    Generates a vector embedding for long text using the AWS Bedrock API.
    This uses ZERO local memory for the model.
    """
    print("Generating vector embedding via AWS Bedrock API...")
    if not content:
        return np.array([])
    
    try:
        # The body of the request needs to be a JSON string
        body = json.dumps({
            "inputText": content[:20000] # Titan has a very large token limit, but we'll cap it just in case
        })
        
        # The model ID for Titan Text Embeddings
        model_id = 'amazon.titan-embed-text-v1'
        
        # Invoke the model
        response = bedrock_client.invoke_model(
            body=body,
            modelId=model_id,
            accept='application/json',
            contentType='application/json'
        )
        
        # Parse the response
        response_body = json.loads(response['body'].read())
        embedding = np.array(response_body['embedding'])
        
        print(f"Successfully generated embedding with shape: {embedding.shape}")
        return embedding

    except Exception as e:
        print(f"❌ AWS Bedrock API Error: {e}")
        return np.array([])