#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
---
title: "Générateur de Cahier de texte"
author: "qkzk"
version: "1.0"
date: "2019/08/02"
---

Genere un cahier de texte pour être hébergé sur Github

Exécutez le script directement avec ou sans année en argument.
Il est préférable de modifier deux variables dans les sources :

    * les dates des périodes scolaires
    * les contenus de chaque journée

    J'imagine que si vous lisez ceci, vous êtes capable de le faire...


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


semaine36.md
>
>  # Semaine 35 - du Lundi 26 août au Dimanche 01 septembre
>
>  ## Lundi 3 septembre
>      **8h-9h30** _salle 213_ : exos bidules
>  ## Mardi 4 septembre

TODO
* intégrer un calendar avec lien cliquables vers le bon fichier
    pour intégration dans le site... plus difficile mais p-ê worth it
    utiliser htmlcalendar et htmlcalendarclass je sais pas quoi

    pas evident de rendre chaque jour cliquable vers son jour en question...
    faut p-ê du JS pour créer les liens :(

    https://www.guru99.com/calendar-in-python.html
    https://docs.python.org/fr/3/library/calendar.html
    https://stackabuse.com/introduction-to-the-python-calendar-module/
    https://www.w3resource.com/python/module/calendar/html-calendar-formatmonth.php

DONE
1. générer le calendrier
2. probleme des périodes de chaque année...

1. générer les dossiers de parents : DONE
2. générer les fichiers .md de chaque semaine de la période
    1. découper en dates proprement chaque période : DONE
    2. quelle semaine dans quelle période ? : DONE
    3. créer les fichiers .md : DONE
3. peupler les fichiers .md
    2. ajouter le titre : semaine bidule dates machin DONE
    2. ajouter les découpages par jour DONE
'''

import datetime
import pathlib
import os
import sys
from datetime import timedelta
from pprint import pprint

year = 2019
liste_periode = range(1, 6)
dic_fin_periodes = {
    0: "29/08/2019",
    1: "04/11/2019",
    2: "06/01/2020",
    3: "02/03/2020",
    4: "27/04/2020",
    5: "06/07/2020"
}
warning_periods_year = '''
Generation du cahier de texte de l'année {}.

Attention,
il faut modifier les dates des périodes dans les sources !
Les périodes en mémoire sont sont :
'''
warning_emploi_du_temps = '''
Attention, vous pouvez aussi modifier l'emploi du temps de chaque journée
dans les sources.

Il faut modifier la variable "content_per_day"

Pour l'instant elle contient :
'''

traduction = {
    # on pourrait utiliser des locales et traduire automatiquement...
    "Monday":       "Lundi",
    "Tuesday":      "Mardi",
    "Wednesday":    "Mercredi",
    "Thursday":     "Jeudi",
    "Friday":       "Vendredi",
    "Saturday":     "Samedi",
    "Sunday":       "Dimanche",
    "January":      "janvier",
    "February":     "février",
    "March":        "mars",
    "April":        "avril",
    "May":          "mai",
    "June":         "juin",
    "July":         "juillet",
    "August":       "août",
    "September":    "septembre",
    "October":      "octobre",
    "November":     "novembre",
    "December":     "décembre",
}

content_per_day = {
    0: "\n* 8h-8h55 - s213\n* 8h55-9h50 - s215\n* 10h-10h55 - s104\n",
    1: "\n* 8h-8h55 - s213\n* 8h55-9h50 - s215\n* 10h-10h55 - s104\n",
    2: "\n* 8h-8h55 - s213\n* 8h55-9h50 - s215\n* 10h-10h55 - s104\n",
    3: "\n* 8h-8h55 - s213\n* 8h55-9h50 - s215\n* 10h-10h55 - s104\n",
    4: "\n* 8h-8h55 - s213\n* 8h55-9h50 - s215\n* 10h-10h55 - s104\n",
    5: "\n",
    6: "\n",
}


# VARIABLES
liste_fin_periode = []

for period_nb, string_fin_periode in dic_fin_periodes.items():
    date_fin_periode = datetime.datetime.strptime(
        string_fin_periode, '%d/%m/%Y'
    )
    liste_fin_periode.append(date_fin_periode)

dic_semaine_periode = {}


# FONCTIONS

def get_start_and_end_date_from_calendar_week(year, calendar_week):
    '''
    Renvoie une liste de jours d'une semaine d'une année

    @param year: (int) numero de l'année : 2019
    @param calendar_week: (int) numero de la semaine : 36
    @return: (list of date) la liste des dates de la semaine du lundi au
        dimanche
    '''
    monday = datetime.datetime.strptime(
        f'{year}-{calendar_week}-1', "%Y-%W-%w"
    ).date()

    list_days = []
    for d in range(7):
        days = d + 0.9
        list_days.append(monday + datetime.timedelta(days=days))
    return list_days


def create_file_content(sem):
    '''
    Renvoie le contenu d'un fichier semaine.

    Le fichier est formaté markdown et on le remplit.

    @param sem: (int) numéro de semaine
    @return : (str) la chaîne de caractères qui est écrite dans le fichier
    '''
    current_year = year
    # on choisit la bonne année courante
    if int(sem) < 30:
        current_year = current_year + 1

    # on récupère la liste des dates de la semaine
    list_days = get_start_and_end_date_from_calendar_week(2019, sem - 1)

    # on formate toutes les dates pour énumérer plus facilement
    list_string_day = list(map(format_string_jour, list_days))
    file_content = "# Semaine {0} - du {1} au {2}\n\n".format(
        sem,
        list_string_day[0],
        list_string_day[-1],
    )
    # on itère sur les dates et ajoute le contenu de chaque journée
    for nb, day in enumerate(list_days):
        string_day = list_string_day[nb]
        # l'entête de chaque journée
        file_content += "\n## {0}\n".format(string_day)
        # le contenu de chaque journée
        file_content += content_per_day[nb]
    return file_content


def format_string_jour(day):
    '''
    Traduit une date au format français pour être écrite dans le fichier

    @param day: (date) date d'un jour
    @return : (str) le format d'un jour : Lundi 03 Septembre
    '''
    day_of_the_week = traduction[day.strftime("%A")]
    month = traduction[day.strftime("%B")]
    string_day = "{0} {1} {2}".format(
        day_of_the_week,
        day.strftime("%d"),
        month
    )
    return string_day


def create_md_file(period_nb, week_number):
    '''
    Crée le fichier .md de chaque semaine et le remplit
    Les dossiers existent déjà à cette étape, on se contente de les remplir
    de fichier et de remplir les fichiers.

    @param period_nb: (int) numero de période : 1
    @param week_number: (int) numero de semaine : 36
    @return : (None)
    SE : crée un fichier et écrit dedans
    '''

    # 0 ---> ./calendrier/periode_1
    path = default_path_md + str(period_nb + 1)
    # 36 ---> semaine_36.md
    filename = default_file_name.format(week_number)
    with open(os.path.join(path, filename), 'w+') as f:
        content = create_file_content(week_number)
        f.write(content)
        return


def create_cahier_texte():
    '''
    Fonction principale qui crée les fichiers et les remplit pour chaque
    période et chaque semaine de chaque période.

    On parcours chaque période de la liste des périodes.
    On crée les sous dossiers

    @param:
    @return None
    SE : plante en fin de travail, quand tout est fait, donc c'est pas important
    '''
    # on cree le dossier de l'année
    pathlib.Path(default_path_year).mkdir(parents=True, exist_ok=True)

    # on crée les dossiers de période
    for periode in liste_periode:
        pathlib.Path(
            default_path_md + str(periode)).mkdir(parents=True, exist_ok=True
                                                  )

    # on peuple les dossiers de période
    for period_nb, v in dic_fin_periodes.items():
        # on crée une liste pour chaque période
        dic_semaine_periode[period_nb] = []
        # on compte les semaines entre les dates

        try:
            # est-ce la dernière période ?
            # on récupère les dates et semaines extrèmes de la période
            date_debut = liste_fin_periode[period_nb]
            date_fin = liste_fin_periode[period_nb + 1]
            semaine_debut_periode = date_debut.isocalendar()[1]
            semaine_fin_periode = date_fin.isocalendar()[1]

            # on affiche un peu pour se repérer et voir l'avancée
            print('periode {}'.format(period_nb + 1), end=' - ')
            print("semaines {} jusque {}".format(
                semaine_debut_periode,
                semaine_fin_periode)
            )
            if semaine_debut_periode < semaine_fin_periode:
                # période normale, pas de changement d'année civile
                for sem_nbr in range(
                    semaine_debut_periode,
                    semaine_fin_periode
                ):
                    create_md_file(period_nb, sem_nbr)
            else:
                # changement d'année civile en cours de période
                for sem_nbr in range(semaine_debut_periode, 53):
                    create_md_file(period_nb, sem_nbr)
                for sem in range(1, semaine_fin_periode):
                    create_md_file(period_nb, sem_nbr)
        except IndexError as e:
            print("\nCalendrier généré correctement, fin du programme")
            print("\nPensez à copier le calendrier dans Github pour le publier")
            return


if __name__ == '__main__':
    args = sys.argv
    if len(args) > 1:
        try:
            # on s'assure que l'user comprend qu'il va créer 45 fichiers ...
            year = int(args[1])
            print(warning_periods_year.format(year))
            pprint(dic_fin_periodes)
            reponse_annee = input("Voulez-vous continuer ? (y/N) : ")
            if not reponse_annee == "y":
                exit("Fin du programme, aucun calendrier n'a été généré")
            print(warning_emploi_du_temps)
            pprint(content_per_day)
            reponse_edt = input("Voulez-vous continuer ? (y/N) : ")
            if not reponse_edt == "y":
                exit("Fin du programme, aucun calendrier n'a été généré")
            print()
        except ValueError as e:
            print(e)
            print("L'argument doit être une année, par exemple : 2019")
            raise e
    # l'user a tout compris on peut créer 45 fichiers :)
    default_path_year = "./calendrier/{}/".format(year)
    default_path_md = "./calendrier/{}/periode_".format(year)
    default_file_name = "semaine_{}.md"
    create_cahier_texte()
