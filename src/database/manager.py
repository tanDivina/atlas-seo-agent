import os
import struct
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Text, text
from sqlalchemy.dialects.mysql import BLOB
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from typing import List
from dotenv import load_dotenv
import datetime
import numpy as np

dotenv_path = os.path.join(os.path.dirname(__file__), '..', '..', '.env')
load_dotenv(dotenv_path=dotenv_path)

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable not set.")

connect_args = {'ssl_verify_identity': False, 'ssl_ca': '/etc/ssl/cert.pem'}
engine = create_engine(DATABASE_URL, connect_args=connect_args, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class ScrapedPage(Base):
    __tablename__ = "scraped_pages"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    url = Column(String(1024), unique=True, index=True, nullable=False)
    content = Column(Text, nullable=True)
    scraped_at = Column(DateTime, default=datetime.datetime.utcnow)
    status = Column(String(50), default="scraped")
    qae_score = Column(Integer, default=0)
    content_embedding = Column(BLOB, nullable=True)  # BLOB for binary vectors

def create_tables():
    print("Checking and creating tables if necessary...")
    Base.metadata.create_all(bind=engine)
    print("Tables are ready.")

def save_scraped_content(url: str, content: str, qae_score: int, embedding: np.ndarray):
    db = SessionLocal()
    try:
        existing_page = db.query(ScrapedPage).filter(ScrapedPage.url == url).first()
        embedding_binary = struct.pack('384f', *embedding) if embedding is not None else None
        # Save as binary bytes
        if existing_page:
            print(f"URL exists. Updating content, analysis, and embedding for: {url}")
            existing_page.content = content
            existing_page.scraped_at = datetime.datetime.utcnow()
            existing_page.status = "vectorized"
            existing_page.qae_score = qae_score
            existing_page.content_embedding = embedding_binary
        else:
            print(f"Saving new content, analysis, and embedding for: {url}")
            new_page = ScrapedPage(url=url, content=content, qae_score=qae_score, status="vectorized", content_embedding=embedding_binary)
            db.add(new_page)
        db.commit()
        print(f"✅ Successfully saved vector embedding to the database.")
    except Exception as e:
        print(f"❌ Error saving to database: {e}")
        db.rollback()
    finally:
        db.close()

def search_similar_articles(search_embedding: np.ndarray, keyword: str = "") -> List[str]:
    """
    Search for similar articles using vector similarity or fallback to text-based search.
    """
    competitor_texts = []
    has_vector_support = False

    try:
        # Test if vector functions are available
        with engine.connect() as conn:
            result = conn.execute(text("SELECT VEC_L2_DISTANCE(VECTOR_FROM_BINARY('0000', 384), VECTOR_FROM_BINARY('0000', 384))")).fetchone()
            has_vector_support = True
            print("Vector search functions are available in TiDB.")
    except Exception as ve:
        has_vector_support = False
        print(f"Vector search not supported in this TiDB instance: {ve}")

    if has_vector_support:
        try:
            # Use vector search
            search_binary = struct.pack('384f', *search_embedding)
            with engine.connect() as conn:
                results = conn.execute(text("""
                    SELECT content FROM scraped_pages
                    WHERE content_embedding IS NOT NULL
                    ORDER BY VEC_L2_DISTANCE(VECTOR_FROM_BINARY(content_embedding, 384), VECTOR_FROM_BINARY(:search_vec, 384)) ASC
                    LIMIT 3
                """), {"search_vec": search_binary}).fetchall()
                competitor_texts = [row[0] for row in results if row[0]]
                print(f"Vector search retrieved {len(competitor_texts)} competitor texts.")
        except Exception as vector_error:
            print(f"Vector search failed: {vector_error}")
            competitor_texts = []
    else:
        # Fallback to text-based search
        try:
            with engine.connect() as conn:
                results = conn.execute(text("""
                    SELECT content FROM scraped_pages 
                    WHERE content LIKE :keyword 
                    LIMIT 3
                """), {"keyword": f"%{keyword}%" if keyword else "%"}).fetchall()
                competitor_texts = [row[0] for row in results if row[0]]
                print(f"Text fallback retrieved {len(competitor_texts)} competitor texts.")
        except Exception as text_error:
            print(f"Text fallback failed: {text_error}")
            competitor_texts = []

    if not competitor_texts:
        print("No competitor texts found. Using fallback prompt.")
        return ["No relevant competitor texts available. Generate strategy based on general best practices for the keyword."]

    return competitor_texts
