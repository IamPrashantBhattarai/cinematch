"""
Generates screenshots/cosine_similarity_explained.png
Run: python generate_diagram.py
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.patheffects as pe
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch
from matplotlib.gridspec import GridSpec

plt.rcParams['font.family'] = 'DejaVu Sans'

FIG_BG   = '#0d0d14'
CARD_BG  = '#13131f'
BORDER   = '#2a2a3e'
PURPLE   = '#9b7ff0'
GREEN    = '#5dd4a0'
GOLD     = '#f0c040'
WHITE    = '#f0eeff'
MUTED    = '#6b6b8a'
RED      = '#f08080'

fig = plt.figure(figsize=(18, 13), facecolor=FIG_BG)
fig.text(0.5, 0.965, 'How CineMatch Computes Movie Similarity',
         ha='center', va='top', fontsize=20, fontweight='bold', color=WHITE)
fig.text(0.5, 0.945, 'TF-IDF Vectorization  →  Cosine Similarity  →  Hybrid Scoring',
         ha='center', va='top', fontsize=11, color=MUTED)

gs = GridSpec(3, 3, figure=fig,
              left=0.04, right=0.97, top=0.92, bottom=0.04,
              hspace=0.55, wspace=0.35)


# ── helpers ──────────────────────────────────────────────────────────────────
def card(ax, title, title_color=PURPLE):
    ax.set_facecolor(CARD_BG)
    for spine in ax.spines.values():
        spine.set_edgecolor(BORDER)
        spine.set_linewidth(1.4)
    ax.set_xticks([]); ax.set_yticks([])
    ax.set_title(title, color=title_color, fontsize=11,
                 fontweight='bold', pad=8, loc='left')

def arrow(ax, x0, y0, x1, y1, color=PURPLE, lw=1.5):
    ax.annotate('', xy=(x1, y1), xytext=(x0, y0),
                arrowprops=dict(arrowstyle='->', color=color,
                                lw=lw, mutation_scale=14))


# ══════════════════════════════════════════════════════════════════════════════
# PANEL 1 — Preprocessing pipeline
# ══════════════════════════════════════════════════════════════════════════════
ax1 = fig.add_subplot(gs[0, :])
card(ax1, '① Text Preprocessing Pipeline', GREEN)
ax1.set_xlim(0, 10); ax1.set_ylim(0, 1)

steps = [
    ('Raw Text',         '"The Dark Knight - 2008"',         0.45, '#3a2a5e'),
    ('Lowercase',        '"the dark knight  2008"',           2.05, '#2a3a5e'),
    ('Remove Punct',     '"the dark knight  2008"',           3.65, '#2a3a5e'),
    ('Remove Stopwords', '"dark knight 2008"',                5.25, '#2a3a5e'),
    ('Lemmatize',        '"dark knight 2008"',                6.85, '#2a3a5e'),
    ('Enriched Text',    'title×3 + genre×2 + desc×1',       8.55, '#1a3a2e'),
]

for label, example, x, bg in steps:
    box = FancyBboxPatch((x - 0.75, 0.15), 1.5, 0.68,
                         boxstyle='round,pad=0.05',
                         facecolor=bg, edgecolor=BORDER, linewidth=1.2)
    ax1.add_patch(box)
    ax1.text(x, 0.67, label,   ha='center', va='center',
             fontsize=8.5, fontweight='bold', color=WHITE)
    ax1.text(x, 0.34, example, ha='center', va='center',
             fontsize=7.2, color=GREEN, style='italic')

for i in range(len(steps) - 1):
    x0 = steps[i][2] + 0.75
    x1 = steps[i+1][2] - 0.75
    arrow(ax1, x0, 0.49, x1, 0.49, color=PURPLE)

ax1.text(8.55, 0.06, '★ Title repeated ×3 boosts TF-IDF weight (field weighting)',
         ha='center', fontsize=7.5, color=GOLD)


# ══════════════════════════════════════════════════════════════════════════════
# PANEL 2 — TF-IDF concept
# ══════════════════════════════════════════════════════════════════════════════
ax2 = fig.add_subplot(gs[1, 0])
card(ax2, '② TF-IDF Score per Term', PURPLE)
ax2.set_xlim(0, 1); ax2.set_ylim(0, 1)

ax2.text(0.5, 0.90, 'TF-IDF(t, d) = TF(t,d)  ×  IDF(t)',
         ha='center', fontsize=10, fontweight='bold', color=WHITE)

sections = [
    (0.25, 0.68, 'TF(t, d)', 'log(1 + count of term t\nin document d)', PURPLE),
    (0.75, 0.68, 'IDF(t)',   'log( N / df(t) )\nN=corpus size, df=doc freq', GREEN),
]
for x, y, title, body, col in sections:
    ax2.text(x, y, title, ha='center', fontsize=9.5,
             fontweight='bold', color=col)
    ax2.text(x, y - 0.18, body, ha='center', fontsize=8,
             color=WHITE, linespacing=1.5)

ax2.plot([0.5, 0.5], [0.44, 0.52], color=BORDER, lw=1)

ax2.text(0.5, 0.32, 'sublinear_tf=True  →  log scale\nprevents long descriptions dominating',
         ha='center', fontsize=8, color=GOLD, linespacing=1.6,
         bbox=dict(boxstyle='round,pad=0.4', facecolor='#2a2000', edgecolor=GOLD, lw=0.8))

ax2.text(0.5, 0.10, 'Output: sparse matrix  (238K movies × 10K features)',
         ha='center', fontsize=8, color=MUTED)


# ══════════════════════════════════════════════════════════════════════════════
# PANEL 3 — Vector space + angle diagram
# ══════════════════════════════════════════════════════════════════════════════
ax3 = fig.add_subplot(gs[1, 1])
card(ax3, '③ Vector Space (2D illustration)', PURPLE)
ax3.set_xlim(-0.1, 1.15); ax3.set_ylim(-0.1, 1.15)
ax3.set_aspect('equal')

ax3.axhline(0, color=BORDER, lw=0.8)
ax3.axvline(0, color=BORDER, lw=0.8)
ax3.text(1.10, -0.07, 'dim 1', fontsize=7, color=MUTED)
ax3.text(-0.09, 1.10, 'dim 2', fontsize=7, color=MUTED)

vA = np.array([0.85, 0.70])
vB = np.array([0.55, 0.90])
vC = np.array([0.20, 0.95])

for v, col, lbl, off in [(vA, PURPLE, 'Movie A\n(Dark Knight)', (0.04, -0.06)),
                          (vB, GREEN,  'Movie B\n(Batman Begins)', (0.04, 0.02)),
                          (vC, RED,    'Movie C\n(Comedy)', (-0.05, 0.04))]:
    ax3.annotate('', xy=v, xytext=(0, 0),
                 arrowprops=dict(arrowstyle='->', color=col, lw=2))
    ax3.text(v[0]+off[0], v[1]+off[1], lbl,
             fontsize=7.5, color=col, fontweight='bold')

theta_A = np.degrees(np.arctan2(vA[1], vA[0]))
theta_B = np.degrees(np.arctan2(vB[1], vB[0]))
arc = mpatches.Arc((0,0), 0.38, 0.38,
                   theta1=theta_A, theta2=theta_B,
                   color=GOLD, lw=1.5)
ax3.add_patch(arc)
mid = np.radians((theta_A + theta_B) / 2)
ax3.text(0.26*np.cos(mid), 0.26*np.sin(mid), 'θ',
         fontsize=11, color=GOLD, fontweight='bold')

cos_AB = np.dot(vA, vB) / (np.linalg.norm(vA) * np.linalg.norm(vB))
cos_AC = np.dot(vA, vC) / (np.linalg.norm(vA) * np.linalg.norm(vC))
ax3.text(0.5, -0.08,
         f'sim(A,B) = {cos_AB:.3f}   sim(A,C) = {cos_AC:.3f}',
         ha='center', fontsize=8, color=WHITE)


# ══════════════════════════════════════════════════════════════════════════════
# PANEL 4 — Cosine similarity formula
# ══════════════════════════════════════════════════════════════════════════════
ax4 = fig.add_subplot(gs[1, 2])
card(ax4, '④ Cosine Similarity Formula', PURPLE)
ax4.set_xlim(0, 1); ax4.set_ylim(0, 1)

ax4.text(0.5, 0.88,
         'cos(A, B)  =  A · B\n             ‖A‖ × ‖B‖',
         ha='center', fontsize=13, fontweight='bold', color=WHITE,
         linespacing=1.8,
         bbox=dict(boxstyle='round,pad=0.5', facecolor='#1e1030',
                   edgecolor=PURPLE, lw=1.5))

props = [
    ('A · B', 'Dot product  =  Σ aᵢ × bᵢ\n(shared weighted terms)', PURPLE),
    ('‖A‖, ‖B‖', 'L2 norms  =  √(Σ aᵢ²)\n(length normalisation)', GREEN),
    ('Result range', '0  (orthogonal)  →  1  (identical)\nHigher = more similar', GOLD),
]
y = 0.55
for title, desc, col in props:
    ax4.text(0.08, y, f'▸ {title}:', fontsize=8.5,
             fontweight='bold', color=col)
    ax4.text(0.08, y - 0.085, desc, fontsize=8,
             color=WHITE, linespacing=1.5)
    y -= 0.21

ax4.text(0.5, 0.02, 'sklearn: cosine_similarity(tfidf_matrix[idx], tfidf_matrix)',
         ha='center', fontsize=7.5, color=MUTED, style='italic')


# ══════════════════════════════════════════════════════════════════════════════
# PANEL 5 — Hybrid scoring formula (full width)
# ══════════════════════════════════════════════════════════════════════════════
ax5 = fig.add_subplot(gs[2, :])
card(ax5, '⑤ Hybrid Scoring — Final Ranking Formula', GOLD)
ax5.set_xlim(0, 10); ax5.set_ylim(0, 1)

ax5.text(5.0, 0.82,
         'hybrid_score  =  cosine_similarity  +  genre_jaccard × 0.15  +  norm_rating × 0.10',
         ha='center', fontsize=13, fontweight='bold', color=WHITE,
         bbox=dict(boxstyle='round,pad=0.45', facecolor='#1a1030',
                   edgecolor=GOLD, lw=1.8))

components = [
    (1.3,  PURPLE, 'cosine_similarity',
     'Primary signal\nAngle between TF-IDF vectors\nRange: 0 → 1'),
    (4.2,  GREEN,  'genre_jaccard × 0.15',
     'Genre overlap bonus\n|genres_A ∩ genres_B| / |genres_A ∪ genres_B|\nUses expanded-genres field'),
    (7.2,  GOLD,   'norm_rating × 0.10',
     'Rating tie-breaker\nIMDB rating normalised 0→1\nFavours higher-rated films'),
    (9.3,  WHITE,  'Dedup',
     'Same title never\nappears twice\nin results'),
]

for x, col, title, desc in components:
    box = FancyBboxPatch((x - 1.1, 0.05), 2.2, 0.52,
                         boxstyle='round,pad=0.06',
                         facecolor='#13131f', edgecolor=col, linewidth=1.3)
    ax5.add_patch(box)
    ax5.text(x, 0.49, title, ha='center', fontsize=8.5,
             fontweight='bold', color=col)
    ax5.text(x, 0.27, desc,  ha='center', fontsize=7.8,
             color=WHITE, linespacing=1.55)

for i in range(len(components) - 1):
    x0 = components[i][0] + 1.1
    x1 = components[i+1][0] - 1.1
    ax5.text((x0+x1)/2, 0.30, '+', ha='center',
             fontsize=18, color=MUTED, fontweight='bold')

plt.savefig('screenshots/cosine_similarity_explained.png',
            dpi=160, bbox_inches='tight', facecolor=FIG_BG)
print("Saved: screenshots/cosine_similarity_explained.png")
