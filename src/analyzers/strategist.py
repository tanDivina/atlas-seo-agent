import os
from typing import List, Dict
from openai import OpenAI
from google import genai
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL")

if not OPENAI_API_KEY or not OPENAI_BASE_URL:
    raise ValueError("OPENAI_API_KEY or OPENAI_BASE_URL environment variable is not set.")

client = OpenAI(
    api_key=OPENAI_API_KEY,
    base_url=OPENAI_BASE_URL,
)

client = genai.Client()

groq_key = os.getenv("GROQ_API_KEY")
if groq_key:
    groq_client = Groq(api_key=groq_key)

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
        prompt = """
        Analyze the following competitor content texts and generate a comprehensive content strategy blueprint for creating superior content:
        
        """ + "\n\n".join(competitor_texts) + """
        
        Provide a step-by-step strategy for content creation, including key themes, keywords, structure, and optimization tips.
        """
        print("Sending to Moonshot:", prompt[:200] + "..." if len(prompt) > 200 else prompt)

        gemini_key = os.getenv("GEMINI_API_KEY")
        if gemini_key:
            try:
                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=prompt
                )
                print("Gemini response:", response.text[:200])
                return response.text
            except Exception as gemini_error:
                print(f"Gemini error: {gemini_error}")
                print("Falling back to Groq...")
        
        if groq_key:
            try:
                groq_response = groq_client.chat.completions.create(
                    model="llama3-70b-8192",
                    messages=[
                        {"role": "system", "content": "You are a content strategist AI. Provide detailed, actionable content strategies based on competitor analysis."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.7,
                    max_tokens=1500
                )
                print("Groq response:", groq_response.choices[0].message.content[:200])
                return groq_response.choices[0].message.content
            except Exception as groq_error:
                print(f"Groq error: {groq_error}")
                print("Falling back to Moonshot...")
        
        try:
            response = client.chat.completions.create(
                model="kimi-k2-turbo-preview",
                messages=[
                    {"role": "system", "content": "You are a content strategist AI. Provide detailed, actionable content strategies based on competitor analysis."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=1500
            )
            print("Moonshot response:", response.choices[0].message.content[:200] if response.choices else "Empty response")
            return response.choices[0].message.content or "No response from Moonshot - check quota/key."
        except Exception as e:
            print(f"Moonshot error: {e}")
            return f"Strategy generation failed: {str(e)}. Verify Moonshot API key and quota."
    except Exception as e:
        print(f"Exception in generate_content_strategy: {e}")
        raise Exception(f"Failed to generate content strategy: {e}")