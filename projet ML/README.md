# Analyse des émotions dans des textes arabes

## Résumé

Le projet réunit un agent IA de collecte et d'annotation initiale, des scripts reproductibles d'exploration et de préparation, ainsi qu'un corpus de textes arabes classés par thème et émotion. Il suit quatre phases de la démarche CRISP-DM : **compréhension métier**, **collecte**, **compréhension des données** et **préparation**. Le corpus analysé comprend 49 055 lignes après nettoyage, six thèmes et cinq émotions, réparties en trois partitions.

## Parcours du projet

1. Lire [`collecte_et_methodologie.md`](collecte_et_methodologie.md) : problème, objectifs, plan, sources et protocole.
2. Consulter [`dictionnaire_donnees.md`](dictionnaire_donnees.md) : schéma, vocabulaire et contrôles.
3. Lire le rapport illustré [`rapport_projet.tex`](../rapport_projet.tex); son PDF est [`rapport_projet.pdf`](../rapport_projet.pdf).
4. Pour lancer l'agent, configurer les clés API dans `AI_agent/.env`, puis exécuter `python AI_agent/agent.py` depuis la racine.
5. Relancer la préparation : `python "projet ML/nettoyage.py"`.
6. Regénérer l'exploration : `python "projet ML/analyse_exploratoire.py"`.

## Étapes réalisées

### 1. Compréhension métier

Question exploratoire : comment la distribution des émotions annotées varie-t-elle selon le thème ? L'apprentissage automatique est un prolongement possible pour automatiser une classification, mais cette livraison ne contient pas de modèle entraîné et ne mesure pas la représentativité du corpus.

### 2. Collecte

L'agent `AI_agent/agent.py` utilise Tavily pour rechercher des pages Web publiques et Gemini pour filtrer et annoter les segments pertinents. Il exporte `AI_agent/output/dataset.csv`, un manifeste `AI_agent/output/dataset_sources.csv` et le résumé `AI_agent/output/collecte_run.json`. Le jeu historique `AI_agent/output/arabic_topic_emotion_dataset_50000.csv` sert de corpus de référence présent; le script de préparation sélectionne automatiquement la sortie de l'agent lorsqu'elle existe.

### 3. Compréhension des données

50 050 lignes initiales, aucune valeur manquante observée, six thèmes et cinq émotions, textes de 32 à 81 caractères (médiane 57). Le bilan détaillé est généré dans `rapport_exploratoire.md`; l'analyse croisée est disponible en CSV.

### 4. Préparation

Normalisation des espaces et des étiquettes, retrait des textes vides et labels inconnus (aucun observé), déduplication exacte insensible à la casse (995 textes retirés), conservation des caractères arabes et emojis, réidentification puis séparation stratifiée à 70/15/15 (graine 42). Voir `nettoyage.py` pour le code reproductible.

## Arborescence

```text
projet ML/
├── README.md
├── collecte_et_methodologie.md
├── dictionnaire_donnees.md
├── rapport_exploratoire.md
├── nettoyage.py
├── analyse_exploratoire.py
└── donnees/
    ├── dataset_nettoye.csv
    ├── train.csv
    ├── validation.csv
    ├── test.csv
    ├── statistiques.json
    ├── exploration.json
    └── croisement_theme_emotion.csv
```

## Installation et reproduction

Python 3.10+ avec `pandas`, `numpy`, `python-dotenv`, `tavily-python` et `google-genai` :

```powershell
python -m pip install pandas numpy python-dotenv tavily-python google-genai
python AI_agent/agent.py
python "projet ML/nettoyage.py"
python "projet ML/analyse_exploratoire.py"
```

Les exports CSV sont en UTF-8 avec BOM. Le schéma est `id,text,topic,emotion`. Pour un futur classifieur, utiliser `text` comme entrée et `emotion` comme cible, exclure `id`; `topic` sert aux analyses par thème. Éviter toute fuite entre partitions si des sources ou auteurs deviennent disponibles.

Le rapport LaTeX et son PDF sont à la racine du dépôt. Depuis la racine, le source se compile avec `xelatex rapport_projet.tex`.

## Prochaines étapes recommandées

1. Maintenir le sujet du prompt et le périmètre six thèmes du dataset alignés.
2. Établir la provenance et joindre URL/date/plateforme à chaque observation.
3. Auditer un échantillon stratifié avec deux annotateurs, documenter les désaccords et calculer leur accord.
4. Mesurer les quasi-doublons et les fuites de formulations entre partitions.
5. Après validation seulement, comparer un modèle de référence et un modèle arabe; rapporter F1 macro, matrice de confusion et résultats par thème/classe.
