import os
from typing import List, Dict
# from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL")

if not OPENAI_API_KEY or not OPENAI_BASE_URL:
    print("OPENAI_API_KEY or OPENAI_BASE_URL not set - using dummy strategy.")
    # raise ValueError("OPENAI_API_KEY or OPENAI_BASE_URL environment variable is not set.")

# client = OpenAI(
#     api_key=OPENAI_API_KEY,
#     base_url=OPENAI_BASE_URL,
# )

def generate_content_strategy(competitor_texts: List[str]) -> str:
    """
    Generate a content strategy using Kimi AI based on competitor content texts.
    
    Args:
        competitor_texts (List[str]): List of competitor content texts.
    
    Returns:
        str: The generated content strategy blueprint.
    """
    print("Reached generate_content_strategy, texts length:", len(competitor_texts))
    try:
        # Temporarily disabled for deployment
        print("AI strategy generation disabled for deployment.")
        return "Content strategy generation temporarily disabled. Please configure OpenAI API key for full functionality. Basic strategy: Analyze competitor content for key themes and keywords, structure your content to cover similar topics with better depth and user experience."
    except Exception as e:
        print(f"Exception in generate_content_strategy: {e}")
        raise Exception(f"Failed to generate content strategy: {e}")