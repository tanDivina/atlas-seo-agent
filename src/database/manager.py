import os
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv
import datetime
import numpy as np

dotenv_path = os.path.join(os.path.dirname(__file__), '..', '..', '.env')
load_dotenv(dotenv_path=dotenv_path)
DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL, pool_pre_ping=True)
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
    content_embedding = Column(Text, nullable=True)  # Store as JSON string for TiDB VECTOR

def create_tables():
    print("Checking and creating tables if necessary...")
    Base.metadata.create_all(bind=engine)
    print("Tables are ready.")

def save_scraped_content(url: str, content: str, qae_score: int, embedding: np.ndarray):
    db = SessionLocal()
    try:
        existing_page = db.query(ScrapedPage).filter(ScrapedPage.url == url).first()
        embedding_list = embedding.tolist() if embedding is not None else None
        import json
        embedding_json = json.dumps(embedding_list) if embedding_list else None

        if existing_page:
            print(f"URL exists. Updating content, analysis, and embedding for: {url}")
            existing_page.content = content
            existing_page.scraped_at = datetime.datetime.utcnow()
            existing_page.status = "vectorized"
            existing_page.qae_score = qae_score
            existing_page.content_embedding = embedding_json
        else:
            print(f"Saving new content, analysis, and embedding for: {url}")
            new_page = ScrapedPage(url=url, content=content, qae_score=qae_score, status="vectorized", content_embedding=embedding_json)
            db.add(new_page)
        db.commit()
        print(f"✅ Successfully saved vector embedding to the database.")
    except Exception as e:
        print(f"❌ Error saving to database: {e}")
        db.rollback()
    finally:
        db.close()