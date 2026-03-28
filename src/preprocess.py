# src/preprocess.py
import re
import nltk
import pandas as pd
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

nltk.download('stopwords', quiet=True)
nltk.download('wordnet', quiet=True)
nltk.download('omw-1.4', quiet=True)

lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words('english'))


def clean_text(text: str) -> str:
    """Lowercase → remove punctuation → remove stopwords → lemmatize."""
    if not isinstance(text, str) or text.strip() == "":
        return ""
    text = text.lower()
    text = re.sub(r'[^a-z\s]', '', text)
    tokens = [t for t in text.split() if t not in stop_words]
    tokens = [lemmatizer.lemmatize(t) for t in tokens]
    return ' '.join(tokens)


def build_enriched_text(row: pd.Series) -> str:
    """
    FLOOR 3: Weighted multi-field fusion.
    Title × 3 + Genre × 2 + Description × 1
    Repeating fields boosts their TF-IDF weight — same trick used by
    production search engines like Elasticsearch (field weighting).
    """
    clean_title = clean_text(str(row.get('movie title - year', '')))

    if 'expanded-genres' in row.index and pd.notna(row.get('expanded-genres')):
        clean_genre = clean_text(str(row['expanded-genres']))
    else:
        clean_genre = clean_text(str(row.get('genre', '')))

    clean_desc = clean_text(str(row.get('description', '')))

    return f"{clean_title} {clean_title} {clean_title} " \
           f"{clean_genre} {clean_genre} " \
           f"{clean_desc}".strip()


def preprocess_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """
    Full preprocessing pipeline.
    FLOOR 3 additions:
      - Filters stub descriptions (< 8 words) — removes noise movies
      - Builds enriched_text column (title+genre+desc weighted)
    """
    df = df.copy()

    if 'description' not in df.columns:
        raise ValueError(f"Column 'description' not found. Got: {df.columns.tolist()}")

    # Clean description — still needed for query vectorization
    df['clean_description'] = df['description'].apply(clean_text)

    # Filter stub descriptions
    df['desc_word_count'] = df['clean_description'].str.split().str.len()
    before = len(df)
    df = df[df['desc_word_count'] >= 8]
    print(f"  [preprocess] Removed {before - len(df)} stub descriptions. Remaining: {len(df)}")

    # Build enriched text per row
    df['enriched_text'] = df.apply(build_enriched_text, axis=1)
    df = df[df['enriched_text'].str.strip() != ""]

    return df