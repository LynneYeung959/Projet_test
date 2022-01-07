# Projet_test

## Nos principes 

KISS : Keep It Simple Stupid
DRY : Don't Répertoire Yourself
YAGNI : You Aren't Gonna Need It

## Syntaxe commits

Écrire les commits en suivant le guide https://gitmoji.dev/ .
Commits en anglais. 

Exemple de commit : 
 - ":sparkles: server : implement send_msg"
 - ":recycle: client : refactor user login code"

## Code style

Suivre la [PEP8](https://www.python.org/dev/peps/pep-0008/)

Le principal :
 - Indentation avec 4 espaces (pas de tab)
 - Classes en CamelCase, variables et fonctions en snake_case
 - Utiliser des noms explicites (abréviations autorisées pour les cas d'usages connus)

Tout en anglais, même les commentaires.

## Arborescence

```
Projet_test
|_ client
|   |_ fichier1.py
|   |_ fichiers.py
|_ server
|   |_ fichier1.py
|   |_ fichier2.py
|_ .gitignore
|_ .pylintrc
|_ LICENSE.md
|_ README.md
```

Nom des scripts Python tout en minuscule.
Un fichier rempli une fonction précise (éviter les fichiers fourre tout)
