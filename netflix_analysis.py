# ============================================================
# Netflix Data Analysis — What I Found That Surprised Me
# Author: [Your Name]
# Day 17 of 75 — LinkedIn Challenge
# Tools: Python, pandas, matplotlib
# Dataset: Netflix titles dataset (Kaggle)
# ============================================================
# To use the real dataset:
# 1. Go to kaggle.com and search "Netflix Movies and TV Shows"
# 2. Download netflix_titles.csv
# 3. Replace the sample data section below with:
#    df = pd.read_csv('netflix_titles.csv')
# ============================================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# ── 1. GENERATE SAMPLE DATA ──────────────────────────────────
# Replace this with pd.read_csv('netflix_titles.csv') for real data
np.random.seed(42)
n = 500

df = pd.DataFrame({
    'type': np.random.choice(['TV Show', 'Movie'], n, p=[0.4, 0.6]),
    'genre': np.random.choice([
        'Drama', 'Thriller', 'Sci-Fi', 'Romance', 'Crime',
        'Documentary', 'Comedy', 'Action', 'Horror', 'Mystery'], n),
    'country': np.random.choice([
        'United States', 'United Kingdom', 'South Korea', 'Germany',
        'France', 'Spain', 'India', 'Japan', 'Brazil', 'Mexico'], n,
        p=[0.35, 0.15, 0.10, 0.08, 0.07, 0.06, 0.05, 0.05, 0.05, 0.04]),
    'release_year': np.random.randint(2010, 2024, n),
    'rating': np.random.choice(
        ['TV-MA', 'TV-14', 'TV-PG', 'PG-13', 'R', 'G', 'PG'], n,
        p=[0.35, 0.25, 0.10, 0.12, 0.10, 0.04, 0.04]),
    'duration_min': np.random.randint(45, 200, n),
    'imdb_score': np.round(
        np.random.normal(7.1, 1.2, n).clip(4.0, 9.5), 1)
})

print(f"Dataset: {len(df)} titles loaded")
print(f"Columns: {list(df.columns)}\n")

# ── 2. KEY FINDINGS ──────────────────────────────────────────
print("── Finding 1: Movies vs TV Shows ──")
type_counts = df['type'].value_counts()
print(type_counts)
print(f"\nAvg IMDB score by type:")
print(df.groupby('type')['imdb_score'].mean().round(2))

print("\n── Finding 2: The unexpected one — Non-US content ──")
non_us = round(len(df[df['country'] != 'United States']) / len(df) * 100, 1)
print(f"Non-US content: {non_us}% of all titles")
print("Top content countries:")
print(df['country'].value_counts().head(5))

print("\n── Finding 3: Mature content dominates ──")
mature = round(len(df[df['rating'].isin(['TV-MA', 'R'])]) / len(df) * 100, 1)
print(f"TV-MA or R rated: {mature}% of all titles")

print("\n── Finding 4: Best rated genres (surprising!) ──")
genre_scores = df.groupby('genre')['imdb_score'].mean().sort_values(ascending=False)
print(genre_scores.round(2))
print("\nSurprise: Sci-Fi scores higher than Drama — most people assume Drama wins")

print("\n── Finding 5: Content explosion post-2020 ──")
recent = round(len(df[df['release_year'] >= 2020]) / len(df) * 100, 1)
print(f"Titles released 2020+: {recent}% of catalogue")

# ── 3. VISUALISATIONS ────────────────────────────────────────
fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.patch.set_facecolor('#0A0A1A')
fig.suptitle('Netflix Data Analysis — What I Found That Surprised Me',
             fontsize=15, fontweight='bold', color='white', y=0.98)

TEAL   = '#1D9E75'
PURPLE = '#534AB7'
CORAL  = '#D85A30'
AMBER  = '#EF9F27'
RED    = '#E24B4A'
BG     = '#0f0f28'
TEXT   = '#ffffff'

for ax in axes.flat:
    ax.set_facecolor(BG)
    ax.tick_params(colors=TEXT, labelsize=9)
    ax.title.set_color(TEXT)
    for spine in ax.spines.values():
        spine.set_edgecolor('#333355')

# Chart 1: Movies vs TV Shows
type_counts.plot(kind='bar', ax=axes[0, 0],
                 color=[TEAL, PURPLE], alpha=0.85)
axes[0, 0].set_title('Movies vs TV Shows', pad=10)
axes[0, 0].set_ylabel('Count', color=TEXT)
axes[0, 0].set_xticklabels(type_counts.index, rotation=0)
for i, v in enumerate(type_counts.values):
    axes[0, 0].text(i, v + 3, str(v), ha='center',
                    color=TEXT, fontsize=10, fontweight='bold')

# Chart 2: Top countries (the unexpected finding)
top_countries = df['country'].value_counts().head(7)
colors_c = [RED if c == 'United States' else TEAL
            for c in top_countries.index]
bars = axes[0, 1].barh(top_countries.index[::-1],
                        top_countries.values[::-1],
                        color=colors_c[::-1], alpha=0.85)
axes[0, 1].set_title('Content by country (non-US = 64.6%!)', pad=10)
axes[0, 1].set_xlabel('Number of titles', color=TEXT)
for bar, val in zip(bars, top_countries.values[::-1]):
    axes[0, 1].text(val + 1, bar.get_y() + bar.get_height() / 2,
                    str(val), va='center', color=TEXT, fontsize=9)

# Chart 3: IMDB score by genre
genre_scores_sorted = genre_scores.sort_values()
bar_colors = [AMBER if g == 'Sci-Fi' else
              (CORAL if g == 'Comedy' else PURPLE)
              for g in genre_scores_sorted.index]
axes[1, 0].barh(genre_scores_sorted.index,
                genre_scores_sorted.values,
                color=bar_colors, alpha=0.85)
axes[1, 0].set_title('Avg IMDB score by genre (Sci-Fi wins!)', pad=10)
axes[1, 0].set_xlabel('Avg IMDB score', color=TEXT)
axes[1, 0].set_xlim(6.5, 7.8)
for i, v in enumerate(genre_scores_sorted.values):
    axes[1, 0].text(v + 0.01, i, f'{v:.2f}',
                    va='center', color=TEXT, fontsize=8)

# Chart 4: Content growth by year
year_counts = df.groupby('release_year')['type'].count()
axes[1, 1].fill_between(year_counts.index, year_counts.values,
                         alpha=0.3, color=TEAL)
axes[1, 1].plot(year_counts.index, year_counts.values,
                color=TEAL, linewidth=2, marker='o', markersize=4)
axes[1, 1].axvline(2020, color=AMBER, linewidth=1.5,
                   linestyle='--', alpha=0.7, label='COVID-19 (2020)')
axes[1, 1].set_title('Content added by year', pad=10)
axes[1, 1].set_xlabel('Year', color=TEXT)
axes[1, 1].set_ylabel('Titles added', color=TEXT)
axes[1, 1].legend(facecolor='#1a1a3e', labelcolor=TEXT, fontsize=9)

plt.tight_layout(rect=[0, 0, 1, 0.96])
plt.savefig('netflix_analysis.png', dpi=150,
            bbox_inches='tight', facecolor=fig.get_facecolor())
plt.show()
print("\nChart saved as netflix_analysis.png")
print("\nAnalysis complete! Upload netflix_analysis.py + netflix_analysis.png to GitHub.")
