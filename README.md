# CineMatch — Movie Recommendation System

> AI/ML Internship Task · Content-based recommender using TF-IDF + Cosine Similarity
> Dataset: [jquigl/imdb-genres](https://huggingface.co/datasets/jquigl/imdb-genres) · 238K+ movies

---

## Overview

CineMatch is a **content-based movie recommendation system** built without pre-trained embeddings. It uses a weighted TF-IDF matrix over multi-field enriched text (title + genre + description), then ranks candidates using a hybrid score combining cosine similarity, genre Jaccard overlap, and normalised rating.

The app ships as a **Streamlit web UI** and is fully containerised on Docker Hub.

---

## Features

| Input Mode | What it does |
|---|---|
| By Title | Fuzzy-matches the title, returns top-N similar movies |
| By Genre | Filters by genre, ranks by rating |
| By Description | Vectorises free-text query, finds closest movies |

---

## Project Structure

```
movie_recommender/
├── app.py                  # Streamlit UI
├── main.py                 # CLI demo (no UI)
├── requirements.txt
├── Dockerfile
├── .dockerignore
├── src/
│   ├── __init__.py
│   ├── preprocess.py       # Text cleaning + enriched-text builder
│   ├── vectorizer.py       # TF-IDF builder + joblib cache
│   └── recommender.py      # HybridMovieRecommender class
└── data/                   # Auto-created at runtime; stores tfidf_cache.pkl
```

---

## Setup Instructions

### Option 1 — Run with Docker (recommended)

```bash
docker pull prashant058/cinematch:latest
docker run -p 8501:8501 prashant058/cinematch:latest
```

Open `http://localhost:8501` in your browser.
First run downloads the dataset and builds the cache (~60s). Subsequent runs load from cache (~3s).

---

### Option 2 — Run Locally

**Prerequisites:** Python 3.10+

```bash
# 1. Clone the repo
git clone https://github.com/prashant058/cinematch.git
cd cinematch

# 2. Create and activate a virtual environment
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Launch the Streamlit app
streamlit run app.py
```

Or run the CLI demo (no UI):

```bash
python main.py
```

---

## Approach

### 1. Data Preprocessing (`src/preprocess.py`)

Each movie's text fields go through a standard NLP cleaning pipeline:

| Step | Detail |
|---|---|
| Lowercase | Normalises casing |
| Remove punctuation | Strips non-alpha characters via regex `[^a-z\s]` |
| Remove stopwords | NLTK English stopwords list |
| Lemmatization | WordNetLemmatizer — reduces inflected words to base form |
| Stub filter | Drops descriptions with fewer than 8 words (noise removal) |

After cleaning, a **weighted enriched text** field is built per movie:

```
enriched_text = title × 3  +  genre × 2  +  description × 1
```

Repeating fields boosts their TF-IDF weight — the same field-weighting technique used by production search engines like Elasticsearch.

---

### 2. Vectorization (`src/vectorizer.py`)

**Method chosen: TF-IDF** (over Bag-of-Words)

| Setting | Value | Reason |
|---|---|---|
| `max_features` | 10,000 | Caps vocabulary; keeps matrix sparse and fast |
| `ngram_range` | (1, 2) | Captures bigrams like *serial killer*, *time travel* |
| `min_df` | 2 | Ignores terms appearing in only one movie (likely typos) |
| `sublinear_tf` | True | Log-scale TF — prevents long descriptions dominating |

**Why TF-IDF over BoW?**
BoW treats all term frequencies as raw counts, so frequent but uninformative words like *"film"* or *"story"* score high. TF-IDF down-weights terms that are common across the entire corpus, surfacing genuinely discriminative words instead.

The fitted vectorizer and matrix are persisted to `data/tfidf_cache.pkl` via `joblib`, skipping the 60-second rebuild on subsequent runs.

---

### 3. Recommendation Logic (`src/recommender.py`)

**Hybrid scoring formula:**

```
hybrid_score = cosine_similarity
             + jaccard_genre_overlap × 0.15
             + normalised_rating     × 0.10
```

| Component | Role |
|---|---|
| Cosine similarity | Primary signal — measures angle between TF-IDF vectors |
| Genre Jaccard overlap | Bonus for movies sharing genre labels (uses `expanded-genres` when available) |
| Rating bonus | Breaks ties in favour of higher-rated movies |
| Deduplication | Results never contain the same title twice |

For free-text queries (`recommend_by_description`), the user's input goes through the same preprocessing pipeline and is transformed using the already-fitted vectorizer.

---

## Example Outputs

### By Title — "The Dark Knight"

| # | Title | Hybrid Score | TF-IDF Sim | Genre | Rating |
|---|---|---|---|---|---|
| 1 | The Dark Knight Rises - 2012 | 0.4821 | 0.3910 | Action | 8.4 |
| 2 | Batman Begins - 2005 | 0.4103 | 0.3201 | Action | 8.2 |
| 3 | Batman - 1989 | 0.3817 | 0.2990 | Action | 7.6 |
| 4 | Joker - 2019 | 0.3542 | 0.2710 | Crime/Drama | 8.4 |
| 5 | V for Vendetta - 2005 | 0.3201 | 0.2488 | Action | 8.1 |

### By Description — "a heist gone wrong with betrayal"

| # | Title | Similarity | Genre | Rating |
|---|---|---|---|---|
| 1 | Heat - 1995 | 0.2943 | Crime | 8.2 |
| 2 | The Italian Job - 2003 | 0.2711 | Action | 7.0 |
| 3 | Ocean's Eleven - 2001 | 0.2588 | Crime | 7.8 |

---

## Limitations

1. **No semantic understanding** — TF-IDF cannot understand that *"cop"* and *"police officer"* are synonyms, or that *"not funny"* is negative sentiment.
2. **Cold-start on descriptions** — movies with very short or missing descriptions are filtered out (stub filter), reducing catalogue coverage.
3. **Static vocabulary** — the vectorizer is fitted once on the training split. New movies require a full rebuild.
4. **No user personalisation** — purely content-based; cannot learn from individual watch history or preferences.
5. **Inconsistent genre labels** — the dataset uses inconsistent labels (e.g. `"Sci-Fi"` vs `"Science Fiction"`), reducing Jaccard accuracy.
6. **Memory footprint** — the full 238K-movie TF-IDF matrix (~90MB) must be loaded into RAM at startup.

---

## Potential Improvements

| Area | Improvement |
|---|---|
| Semantic similarity | Replace TF-IDF with sentence-transformers (e.g. `all-MiniLM-L6-v2`) for contextual embeddings |
| Scalability | Use approximate nearest-neighbour search (FAISS / Annoy) instead of brute-force cosine over 238K vectors |
| Personalisation | Add collaborative filtering (matrix factorisation) on top of content scores |
| Genre normalisation | Canonicalise genre labels with a lookup table before computing Jaccard |
| Incremental updates | Use a vector database (Pinecone, Weaviate) for live updates without full rebuild |
| Evaluation | Collect explicit relevance labels and measure NDCG@K or Precision@K |

---

## Metrics for Evaluation

Since this is an unsupervised system (no ground-truth relevance labels), evaluation uses proxy metrics:

| Metric | How to compute | What it measures |
|---|---|---|
| **Genre precision** | % of top-N results sharing at least one genre with the query movie | Relevance proxy |
| **Intra-list diversity** | Average pairwise cosine distance among top-N results | Avoids near-duplicate recommendations |
| **Coverage** | % of catalogue appearing in at least one recommendation list | Avoids popularity bias |
| **Serendipity** | % of results not in the query movie's franchise/sequel chain | Novelty |
| **NDCG@K** | Requires human-labelled relevance judgements; gold standard | Ranking quality |

---

## Tech Stack

| Component | Technology |
|---|---|
| Language | Python 3.11 |
| Data loading | HuggingFace `datasets` |
| NLP preprocessing | NLTK (stopwords, WordNet lemmatizer) |
| Vectorization | Scikit-learn `TfidfVectorizer` |
| Similarity | Scikit-learn `cosine_similarity` |
| Caching | `joblib` |
| UI | Streamlit |
| Containerisation | Docker → Docker Hub (`prashant058/cinematch`) |

---

## Docker Hub

```bash
docker pull prashant058/cinematch:latest
```

Image: [hub.docker.com/r/prashant058/cinematch](https://hub.docker.com/r/prashant058/cinematch)
