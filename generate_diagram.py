"""
Generates screenshots/cosine_similarity_explained.png
Run: python generate_diagram.py
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

plt.rcParams['font.family'] = 'DejaVu Sans'

FIG_BG = '#0f0f1a'
WHITE  = '#f0eeff'
MUTED  = '#7a7a9a'
PURPLE = '#9b7ff0'
GREEN  = '#5dd4a0'
GOLD   = '#f0c040'
DARK   = '#1a1a2e'
CARD   = '#16162a'

fig, ax = plt.subplots(figsize=(16, 9), facecolor=FIG_BG)
ax.set_facecolor(FIG_BG)
ax.set_xlim(0, 16)
ax.set_ylim(0, 9)
ax.axis('off')

# ── Title ─────────────────────────────────────────────────────────────────────
ax.text(8, 8.5, 'How CineMatch Recommends Movies',
        ha='center', va='center', fontsize=22, fontweight='bold', color=WHITE)
ax.text(8, 8.05, 'TF-IDF  +  Cosine Similarity  +  Hybrid Scoring',
        ha='center', va='center', fontsize=12, color=MUTED)

# ── Step definitions ──────────────────────────────────────────────────────────
steps = [
    (1.3,  PURPLE, '1', 'Input',
     'Movie Title\nor Description',
     '"The Dark Knight"'),

    (4.0,  '#5b8dee', '2', 'Preprocess',
     'Clean the text',
     'lowercase  remove punctuation\nstopwords  lemmatize'),

    (6.9,  PURPLE, '3', 'TF-IDF\nVectorize',
     'Text  ->  Numbers',
     'Each movie becomes\na vector of 10K values'),

    (9.8,  GREEN,  '4', 'Cosine\nSimilarity',
     'Measure angle\nbetween vectors',
     'cos(A,B) = A·B / (||A|| x ||B||)\n0 = different   1 = identical'),

    (12.7, GOLD,   '5', 'Hybrid\nScore',
     'Combine signals',
     'TF-IDF sim  +  genre overlap\n+ rating bonus'),

    (15.2, '#f08080', '6', 'Top-N\nResults',
     'Return best matches',
     'Ranked list of\nsimilar movies'),
]

BOX_W, BOX_H = 2.3, 3.8
BOX_Y = 2.0

for x, color, num, title, subtitle, detail in steps:
    # card
    box = FancyBboxPatch((x - BOX_W/2, BOX_Y), BOX_W, BOX_H,
                         boxstyle='round,pad=0.15',
                         facecolor=CARD, edgecolor=color,
                         linewidth=2.2, zorder=2)
    ax.add_patch(box)

    # coloured top bar
    bar = FancyBboxPatch((x - BOX_W/2, BOX_Y + BOX_H - 0.55), BOX_W, 0.55,
                         boxstyle='round,pad=0.0',
                         facecolor=color, edgecolor='none', zorder=3)
    ax.add_patch(bar)

    # step number in bar
    ax.text(x, BOX_Y + BOX_H - 0.27, f'Step {num}',
            ha='center', va='center', fontsize=9,
            fontweight='bold', color='#0f0f1a', zorder=4)

    # title
    ax.text(x, BOX_Y + BOX_H - 1.05, title,
            ha='center', va='center', fontsize=12,
            fontweight='bold', color=color, zorder=4,
            linespacing=1.3)

    # subtitle
    ax.text(x, BOX_Y + 1.85, subtitle,
            ha='center', va='center', fontsize=9,
            color=MUTED, zorder=4, linespacing=1.4)

    # divider
    ax.plot([x - BOX_W/2 + 0.2, x + BOX_W/2 - 0.2],
            [BOX_Y + 1.55, BOX_Y + 1.55],
            color=color, lw=0.8, alpha=0.4, zorder=4)

    # detail
    ax.text(x, BOX_Y + 0.8, detail,
            ha='center', va='center', fontsize=8,
            color=WHITE, zorder=4, linespacing=1.55)

# ── Arrows between cards ──────────────────────────────────────────────────────
for i in range(len(steps) - 1):
    x0 = steps[i][0]   + BOX_W/2
    x1 = steps[i+1][0] - BOX_W/2
    xm = (x0 + x1) / 2
    ym = BOX_Y + BOX_H / 2

    ax.annotate('',
                xy=(x1, ym), xytext=(x0, ym),
                arrowprops=dict(
                    arrowstyle='->', color=MUTED,
                    lw=2, mutation_scale=18),
                zorder=5)

# ── Formula highlight at bottom ───────────────────────────────────────────────
formula_box = FancyBboxPatch((1.5, 0.3), 13, 1.3,
                              boxstyle='round,pad=0.15',
                              facecolor='#1a1030', edgecolor=PURPLE,
                              linewidth=1.5, zorder=2)
ax.add_patch(formula_box)

ax.text(8, 1.25, 'Final Score Formula',
        ha='center', va='center', fontsize=10,
        fontweight='bold', color=PURPLE, zorder=3)

parts = [
    (3.2,  PURPLE, 'cosine_similarity'),
    (5.05, MUTED,  '+'),
    (6.7,  GREEN,  'genre_jaccard x 0.15'),
    (8.55, MUTED,  '+'),
    (10.2, GOLD,   'norm_rating x 0.10'),
    (12.0, MUTED,  '-->'),
    (13.6, '#f08080', 'Ranked Results'),
]
for x, col, txt in parts:
    ax.text(x, 0.72, txt,
            ha='center', va='center', fontsize=10.5,
            fontweight='bold', color=col, zorder=3)

plt.tight_layout(pad=0)
plt.savefig('screenshots/cosine_similarity_explained.png',
            dpi=160, bbox_inches='tight', facecolor=FIG_BG)
print("Saved: screenshots/cosine_similarity_explained.png")
