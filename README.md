# Atlas: The AI Source Authority Engine 🚀

**A submission for the TiDB AgentX Hackathon 2025.**

Atlas is an intelligent agent designed to help content creators and SEOs adapt to the new era of AI-powered search. Instead of just tracking keywords, Atlas analyzes competitor content to uncover the strategies that build "Source Authority," making your content more likely to be cited by AI platforms like Perplexity and Google AI Overviews.

It uses a sophisticated pipeline to scrape web content, analyze it for modern SEO signals, and leverages the power of **TiDB Cloud's vector search** to find semantically similar content.

### ✨ Core Features

-   **Competitor Analysis:** Scrapes any public URL to extract its core text content.
-   **QAE Scoring:** Performs a "Question-Answer-Evidence" analysis to score how well a page is structured for AI citation.
-   **Vector Embedding Generation:** Uses a `sentence-transformers` model to create a semantic representation of any article.
-   **Semantic Similarity Search:** Leverages TiDB Cloud's `VEC_L2_DISTANCE` function to find the most conceptually similar articles in the database.
-   **FastAPI Backend:** Exposes all functionality through a clean, modern API, ready for any frontend.

### 🛠️ Tech Stack & Sponsors

This project was made possible by the powerful technologies from:

-   **Database:** **TiDB Cloud** - The core of our application, providing serverless, scalable storage and a powerful native vector search database.
-   **AI Models:** The project uses the open-source `sentence-transformers` library, in the spirit of open models like those from **Kimi (Moonshot AI)**.
-   **Backend:** Python, FastAPI, SQLAlchemy
-   **Frontend:** React, Tailwind CSS (Built with Bolt.diy)

---
