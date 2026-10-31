"""Nettoyage reproductible du jeu de données d'émotions arabes."""

from __future__ import annotations

import json
import re
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parent
OUTPUT_DIR = ROOT.parent / "AI_agent" / "output"
AGENT_SOURCE = OUTPUT_DIR / "dataset.csv"
ARCHIVE_SOURCE = OUTPUT_DIR / "arabic_topic_emotion_dataset_50000.csv"
SOURCE = AGENT_SOURCE if AGENT_SOURCE.exists() else ARCHIVE_SOURCE
DATA_DIR = ROOT / "donnees"
SEED = 42
VALID_TOPICS = {"sport", "economy", "politics", "religion", "technology", "health"}
VALID_EMOTIONS = {"joy", "anger", "sadness", "hope", "neutral"}
EXPECTED_COLUMNS = ["id", "text", "topic", "emotion"]


def clean_text(value: object) -> str:
    """Normalise les espaces sans supprimer les caractères arabes ni les emojis."""
    if pd.isna(value):
        return ""
    return re.sub(r"\s+", " ", str(value)).strip()


def split_stratified(frame: pd.DataFrame) -> tuple[pd.DataFrame, ...]:
    """Répartit chaque couple thème/émotion en 70 % / 15 % / 15 %."""
    train_parts, validation_parts, test_parts = [], [], []
    rng = __import__("numpy").random.default_rng(SEED)
    strata = frame.groupby(["topic", "emotion"], sort=True, dropna=False)
    for _, group in strata:
        indices = group.index.to_numpy().copy()
        rng.shuffle(indices)
        n = len(indices)
        n_train = int(n * 0.70)
        n_validation = int(n * 0.15)
        train_parts.append(frame.loc[indices[:n_train]])
        validation_parts.append(frame.loc[indices[n_train:n_train + n_validation]])
        test_parts.append(frame.loc[indices[n_train + n_validation:]])

    def combine(parts: list[pd.DataFrame]) -> pd.DataFrame:
        return pd.concat(parts).sample(frac=1, random_state=SEED).reset_index(drop=True)

    return combine(train_parts), combine(validation_parts), combine(test_parts)


def main() -> None:
    if not SOURCE.exists():
        raise FileNotFoundError(f"CSV source introuvable : {SOURCE}")
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    original = pd.read_csv(SOURCE, encoding="utf-8-sig")
    missing_columns = sorted(set(EXPECTED_COLUMNS) - set(original.columns))
    if missing_columns:
        raise ValueError(f"Colonnes manquantes : {missing_columns}")

    data = original[EXPECTED_COLUMNS].copy()
    initial_rows = len(data)
    missing_values = int(data.isna().sum().sum())
    data["text"] = data["text"].map(clean_text)
    data["topic"] = data["topic"].fillna("").astype(str).str.strip().str.lower()
    data["emotion"] = data["emotion"].fillna("").astype(str).str.strip().str.lower()

    empty_text_rows = int(data["text"].eq("").sum())
    data = data.loc[data["text"].ne("")].copy()
    invalid_label_rows = int((~data["topic"].isin(VALID_TOPICS) | ~data["emotion"].isin(VALID_EMOTIONS)).sum())
    data = data.loc[data["topic"].isin(VALID_TOPICS) & data["emotion"].isin(VALID_EMOTIONS)].copy()

    # Les répétitions sont détectées sans tenir compte des espaces superflus et de la casse.
    data["_text_key"] = data["text"].str.casefold()
    duplicate_text_rows = int(data.duplicated("_text_key").sum())
    data = data.drop_duplicates("_text_key", keep="first").drop(columns="_text_key")
    data = data.reset_index(drop=True)
    if data.empty:
        raise ValueError("Aucune ligne valide après nettoyage; vérifier le CSV source et les étiquettes.")
    data["id"] = range(1, len(data) + 1)
    data = data[EXPECTED_COLUMNS]

    train, validation, test = split_stratified(data)
    data.to_csv(DATA_DIR / "dataset_nettoye.csv", index=False, encoding="utf-8-sig")
    train.to_csv(DATA_DIR / "train.csv", index=False, encoding="utf-8-sig")
    validation.to_csv(DATA_DIR / "validation.csv", index=False, encoding="utf-8-sig")
    test.to_csv(DATA_DIR / "test.csv", index=False, encoding="utf-8-sig")

    stats = {
        "source": str(SOURCE.relative_to(ROOT.parent)),
        "seed": SEED,
        "rows_initiales": initial_rows,
        "valeurs_manquantes_initiales": missing_values,
        "textes_vides_supprimes": empty_text_rows,
        "lignes_a_labels_invalides_supprimees": invalid_label_rows,
        "textes_dupliques_supprimes": duplicate_text_rows,
        "lignes_finales": len(data),
        "repartition": {"train": len(train), "validation": len(validation), "test": len(test)},
        "themes": data["topic"].value_counts().sort_index().to_dict(),
        "emotions": data["emotion"].value_counts().sort_index().to_dict(),
        "longueur_caracteres": {
            "minimum": int(data["text"].str.len().min()),
            "mediane": float(data["text"].str.len().median()),
            "moyenne": round(float(data["text"].str.len().mean()), 2),
            "maximum": int(data["text"].str.len().max()),
        },
        "distribution_theme_emotion": {
            f"{topic}|{emotion}": int(count)
            for (topic, emotion), count in data.groupby(["topic", "emotion"]).size().items()
        },
    }
    (DATA_DIR / "statistiques.json").write_text(json.dumps(stats, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(stats, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
