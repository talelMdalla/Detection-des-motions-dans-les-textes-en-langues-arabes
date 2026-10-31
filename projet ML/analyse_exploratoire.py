"""Génère un bilan descriptif reproductible du corpus préparé."""
from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "donnees" / "dataset_nettoye.csv"
OUT = ROOT / "donnees"


def main() -> None:
    frame = pd.read_csv(DATA, encoding="utf-8-sig")
    frame["longueur"] = frame["text"].fillna("").astype(str).str.len()
    cross = pd.crosstab(frame["topic"], frame["emotion"], margins=True)
    cross.to_csv(OUT / "croisement_theme_emotion.csv", encoding="utf-8-sig")
    summary = {
        "fichier": DATA.name,
        "lignes": int(len(frame)),
        "valeurs_manquantes_par_colonne": frame.drop(columns="longueur").isna().sum().astype(int).to_dict(),
        "identifiants_uniques": int(frame["id"].nunique()),
        "textes_uniques": int(frame["text"].nunique()),
        "longueur_caracteres": {
            "min": int(frame["longueur"].min()),
            "q1": float(frame["longueur"].quantile(.25)),
            "mediane": float(frame["longueur"].median()),
            "moyenne": round(float(frame["longueur"].mean()), 2),
            "q3": float(frame["longueur"].quantile(.75)),
            "max": int(frame["longueur"].max()),
        },
        "themes": frame["topic"].value_counts().sort_index().astype(int).to_dict(),
        "emotions": frame["emotion"].value_counts().sort_index().astype(int).to_dict(),
        "croisement_theme_emotion": {
            str(topic): {str(emotion): int(n) for emotion, n in row.items()}
            for topic, row in pd.crosstab(frame["topic"], frame["emotion"]).iterrows()
        },
    }
    (OUT / "exploration.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    lines = [
        "# Exploration des données", "",
        "> Bilan descriptif du corpus préparé. Une distribution équilibrée ne démontre ni représentativité ni validité des annotations.", "",
        "## Vue d'ensemble", "",
        f"- Observations : **{summary['lignes']:,}**; textes distincts : **{summary['textes_uniques']:,}**.",
        f"- Valeurs manquantes : **{sum(summary['valeurs_manquantes_par_colonne'].values())}**.",
        f"- Longueur : min {summary['longueur_caracteres']['min']}, médiane {summary['longueur_caracteres']['mediane']:.0f}, moyenne {summary['longueur_caracteres']['moyenne']}, max {summary['longueur_caracteres']['max']} caractères.",
        "", "## Répartition par thème", "", "| Thème | Nombre | Part |", "|---|---:|---:|",
    ]
    lines += [f"| {k} | {v:,} | {v / len(frame):.1%} |" for k, v in summary["themes"].items()]
    lines += ["", "## Répartition par émotion", "", "| Émotion | Nombre | Part |", "|---|---:|---:|"]
    lines += [f"| {k} | {v:,} | {v / len(frame):.1%} |" for k, v in summary["emotions"].items()]
    lines += [
        "", "## Contrôles et interprétation", "",
        "Le tableau détaillé thème × émotion est disponible dans `donnees/croisement_theme_emotion.csv`. Les effectifs proches dans les 30 cellules sont inhabituels pour des conversations spontanées et peuvent signaler une construction ou un équilibrage du corpus. La répartition ne doit donc pas être interprétée comme la fréquence des émotions dans la population.",
        "", "Contrôles à réaliser avant modélisation : vérifier la provenance ligne par ligne; auditer manuellement un échantillon stratifié; vérifier les doublons quasi identiques; contrôler les dialectes, l'ironie et les annotations; conserver les sources et dates; puis séparer les partitions par source/auteur si ces identifiants deviennent disponibles.",
        "", "## Reproduction", "", "Depuis ce dossier : `python analyse_exploratoire.py`.", "",
    ]
    (ROOT / "rapport_exploratoire.md").write_text("\n".join(lines), encoding="utf-8")
    print(f"Bilan écrit dans {ROOT / 'rapport_exploratoire.md'}")


if __name__ == "__main__":
    main()
