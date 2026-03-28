# app.py
import streamlit as st
import time

st.set_page_config(
    page_title="CineMatch — Movie Recommender",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700&family=DM+Sans:wght@300;400;500&family=DM+Mono&display=swap');

html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 2rem; padding-bottom: 2rem; }

.hero {
    background: linear-gradient(135deg, #0d0d0d 0%, #1a0a2e 50%, #0d1f3c 100%);
    border-radius: 20px; padding: 3rem 3rem 2.5rem; margin-bottom: 2rem;
    border: 1px solid rgba(255,255,255,0.07); position: relative; overflow: hidden;
}
.hero::before {
    content: ''; position: absolute; top: -60px; right: -60px;
    width: 300px; height: 300px;
    background: radial-gradient(circle, rgba(99,60,180,0.25) 0%, transparent 70%);
    pointer-events: none;
}
.hero-tag  { font-family:'DM Mono',monospace; font-size:11px; letter-spacing:0.18em; color:#7b6fe8; text-transform:uppercase; margin-bottom:0.75rem; }
.hero-title{ font-family:'Playfair Display',serif; font-size:3.2rem; font-weight:700; color:#f0eeff; line-height:1.1; margin-bottom:0.5rem; }
.hero-title span { color:#9b7ff0; }
.hero-sub  { font-size:1rem; color:rgba(255,255,255,0.45); font-weight:300; max-width:520px; line-height:1.6; }
.hero-badge{ display:inline-block; font-family:'DM Mono',monospace; font-size:10px; padding:3px 10px; border-radius:20px; background:rgba(29,200,120,0.12); border:1px solid rgba(29,200,120,0.3); color:#5dd4a0; margin-top:1rem; }
.hero-stats{ display:flex; gap:2.5rem; margin-top:1.5rem; }
.stat-num  { font-family:'Playfair Display',serif; font-size:1.6rem; color:#9b7ff0; font-weight:700; }
.stat-label{ font-size:11px; color:rgba(255,255,255,0.35); text-transform:uppercase; letter-spacing:0.1em; font-family:'DM Mono',monospace; }

[data-testid="stSidebar"] { background:#0d0d14 !important; border-right:1px solid rgba(255,255,255,0.06); }
[data-testid="stSidebar"] * { color:#c9c4e8 !important; }
.sidebar-logo    { font-family:'Playfair Display',serif; font-size:1.4rem; color:#9b7ff0 !important; font-weight:700; padding:0.5rem 0 1.5rem; border-bottom:1px solid rgba(255,255,255,0.06); margin-bottom:1.5rem; }
.sidebar-section { font-family:'DM Mono',monospace; font-size:10px; text-transform:uppercase; letter-spacing:0.14em; color:rgba(255,255,255,0.3) !important; margin:1.5rem 0 0.5rem; }

.results-header { font-family:'DM Mono',monospace; font-size:11px; text-transform:uppercase; letter-spacing:0.14em; color:rgba(255,255,255,0.35); margin-bottom:1rem; padding-bottom:0.5rem; border-bottom:1px solid rgba(255,255,255,0.06); }
.movie-card { background:linear-gradient(135deg,#13131f,#0f0f1a); border:1px solid rgba(255,255,255,0.07); border-radius:14px; padding:1.25rem 1.4rem; margin-bottom:0.75rem; position:relative; overflow:hidden; }
.movie-card:hover { border-color:rgba(155,127,240,0.4); }
.movie-card::before { content:''; position:absolute; left:0; top:0; bottom:0; width:3px; border-radius:3px 0 0 3px; }
.rank-1::before{background:#f0c040;} .rank-2::before{background:#b0b8c8;} .rank-3::before{background:#c87040;} .rank-4::before,.rank-5::before{background:#9b7ff0;}
.card-rank  { font-family:'DM Mono',monospace; font-size:10px; color:rgba(255,255,255,0.25); text-transform:uppercase; letter-spacing:0.1em; margin-bottom:0.35rem; }
.card-title { font-family:'Playfair Display',serif; font-size:1.1rem; color:#f0eeff; font-weight:700; line-height:1.3; }
.card-meta  { display:flex; gap:0.75rem; align-items:center; flex-wrap:wrap; margin-top:0.5rem; }
.badge      { font-family:'DM Mono',monospace; font-size:10px; padding:2px 8px; border-radius:20px; }
.badge-genre {background:rgba(155,127,240,0.15);border:1px solid rgba(155,127,240,0.3);color:#b8a8f0;}
.badge-score {background:rgba(26,200,120,0.12);border:1px solid rgba(26,200,120,0.25);color:#5dd4a0;}
.badge-rating{background:rgba(240,192,64,0.12);border:1px solid rgba(240,192,64,0.25);color:#f0c040;}
.score-bar-wrap{margin-top:0.6rem;background:rgba(255,255,255,0.05);border-radius:4px;height:4px;overflow:hidden;}
.score-bar{height:4px;border-radius:4px;background:linear-gradient(90deg,#9b7ff0,#5dd4a0);}

.stTextInput>div>div>input,.stTextArea>div>div>textarea,.stSelectbox>div>div {
    background:#13131f !important; border:1px solid rgba(155,127,240,0.25) !important;
    border-radius:10px !important; color:#f0eeff !important;
}
.stButton>button {
    background:linear-gradient(135deg,#6b4fd8,#9b7ff0) !important; color:white !important;
    border:none !important; border-radius:10px !important; padding:0.6rem 2rem !important;
    font-weight:500 !important; font-size:14px !important; width:100% !important;
}
.info-box { background:rgba(155,127,240,0.08); border:1px solid rgba(155,127,240,0.2); border-radius:10px; padding:0.85rem 1.1rem; color:rgba(200,190,255,0.8); font-size:13px; line-height:1.6; margin-bottom:1rem; }
.err-box  { background:rgba(220,60,60,0.1); border:1px solid rgba(220,60,60,0.25); border-radius:10px; padding:0.85rem 1.1rem; color:#f08080; font-size:13px; }
.empty-state { text-align:center; padding:3rem 1rem; color:rgba(255,255,255,0.2); }
.empty-icon  { font-size:2.5rem; margin-bottom:0.75rem; }
.empty-text  { font-size:14px; line-height:1.6; }
</style>
""", unsafe_allow_html=True)


# ── Model loading — two-layer cache ──────────────────────────────────────────
@st.cache_resource(show_spinner=False)
def load_model():
    from src.vectorizer import cache_exists, load_cache, build_tfidf_matrix, save_cache
    from src.preprocess import preprocess_dataframe
    from src.recommender import HybridMovieRecommender

    if cache_exists():
        vectorizer, tfidf_matrix, df = load_cache()
    else:
        from datasets import load_dataset
        df = load_dataset("jquigl/imdb-genres")['train'].to_pandas()
        df = preprocess_dataframe(df)
        df = df.dropna(subset=['enriched_text'])
        df = df[df['movie title - year'].notna()].reset_index(drop=True)
        vectorizer, tfidf_matrix = build_tfidf_matrix(df['enriched_text'].tolist())
        save_cache(vectorizer, tfidf_matrix, df)

    recommender = HybridMovieRecommender(df, tfidf_matrix)
    recommender.vectorizer = vectorizer
    return recommender, df


# ── Helpers ───────────────────────────────────────────────────────────────────
def render_card(row, rank, score_col='hybrid_score'):
    title  = row.get('movie title - year') or row.get('title', 'Unknown')
    genre  = str(row.get('genre', 'N/A')).strip()
    rating = row.get('rating', None)
    score  = row.get(score_col) or row.get('hybrid_score', 0)
    try:    sv = float(score)
    except: sv = 0.0
    try:    rs = f"★ {float(rating):.1f}" if rating and str(rating) != 'nan' else "★ N/A"
    except: rs = "★ N/A"
    return f"""
<div class="movie-card rank-{min(rank,5)}">
  <div class="card-rank">#{rank} match</div>
  <div class="card-title">{title}</div>
  <div class="card-meta">
    <span class="badge badge-genre">{genre[:35]}</span>
    <span class="badge badge-score">score {sv:.3f}</span>
    <span class="badge badge-rating">{rs}</span>
  </div>
  <div class="score-bar-wrap"><div class="score-bar" style="width:{min(int(sv*100),100)}%"></div></div>
</div>"""


def render_results(results, score_col='hybrid_score'):
    if isinstance(results, str):
        st.markdown(f'<div class="err-box">{results}</div>', unsafe_allow_html=True); return
    if results.empty:
        st.markdown('<div class="err-box">No results found.</div>', unsafe_allow_html=True); return
    st.markdown('<div class="results-header">Top recommendations</div>', unsafe_allow_html=True)
    for i, (_, row) in enumerate(results.iterrows(), 1):
        st.markdown(render_card(row, i, score_col), unsafe_allow_html=True)


# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown('<div class="sidebar-logo">CineMatch</div>', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-section">Search mode</div>', unsafe_allow_html=True)
    mode = st.radio("", ["By Title", "By Genre", "By Description"], label_visibility="collapsed")
    st.markdown('<div class="sidebar-section">Results</div>', unsafe_allow_html=True)
    top_n = st.slider("Number of recommendations", 3, 10, 5)
    st.markdown('<div class="sidebar-section">Floor 3 features</div>', unsafe_allow_html=True)
    st.markdown("""
    <div style="font-size:12px;color:rgba(255,255,255,0.3);line-height:1.9;">
    Title weight ×3<br>Genre weight ×2<br>Expanded-genres Jaccard<br>
    Rating-sorted fuzzy match<br>Stub description filter<br>Joblib disk cache
    </div>""", unsafe_allow_html=True)


# ── Hero ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
  <div class="hero-tag">AI/ML Internship — Floor 3</div>
  <div class="hero-title">Cine<span>Match</span></div>
  <div class="hero-sub">Weighted multi-field TF-IDF · Expanded-genre Jaccard · Rating-aware hybrid scoring</div>
  <div class="hero-badge">Title ×3 · Genre ×2 · Joblib cache</div>
  <div class="hero-stats">
    <div><div class="stat-num">238K+</div><div class="stat-label">Movies</div></div>
    <div><div class="stat-num">3×</div><div class="stat-label">Title weight</div></div>
    <div><div class="stat-num">10K</div><div class="stat-label">Features</div></div>
    <div><div class="stat-num">Hybrid</div><div class="stat-label">Scoring</div></div>
  </div>
</div>
""", unsafe_allow_html=True)

with st.spinner("Loading model — first run ~60s, cached runs ~3s..."):
    recommender, df = load_model()

# ── Search panel ──────────────────────────────────────────────────────────────
col_input, col_results = st.columns([1, 1.4], gap="large")

with col_input:
    st.markdown("#### Search")

    if mode == "By Title":
        st.markdown('<div class="info-box">Include the year for precision — e.g. <b>The Dark Knight - 2008</b>. Fuzzy matches rank by rating.</div>', unsafe_allow_html=True)
        title_input = st.text_input("", placeholder="e.g. The Dark Knight, Inception...", label_visibility="collapsed")
        if st.button("Find similar movies"):
            if title_input.strip():
                with st.spinner("Searching..."):
                    results = recommender.recommend_by_title(title_input.strip(), top_n=top_n)
                col = 'movie title - year'
                fuzzy = recommender.df[
                    recommender.df[col].str.lower().str.contains(title_input.strip().lower(), na=False, regex=False)
                ][[col, 'genre', 'rating']].head(6)
                if len(fuzzy) > 1:
                    with col_input:
                        st.markdown('<div class="info-box">Multiple matches found — showing highest-rated. Add year for exact match.</div>', unsafe_allow_html=True)
                        st.dataframe(fuzzy.rename(columns={col: 'Title'}), hide_index=True, use_container_width=True)
                with col_results:
                    render_results(results)
            else:
                st.markdown('<div class="err-box">Please enter a movie title.</div>', unsafe_allow_html=True)

    elif mode == "By Genre":
        st.markdown('<div class="info-box">Results ranked by rating within the selected genre.</div>', unsafe_allow_html=True)
        genre_col = 'expanded-genres' if 'expanded-genres' in df.columns else 'genre'
        all_genres = sorted({
            g.strip() for cell in df[genre_col].dropna()
            for g in str(cell).split(',')
            if g.strip() and g.strip().lower() != 'nan'
        })
        genre_input = st.selectbox("", options=all_genres, label_visibility="collapsed")
        if st.button("Browse genre"):
            with st.spinner("Fetching..."):
                results = recommender.recommend_by_genre(genre_input, top_n=top_n)
            with col_results:
                render_results(results, score_col='rating')

    elif mode == "By Description":
        st.markdown('<div class="info-box">Describe a plot in your own words. Vectorized using the same TF-IDF vocabulary as the full dataset.</div>', unsafe_allow_html=True)
        desc_input = st.text_area("", placeholder="e.g. a detective solving a murder in a rainy city...", height=120, label_visibility="collapsed")
        if st.button("Find matching movies"):
            if desc_input.strip():
                with st.spinner("Analysing..."):
                    results = recommender.recommend_by_description(desc_input.strip(), top_n=top_n)
                with col_results:
                    render_results(results, score_col='similarity')
            else:
                st.markdown('<div class="err-box">Please enter a description.</div>', unsafe_allow_html=True)

with col_results:
    if 'results' not in dir():
        st.markdown("""
        <div class="empty-state">
          <div class="empty-icon">🎬</div>
          <div class="empty-text">Recommendations appear here.<br>Choose a mode and enter your query.</div>
        </div>""", unsafe_allow_html=True)