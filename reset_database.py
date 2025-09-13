from src.database.manager import engine
from sqlalchemy import text

print("Connecting to the database to reset the table...")
try:
    # Drop the existing table and all its old data
    with engine.connect() as conn:
        conn.execute(text('DROP TABLE IF EXISTS scraped_pages'))
        conn.commit()
    print("✅ Table 'scraped_pages' has been successfully dropped.")
    print("It will be recreated with the correct new schema on the next app run.")
except Exception as e:
    print(f"❌ An error occurred during reset: {e}")