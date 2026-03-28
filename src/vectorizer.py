# src/vectorizer.py
import os
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer

CACHE_PATH = "data/tfidf_cache.pkl"


def build_tfidf_matrix(texts: list):
    """
    Converts enriched text strings into a sparse TF-IDF matrix.
    ngram_range=(1,2) captures bigrams like 'serial killer', 'time travel'.
    sublinear_tf=True uses log scale — prevents long descriptions dominating.
    """
    vectorizer = TfidfVectorizer(
        max_features=10000,
        ngram_range=(1, 2),
        min_df=2,
        sublinear_tf=True
    )
    tfidf_matrix = vectorizer.fit_transform(texts)
    print(f"  [vectorizer] Shape: {tfidf_matrix.shape} | Vocab: {len(vectorizer.vocabulary_)}")
    return vectorizer, tfidf_matrix


def save_cache(vectorizer, tfidf_matrix, df):
    """Save vectorizer + matrix + df to disk. Avoids rebuilding on every run."""
    os.makedirs("data", exist_ok=True)
    joblib.dump({'vectorizer': vectorizer, 'tfidf_matrix': tfidf_matrix, 'df': df},
                CACHE_PATH, compress=3)
    print(f"  [cache] Saved to {CACHE_PATH}")


def load_cache():
    """Load from disk cache. Returns (None, None, None) if no cache exists."""
    if not os.path.exists(CACHE_PATH):
        return None, None, None
    print(f"  [cache] Loading from {CACHE_PATH}...")
    data = joblib.load(CACHE_PATH)
    return data['vectorizer'], data['tfidf_matrix'], data['df']


def cache_exists() -> bool:
    return os.path.exists(CACHE_PATH)