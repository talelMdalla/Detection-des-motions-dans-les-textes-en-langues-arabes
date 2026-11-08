from pathlib import Path
from urllib.parse import urlparse

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

PROJECT_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = PROJECT_DIR / "donnees"
DATASET_FILE = OUTPUT_DIR / "dataset_nettoye.csv"
MANIFEST_FILE = OUTPUT_DIR / "dataset_sources.csv"
PLOTS_DIR = OUTPUT_DIR / "plots"
PLOTS_DIR.mkdir(parents=True, exist_ok=True)

EMOTION_ORDER = ["joy", "hope", "neutral", "sadness", "anger"]
EMOTION_COLORS = {
    "joy": "#f2b134",
    "hope": "#4caf7d",
    "neutral": "#9aa5b1",
    "sadness": "#4a7fc1",
    "anger": "#d9534f",
}

df = pd.read_csv(DATASET_FILE, encoding="utf-8-sig")
print("Rows:", len(df))

# Extra column: text length in words
df["n_words"] = df["text"].astype(str).str.split().str.len()


def save(fig, name):
    fig.tight_layout()
    fig.savefig(PLOTS_DIR / name, dpi=150)
    print("Saved:", PLOTS_DIR / name)


# ---------------------------------------------------------------
# 1. Emotion distribution (class balance)
# ---------------------------------------------------------------
counts = df["emotion"].value_counts().reindex(EMOTION_ORDER).dropna()
fig, ax = plt.subplots(figsize=(7, 4.5))
bars = ax.bar(
    counts.index, counts.values,
    color=[EMOTION_COLORS[e] for e in counts.index],
)
ax.bar_label(bars, padding=2)
ax.set_title("Emotion distribution")
ax.set_ylabel("Number of texts")
save(fig, "1_emotion_distribution.png")

# ---------------------------------------------------------------
# 2. Topic distribution
# ---------------------------------------------------------------
topic_counts = df["topic"].value_counts()
fig, ax = plt.subplots(figsize=(7, 4.5))
bars = ax.barh(topic_counts.index[::-1], topic_counts.values[::-1], color="#5b6f8a")
ax.bar_label(bars, padding=2)
ax.set_title("Topic distribution")
ax.set_xlabel("Number of texts")
save(fig, "2_topic_distribution.png")

# ---------------------------------------------------------------
# 3. Topic x emotion heatmap
# ---------------------------------------------------------------
table = pd.crosstab(df["topic"], df["emotion"])
table = table.reindex(columns=[e for e in EMOTION_ORDER if e in table.columns])
fig, ax = plt.subplots(figsize=(8, 5))
im = ax.imshow(table.values, cmap="Blues")
ax.set_xticks(range(table.shape[1]), labels=table.columns)
ax.set_yticks(range(table.shape[0]), labels=table.index)
for i in range(table.shape[0]):
    for j in range(table.shape[1]):
        value = table.values[i, j]
        color = "white" if value > table.values.max() * 0.6 else "black"
        ax.text(j, i, value, ha="center", va="center", color=color)
ax.set_title("Texts per topic and emotion")
fig.colorbar(im, ax=ax, label="Number of texts")
save(fig, "3_topic_emotion_heatmap.png")

# ---------------------------------------------------------------
# 4. Emotion share within each topic (100% stacked bars)
# ---------------------------------------------------------------
share = table.div(table.sum(axis=1), axis=0) * 100
fig, ax = plt.subplots(figsize=(8, 5))
left = np.zeros(len(share))
for emotion in share.columns:
    ax.barh(share.index, share[emotion], left=left,
            label=emotion, color=EMOTION_COLORS[emotion])
    left += share[emotion].values
ax.set_xlim(0, 100)
ax.set_xlabel("% of texts in the topic")
ax.set_title("Emotion mix by topic")
ax.legend(ncol=len(share.columns), loc="upper center",
          bbox_to_anchor=(0.5, -0.12), frameon=False)
save(fig, "4_emotion_share_by_topic.png")

# ---------------------------------------------------------------
# 5. Text length (words) by emotion
# ---------------------------------------------------------------
emotions_present = [e for e in EMOTION_ORDER if e in df["emotion"].unique()]
data = [df.loc[df["emotion"] == e, "n_words"] for e in emotions_present]
fig, ax = plt.subplots(figsize=(8, 4.5))
box = ax.boxplot(data, tick_labels=emotions_present, patch_artist=True)
for patch, emotion in zip(box["boxes"], emotions_present):
    patch.set_facecolor(EMOTION_COLORS[emotion])
ax.set_title("Text length by emotion")
ax.set_ylabel("Number of words")
save(fig, "5_text_length_by_emotion.png")

# ---------------------------------------------------------------
# 6. Text length histogram
# ---------------------------------------------------------------
fig, ax = plt.subplots(figsize=(7, 4.5))
ax.hist(df["n_words"], bins=20, color="#5b6f8a", edgecolor="white")
ax.axvline(df["n_words"].median(), color="#d9534f", linestyle="--",
           label=f"Median: {df['n_words'].median():.0f} words")
ax.set_title("Distribution of text length")
ax.set_xlabel("Number of words")
ax.set_ylabel("Number of texts")
ax.legend()
save(fig, "6_text_length_histogram.png")

# ---------------------------------------------------------------
# 7. Rows per source website (detect source bias)
# ---------------------------------------------------------------
if MANIFEST_FILE.exists():
    manifest = pd.read_csv(MANIFEST_FILE, encoding="utf-8-sig")
    manifest["domain"] = manifest["source_url"].apply(
        lambda u: urlparse(str(u)).netloc.replace("www.", "")
    )
    domain_counts = manifest["domain"].value_counts().head(10)
    fig, ax = plt.subplots(figsize=(8, 4.5))
    bars = ax.barh(domain_counts.index[::-1], domain_counts.values[::-1],
                   color="#8a6f5b")
    ax.bar_label(bars, padding=2)
    ax.set_title("Top sources (number of accepted texts)")
    ax.set_xlabel("Number of texts")
    save(fig, "7_texts_per_source.png")

# ---------------------------------------------------------------
# Summary printed in the terminal
# ---------------------------------------------------------------
print("\nEmotion percentages:")
print((df["emotion"].value_counts(normalize=True) * 100).round(1))

plt.show()