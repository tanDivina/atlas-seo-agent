from sentence_transformers import SentenceTransformer
import numpy as np

# Model loading disabled for deployment to save memory
# from sentence_transformers import SentenceTransformer
# print("Loading sentence-transformer model...")
# model = SentenceTransformer('paraphrase-MiniLM-L3-v2')
# print("Model loaded.")

def analyze_qae_score(content: str) -> int:
    """
    Calculates a simple QAE score by counting question marks.
    """
    if not content:
        return 0
    
    question_count = content.count('?')
    print(f"Content Analysis: Found {question_count} question marks.")
    return question_count

def generate_embedding(content: str) -> np.ndarray:
    """
    Generates a vector embedding for the given text content.
    Temporarily disabled for deployment.
    """
    if not content:
        return np.array([])  # Return an empty array if there's no content
    
    print("Embedding generation disabled for deployment.")
    return np.zeros(384)  # Dummy embedding to match model dimension

def generate_embedding_for_long_text(content: str, chunk_size: int = 512) -> np.ndarray:
    """
    Generates a vector embedding for long text by chunking and averaging embeddings.
    Temporarily disabled for deployment.
    """
    if not content:
        return np.array([])
    
    print("Long text embedding generation disabled for deployment.")
    return np.zeros(384)  # Dummy embedding to match model dimension
