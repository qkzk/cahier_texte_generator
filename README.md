---
title: "Générateur de Cahier de texte"
author: "qkzk"
version: "1.1"
date: "2019/08/02"
---

Génère un cahier de texte pour être hébergé sur Github

Exécutez le script directement avec ou sans année en argument.
Il est préférable de modifier deux variables dans les sources :

* les dates des périodes scolaires
* les contenus de chaque journée
* l'url de votre repo

J'imagine que si vous lisez ceci, vous êtes capable de le faire...

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
* Mettre tous les paramètre dans un fichier de config format yaml qu'on importe
* Modifier l'url du repo pour qu'elle soit facilement éditable


## DONE
1. générer le calendrier
2. probleme des périodes de chaque année...

1. générer les dossiers de parents :
2. générer les fichiers .md de chaque semaine de la période
    1. découper en dates proprement chaque période :
    2. quelle semaine dans quelle période ? :
    3. créer les fichiers .md :
3. peupler les fichiers .md
    1. ajouter le titre : semaine bidule dates machin
    2. ajouter les découpages par jour
4. **Version 1.1 :**
   intégrer un calendar avec lien cliquables vers le bon fichier
    utilise htmlcalendar
    sources :
    https://www.guru99.com/calendar-in-python.html
    https://docs.python.org/fr/3/library/calendar.html
    https://stackabuse.com/introduction-to-the-python-calendar-module/
    https://www.w3resource.com/python/module/calendar/html-calendar-formatmonth.php

## CORRECTIFS
* corriger bug dates : lundi  29 avril 2020 : FAUX c'est le jour de l'année
  d'avant.

  Les dates de 2020 doivent toutes êtres fausses de ce fait...

  Correction : Oubli de changer une date en dur
