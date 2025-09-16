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

def generate_embedding_for_long_text(content: str, chunk_size: int = 512) -> np.ndarray:
    """
    Generates a vector embedding for long text by chunking and averaging embeddings.
    This prevents OOM for large content.
    """
    if not content:
        return np.array([])
    
    # Split content into chunks
    chunks = [content[i:i+chunk_size] for i in range(0, len(content), chunk_size)]
    print(f"Chunking content into {len(chunks)} chunks for embedding.")
    
    embeddings = []
    for chunk in chunks:
        chunk_embedding = generate_embedding(chunk)
        if len(chunk_embedding) > 0:
            embeddings.append(chunk_embedding)
    
    if not embeddings:
        return np.array([])
    
    # Average the embeddings
    avg_embedding = np.mean(embeddings, axis=0)
    print(f"Averaged embedding shape: {avg_embedding.shape}")
    return avg_embedding
