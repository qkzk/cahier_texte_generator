# Générateur de Cahier de texte

## Auteur : [qkzk](https://github.com/qkzk)

### Collaborateur : [Amaroke](https://github.com/Amaroke)

#### Première version le 2 février 2019, dernière mise à jour le 10 octobre 2022

---

Génère un cahier de texte pour être hébergé sur Github

## HOWTO

Pas de venv
Pas de librairie

Exécutez le script directement avec ou sans année en argument.

Juste exécuter le fichier :

~~~
$ python cahier_texte_generator.py
~~~

En passant une année en argument :

~~~
$ python cahier_texte_generator.py 2022
~~~

## Usage courant

On peut spécifier l'année scolaire de départ : 2019 pour 2019/2020
ainsi que la semaine à partir de laquelle on veut mettre à jour le calendrier
ainsi seuls les semaines après la semaine spécifiée seront modifiées.

Il est préférable de modifier deux variables dans les sources :

* les dates des périodes scolaires
* les contenus de chaque journée
* l'url de votre repo

J'imagine que si vous lisez ceci, vous êtes capable de le faire...

## Exemple de rendu

~~~
.
└── 2019
    ├── periode1
    |   ├── semaine_36.md
    |   ...
    │   └── semaine_41.md
    ...
    └── periode5
        ├── semaine_36.md
        ...
        └── semaine_41.md
~~~

semaine36.md
>
>  # Semaine 35 - du Lundi 26 août au Dimanche 01 septembre
>
>  ## Lundi 3 septembre
>  **8h-9h30** _salle 213_ : exos bidules
>  ## Mardi 4 septembre

## TODO

* Mettre tous les paramètres dans un fichier de config format yaml qu'on importe
* Modifier l'url du repo et le nom de l'auteur pour qu'elle soit facilement éditable
* Adapter copy_github.py pour qu'il soit utilisable par tous

## DONE

1. Générer le calendrier
2. Problème des périodes de chaque année...

3. Générer les dossiers de parents :
4. Générer les fichiers .md de chaque semaine de la période
    1. Découper en dates proprement chaque période
    2. Quelle semaine dans quelle période ?
    3. Créer les fichiers .md
5. Peupler les fichiers .md
    1. ajouter le titre : semaine bidule dates machin
    2. ajouter les découpages par jour
6. **Version 1.1 :**
   intégrer un calendar avec lien cliquable vers le bon fichier
   utilise htmlcalendar
   sources :
   https://www.guru99.com/calendar-in-python.html
   https://docs.python.org/fr/3/library/calendar.html
   https://stackabuse.com/introduction-to-the-python-calendar-module/
   https://www.w3resource.com/python/module/calendar/html-calendar-formatmonth.php
7. startweek : spécifier l'année de départ<br>
   TODO : utiliser automatiquement si l'année est entamée afin d'éviter toute
   bévue quand on copie les fichiers.
8. Copie du readme avec le calendrier vers le dossier github

## CORRECTIFS

Aucun problème detecté dans la version actuelle.
