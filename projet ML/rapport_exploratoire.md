# Exploration des données

> Bilan descriptif du corpus préparé. Une distribution équilibrée ne démontre ni représentativité ni validité des annotations.

## Vue d'ensemble

- Observations : **49,055**; textes distincts : **49,055**.
- Valeurs manquantes : **0**.
- Longueur : min 32, médiane 57, moyenne 56.84, max 81 caractères.

## Répartition par thème

| Thème | Nombre | Part |
|---|---:|---:|
| economy | 8,238 | 16.8% |
| health | 8,092 | 16.5% |
| politics | 8,245 | 16.8% |
| religion | 8,165 | 16.6% |
| sport | 8,223 | 16.8% |
| technology | 8,092 | 16.5% |

## Répartition par émotion

| Émotion | Nombre | Part |
|---|---:|---:|
| anger | 9,821 | 20.0% |
| hope | 9,811 | 20.0% |
| joy | 9,807 | 20.0% |
| neutral | 9,822 | 20.0% |
| sadness | 9,794 | 20.0% |

## Contrôles et interprétation

Le tableau détaillé thème × émotion est disponible dans `donnees/croisement_theme_emotion.csv`. Les effectifs proches dans les 30 cellules sont inhabituels pour des conversations spontanées et peuvent signaler une construction ou un équilibrage du corpus. La répartition ne doit donc pas être interprétée comme la fréquence des émotions dans la population.

Contrôles à réaliser avant modélisation : vérifier la provenance ligne par ligne; auditer manuellement un échantillon stratifié; vérifier les doublons quasi identiques; contrôler les dialectes, l'ironie et les annotations; conserver les sources et dates; puis séparer les partitions par source/auteur si ces identifiants deviennent disponibles.

## Reproduction

Depuis ce dossier : `python analyse_exploratoire.py`.
