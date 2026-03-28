# src/recommender.py
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity


class HybridMovieRecommender:
    """
    Hybrid content-based recommender.
    Score = TF-IDF cosine similarity + genre overlap bonus + rating bonus
    FLOOR 3: operates on enriched_text vectors (title+genre+desc weighted)
    """

    def __init__(self, df, tfidf_matrix, genre_weight=0.15, rating_weight=0.1):
        self.df = df.reset_index(drop=True)
        self.tfidf_matrix = tfidf_matrix
        self.genre_weight = genre_weight
        self.rating_weight = rating_weight

        # Normalise ratings to 0-1 scale, fill missing with median
        if 'rating' in df.columns:
            ratings = pd.to_numeric(df['rating'], errors='coerce')
            ratings = ratings.fillna(ratings.median())
            self.df['norm_rating'] = (ratings - ratings.min()) / (ratings.max() - ratings.min() + 1e-9)
        else:
            self.df['norm_rating'] = 0.5

    def _get_genre_overlap(self, idx1, idx2):
        """
        Jaccard similarity between genre sets.
        FLOOR 3: uses expanded-genres (multi-label) over single genre field.
        """
        try:
            col = 'expanded-genres' if 'expanded-genres' in self.df.columns else 'genre'
            g1 = {g.strip().lower() for g in str(self.df.loc[idx1, col]).split(',')}
            g2 = {g.strip().lower() for g in str(self.df.loc[idx2, col]).split(',')}
            g1 = {g for g in g1 if g and g != 'nan'}
            g2 = {g for g in g2 if g and g != 'nan'}
            union = g1 | g2
            return len(g1 & g2) / len(union) if union else 0
        except Exception:
            return 0

    def recommend_by_title(self, title: str, top_n=5):
        """
        Find movie by title, return top N similar movies.
        FLOOR 3: fuzzy matches sorted by rating — best-known version wins.
        """
        col = 'movie title - year'

        # Exact match first
        matches = self.df[self.df[col].str.lower() == title.lower()]

        # Fuzzy fallback — sort by rating so highest-rated version wins
        if matches.empty:
            matches = self.df[
                self.df[col].str.lower().str.contains(title.lower(), na=False, regex=False)
            ].copy()
            if not matches.empty:
                matches['_r'] = pd.to_numeric(matches['rating'], errors='coerce')
                matches = matches.sort_values('_r', ascending=False, na_position='last')

        if matches.empty:
            return f"Movie '{title}' not found in dataset."

        idx = matches.index[0]
        print(f"  Matched: '{self.df.loc[idx, col]}'")
        return self._get_recommendations(idx, top_n)

    def recommend_by_genre(self, genre: str, top_n=5):
        """Filter by genre, return top-rated movies within it."""
        col = 'expanded-genres' if 'expanded-genres' in self.df.columns else 'genre'
        matches = self.df[self.df[col].str.lower().str.contains(genre.lower(), na=False)]

        if matches.empty:
            matches = self.df[self.df['genre'].str.lower().str.contains(genre.lower(), na=False)]
        if matches.empty:
            return f"No movies found for genre '{genre}'."

        matches = matches.copy()
        matches['norm_rating'] = self.df.loc[matches.index, 'norm_rating']
        top = matches.nlargest(top_n, 'norm_rating')

        return pd.DataFrame([{
            'title' : row['movie title - year'],
            'genre' : row.get('expanded-genres', row['genre']),
            'rating': row['rating'],
        } for _, row in top.iterrows()])

    def recommend_by_description(self, user_description: str, top_n=5):
        """
        Vectorize user free-text and find closest movies.
        FLOOR 3: added deduplication — no repeated titles in results.
        """
        from src.preprocess import clean_text

        if not hasattr(self, 'vectorizer'):
            return "Vectorizer not attached. Set recommender.vectorizer first."

        user_vec = self.vectorizer.transform([clean_text(user_description)])
        sim_scores = cosine_similarity(user_vec, self.tfidf_matrix).flatten()
        top_indices = sim_scores.argsort()[::-1][:top_n * 3]

        results, seen = [], set()
        for i in top_indices:
            title = self.df.loc[i, 'movie title - year']
            if title in seen:
                continue
            seen.add(title)
            results.append({
                'title'     : title,
                'similarity': round(float(sim_scores[i]), 4),
                'genre'     : self.df.loc[i, 'genre'],
                'rating'    : self.df.loc[i, 'rating'],
            })
            if len(results) == top_n:
                break

        return pd.DataFrame(results)

    def _get_recommendations(self, idx: int, top_n: int):
        """
        Core hybrid engine.
        1. Cosine similarity against all movies
        2. Add genre overlap + rating bonus
        3. Sort by hybrid score, deduplicate, return top N
        """
        sim_scores = cosine_similarity(
            self.tfidf_matrix[idx], self.tfidf_matrix
        ).flatten()

        hybrid_scores = []
        for i, base_sim in enumerate(sim_scores):
            if i == idx:
                continue
            score = base_sim \
                  + self._get_genre_overlap(idx, i) * self.genre_weight \
                  + float(self.df.loc[i, 'norm_rating']) * self.rating_weight
            hybrid_scores.append((i, score, base_sim))

        hybrid_scores.sort(key=lambda x: x[1], reverse=True)

        results, seen = [], set()
        for i, hybrid, base in hybrid_scores:
            title = self.df.loc[i, 'movie title - year']
            if title in seen:
                continue
            seen.add(title)
            results.append({
                'title'           : title,
                'hybrid_score'    : round(hybrid, 4),
                'tfidf_similarity': round(base, 4),
                'genre'           : self.df.loc[i, 'genre'],
                'rating'          : self.df.loc[i, 'rating'],
            })
            if len(results) == top_n:
                break

        return pd.DataFrame(results)