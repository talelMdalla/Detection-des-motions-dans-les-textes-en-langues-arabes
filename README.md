# Détection des émotions dans les textes en langues arabes

Projet de fouille de données et de traitement automatique du langage naturel (NLP). Il comprend un agent IA qui recherche des textes arabes sur le Web, un pipeline d'exploration et de préparation, ainsi qu'un rapport détaillé.

## Contenu du dépôt

- `AI_agent/agent.py` : collecte via Tavily et annotation assistée par Gemini.
- `AI_agent/prompt.txt` : requête et critères de collecte.
- `AI_agent/output/` : corpus de référence fourni.
- `projet ML/` : scripts de nettoyage et d'exploration, données préparées, statistiques et documentation.
- `rapport_projet.tex` et `rapport_projet.pdf` : rapport et schémas du projet.
- `presentation_projet.tex` et `presentation_projet.pdf` : présentation Beamer de 10 diapositives.

## Démarrage rapide

Installer les dépendances Python :

```powershell
python -m pip install pandas numpy python-dotenv tavily-python google-genai
```

Pour lancer la collecte, créer `AI_agent/.env` avec les variables `TAVILY_API_KEY` et `GEMINI_API_KEY`, puis exécuter depuis la racine :

```powershell
python AI_agent/agent.py
python "projet ML/nettoyage.py"
python "projet ML/analyse_exploratoire.py"
```

L'agent écrit le jeu de données, son manifeste de sources et un résumé d'exécution dans `AI_agent/output/`. Le nettoyage privilégie le CSV créé par l'agent lorsqu'il est disponible; sinon il utilise le corpus de référence inclus.

## Résultats préparés

Le corpus de référence compte 50 050 lignes avant nettoyage et 49 055 après suppression de 995 textes répétés. Il couvre six thèmes et cinq émotions; les partitions train, validation et test sont créées avec une graine fixe.

Pour la présentation orale, consulter la [présentation PDF](presentation_projet.pdf) et son [source LaTeX Beamer](presentation_projet.tex). Pour les détails de la démarche, voir le [rapport PDF](rapport_projet.pdf) et son [source LaTeX](rapport_projet.tex). Les instructions détaillées sont dans [`projet ML/README.md`](projet%20ML/README.md).
