from sentence_transformers import SentenceTransformer
import numpy as np

# Load the AI model. This is slow, so we do it once when the script starts.
print("Loading sentence-transformer model...")
model = SentenceTransformer('paraphrase-MiniLM-L3-v2')
print("Model loaded.")

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
    """
    if not content:
        return np.array([])  # Return an empty array if there's no content
    
    print("Generating vector embedding for the content...")
    # The model.encode() function turns the text into a list of 384 numbers
    embedding = model.encode(content, normalize_embeddings=True)
    print(f"Embedding generated with shape: {embedding.shape}")
    return embedding
