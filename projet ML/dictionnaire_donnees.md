# Dictionnaire des données

## Schéma CSV

| Champ | Type | Description | Usage |
|---|---|---|---|
| `id` | entier | Identifiant séquentiel régénéré après déduplication | Traçabilité seulement; exclure des variables du modèle |
| `text` | texte UTF-8 | Texte arabe court; espaces normalisés, emojis conservés | Entrée NLP après validation linguistique |
| `topic` | catégorie | Thème parmi sport, economy, politics, religion, technology, health | Variable de groupement pour l'analyse |
| `emotion` | catégorie | Étiquette parmi joy, anger, sadness, hope, neutral | Cible éventuelle d'un classifieur |

## Qualité observée

Source : 50 050 lignes; schéma attendu présent. Valeurs manquantes initiales : 0. Textes vides retirés : 0. Étiquettes hors vocabulaire retirées : 0. Textes répétés supprimés : 995. Corpus final : 49 055 lignes. Longueur : 32–81 caractères, médiane 57, moyenne 56,84. Les classes et thèmes sont presque équilibrés; cette régularité mérite un audit, elle n'est pas une preuve de représentativité.

## Vocabulaire des étiquettes

| Valeur | Interprétation |
|---|---|
| `joy` | joie / enthousiasme |
| `anger` | colère / frustration |
| `sadness` | tristesse / déception |
| `hope` | espoir / optimisme tourné vers l'avenir |
| `neutral` | absence d'émotion explicite ou texte descriptif |

Les étiquettes sont conservées en anglais pour rester compatibles avec les fichiers sources. Une annotation « neutral » peut masquer l'ironie, le sarcasme ou l'ambivalence; elle doit être contrôlée humainement.

