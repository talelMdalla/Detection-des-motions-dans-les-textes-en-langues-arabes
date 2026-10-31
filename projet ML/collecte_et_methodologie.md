# Étape 1–2 — cadrage métier et collecte

## 1. Compréhension métier (Business understanding)

### Contexte et problème

Les équipes qui suivent les conversations publiques ont besoin de comprendre les émotions exprimées autour de sujets différents. Lire manuellement des milliers de courts textes arabes est lent et difficile à comparer. Ce projet prépare un corpus pour étudier la relation entre **thème** et **émotion**, puis, dans une phase ultérieure, entraîner un classifieur de textes.

### Question et objectifs

Question exploratoire : **comment les émotions annotées varient-elles selon le thème dans ce corpus ?** Les objectifs sont de (1) décrire le corpus et sa qualité, (2) préparer des partitions reproductibles, et (3) établir une base documentée pour une validation humaine et une expérimentation NLP. Le livrable actuel est une préparation et une exploration descriptive; il ne prétend pas mesurer l'opinion de la population ni fournir un modèle entraîné.

### Pourquoi l'apprentissage automatique et la fouille de données

La fouille de données permet de résumer des volumes de textes et de comparer des groupes. Le NLP peut ensuite automatiser une première classification émotionnelle, sous réserve d'annotations fiables, d'une validation humaine et d'une évaluation adaptée à l'arabe. Les résultats automatiques ne remplacent pas une enquête représentative.

### Périmètre et indicateurs de réussite

Le fichier existant contient six thèmes (`sport`, `economy`, `politics`, `religion`, `technology`, `health`) et cinq classes (`joy`, `anger`, `sadness`, `hope`, `neutral`). Le succès de cette phase se mesure par des fichiers lisibles, un schéma stable, des règles explicites, des statistiques vérifiables et un découpage sans recouvrement. La provenance et la validité des annotations restent des conditions préalables à toute conclusion substantielle.

### Plan de travail

1. Inventorier le CSV et documenter son schéma et sa provenance disponible.
2. Explorer les valeurs, distributions, longueurs et doublons.
3. Nettoyer sans détruire les marqueurs linguistiques utiles, consigner chaque suppression.
4. Exporter le corpus et les partitions train/validation/test.
5. Faire auditer manuellement un échantillon et confirmer la provenance avant modélisation.

## 2. Collecte des données (Data collection)

### Sources et méthode constatées

Le fichier analysé est `../AI_agent/output/arabic_topic_emotion_dataset_50000.csv` (50 050 lignes). Son ancienne version ne conserve pas d'URL, de date ou d'identifiant de page : son origine ligne par ligne reste donc invérifiable. L'agent `../AI_agent/agent.py` documente les nouvelles collectes dans un manifeste.

Le prompt a été aligné sur le périmètre à six thèmes du corpus. Une collecte distincte centrée uniquement sur l'économie tunisienne doit utiliser une autre configuration et un corpus séparé.

### Outils et protocole cible

L'agent utilise Python et l'API Tavily pour chercher jusqu'à 10 pages publiques, extrait des segments d'au moins 25 caractères et vérifie la présence de texte arabe. L'API Gemini filtre les segments selon le sujet et propose les étiquettes de thème et d'émotion. Le CSV d'analyse conserve exactement `id,text,topic,emotion`; un fichier compagnon `../AI_agent/output/dataset_sources.csv` associe chaque ID à l'URL/titre, à la requête, à l'heure UTC, au SHA-256 du texte, au modèle et à la méthode d'annotation. `../AI_agent/output/collecte_run.json` garde le résumé d'exécution.

La méthode ne garantit pas une collecte représentative : recherche et couverture des pages dépendent du moteur, de la période et de la langue. Aucun scraper ne doit contourner les restrictions d'accès. Respecter les conditions d'utilisation, les droits d'auteur et la minimisation des données personnelles; anonymiser les identifiants personnels. L'annotation par LLM est une proposition à auditer avec des humains.

### Biais et limites de collecte

Une recherche Web limitée à quelques pages est biaisée par le référencement, la plateforme, la langue, la période et la disponibilité des pages. Les contenus publics ne représentent pas l'ensemble des Tunisiens. Les résultats d'un LLM sont des annotations assistées, pas des étiquettes de vérité; prévoir un double codage humain, un guide d'annotation et la mesure de l'accord inter-annotateurs.

