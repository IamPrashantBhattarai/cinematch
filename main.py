# main.py
from datasets import load_dataset
from src.preprocess import preprocess_dataframe
from src.vectorizer import build_tfidf_matrix, save_cache, load_cache, cache_exists
from src.recommender import HybridMovieRecommender


def main():

    # Load from cache if available — skips the 60s rebuild
    if cache_exists():
        print("Cache found — loading from disk...")
        vectorizer, tfidf_matrix, df = load_cache()
        print(f"  Loaded {len(df)} movies.")
    else:
        print("No cache — building from scratch...")

        print("Loading dataset...")
        df = load_dataset("jquigl/imdb-genres")['train'].to_pandas()
        print(f"  Raw: {len(df)} rows")

        print("Preprocessing...")
        df = preprocess_dataframe(df)
        df = df.dropna(subset=['enriched_text'])
        df = df[df['movie title - year'].notna()]
        df = df.reset_index(drop=True)

        print("Vectorizing...")
        vectorizer, tfidf_matrix = build_tfidf_matrix(df['enriched_text'].tolist())

        print("Saving cache...")
        save_cache(vectorizer, tfidf_matrix, df)

    print("Building recommender...")
    recommender = HybridMovieRecommender(df, tfidf_matrix)
    recommender.vectorizer = vectorizer

    # ── Demo queries ──────────────────────────────────────────────────────
    print("\n" + "="*55)
    print("Recommendations for 'The Dark Knight'")
    print("="*55)
    print(recommender.recommend_by_title("The Dark Knight"))

    print("\n" + "="*55)
    print("Genre: Action")
    print("="*55)
    print(recommender.recommend_by_genre("Action"))

    print("\n" + "="*55)
    print("Description: 'a heist gone wrong with betrayal'")
    print("="*55)
    print(recommender.recommend_by_description("a heist gone wrong with betrayal"))


if __name__ == "__main__":
    main()