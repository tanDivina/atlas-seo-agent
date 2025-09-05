import os
from sqlalchemy import create_engine, text, Column, Integer, String, DateTime, Text, JSON
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv
import datetime
import numpy as np

# --- Database Setup ---
# Find the .env file in the root directory
dotenv_path = os.path.join(os.path.dirname(__file__), '..', '..', '.env')
load_dotenv(dotenv_path=dotenv_path)
DATABASE_URL = os.getenv("DATABASE_URL")

# This handles the SSL connection arguments correctly
connect_args = {
    'ssl_verify_identity': True,
    'ssl_ca': '/etc/ssl/cert.pem'
}
engine = create_engine(DATABASE_URL, connect_args=connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# --- Define Our Database Table with the NEW VECTOR COLUMN ---
class ScrapedPage(Base):
    __tablename__ = "scraped_pages"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    url = Column(String(500), nullable=False)
    content = Column(Text, nullable=True)
    scraped_at = Column(DateTime, default=datetime.datetime.utcnow)
    status = Column(String(50), default="scraped")
    qae_score = Column(Integer, default=0)
    
    # ADD THIS NEW VECTOR COLUMN (using JSON for compatibility)
    # The dimension (384) matches the AI model we are using
    content_embedding = Column(JSON, nullable=True)

# --- Functions (create_tables is unchanged) ---
def create_tables():
    """Creates the database tables if they don't exist."""
    print("Checking and creating tables if necessary...")
    Base.metadata.create_all(bind=engine)
    print("Tables are ready.")

# --- UPDATE THIS FUNCTION to accept the embedding ---
def save_scraped_content(url: str, content: str, qae_score: int, embedding: np.ndarray):
    db = SessionLocal()
    try:
        # Check if the URL already exists
        existing_page = db.query(ScrapedPage).filter(ScrapedPage.url == url).first()
        embedding_list = embedding.tolist()  # Convert numpy array to list for saving

        if existing_page:
            print(f"URL exists. Updating content, analysis, and embedding for: {url}")
            existing_page.content = content
            existing_page.scraped_at = datetime.datetime.utcnow()
            existing_page.status = "vectorized"
            existing_page.qae_score = qae_score
            existing_page.content_embedding = embedding_list
        else:
            print(f"Saving new content, analysis, and embedding for: {url}")
            new_page = ScrapedPage(url=url, content=content, qae_score=qae_score, status="vectorized", content_embedding=embedding_list)
            db.add(new_page)
        
        db.commit()
        print(f"✅ Successfully saved vector embedding to the database.")
    except Exception as e:
        print(f"❌ Error saving to database: {e}")
        db.rollback()
    finally:
        db.close()
