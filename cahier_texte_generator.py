#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
---
title: "Générateur de Cahier de texte"
author: "qkzk"
version: "1.1"
date: "2019/08/02"
---

"""

import calendar
import datetime
import os
import pathlib
import sys
from calendar import HTMLCalendar
from datetime import timedelta
from pprint import pprint

from content_per_day import content_per_day

year = 2022
start_week = None
liste_periode = range(1, 6)
dic_fin_periodes = {
    0: "31/08/2022",  # pre rentrée
    1: "07/11/2022",  # rentrée vacances Toussaint
    2: "02/01/2023",  # rentrée vacances Noël
    3: "27/02/2023",  # rentrée vacances d'hiver
    4: "01/05/2023",  # rentrée vacances Printemps
    5: "08/07/2023",  # fin d'année scolaire
}

# constants
TEXT_COLORS = {
    "PURPLE": "\033[95m",
    "CYAN": "\033[96m",
    "DARKCYAN": "\033[36m",
    "BLUE": "\033[94m",
    "GREEN": "\033[92m",
    "YELLOW": "\033[93m",
    "RED": "\033[91m",
    "BOLD": "\033[1m",
    "UNDERLINE": "\033[4m",
    "END": "\033[0m",
}


WELCOME_BANNER = """Bienvenue dans ...


:'######:::::'###::::'##::::'##:'####:'########:'########::
'##... ##:::'## ##::: ##:::: ##:. ##:: ##.....:: ##.... ##:
 ##:::..:::'##:. ##:: ##:::: ##:: ##:: ##::::::: ##:::: ##:
 ##:::::::'##:::. ##: #########:: ##:: ######::: ########::
 ##::::::: #########: ##.... ##:: ##:: ##...:::: ##.. ##:::
 ##::: ##: ##.... ##: ##:::: ##:: ##:: ##::::::: ##::. ##::
. ######:: ##:::: ##: ##:::: ##:'####: ########: ##:::. ##:
:......:::..:::::..::..:::::..::....::........::..:::::..::
'########:'########:'##::::'##:'########:'########:
... ##..:: ##.....::. ##::'##::... ##..:: ##.....::
::: ##:::: ##::::::::. ##'##:::::: ##:::: ##:::::::
::: ##:::: ######:::::. ###::::::: ##:::: ######:::
::: ##:::: ##...:::::: ## ##:::::: ##:::: ##...::::
::: ##:::: ##:::::::: ##:. ##::::: ##:::: ##:::::::
::: ##:::: ########: ##:::. ##:::: ##:::: ########:
:::..:::::........::..:::::..:::::..:::::........::
:::'###::::'##::::'##:'########::'#######::
::'## ##::: ##:::: ##:... ##..::'##.... ##:
:'##:. ##:: ##:::: ##:::: ##:::: ##:::: ##:
'##:::. ##: ##:::: ##:::: ##:::: ##:::: ##:
 #########: ##:::: ##:::: ##:::: ##:::: ##:
 ##.... ##: ##:::: ##:::: ##:::: ##:::: ##:
 ##:::: ##:. #######::::: ##::::. #######::
..:::::..:::.......::::::..::::::.......:::


"""

warning_periods_year = """
Generation du cahier de texte de l'année {}.

Attention,
il faut modifier les dates des périodes dans les sources !
Les périodes en mémoire sont sont :
"""
warning_emploi_du_temps = """
Attention, vous pouvez aussi modifier l'emploi du temps de chaque journée
dans les sources.

Il faut modifier la variable "content_per_day"

Pour l'instant elle contient :
"""

traduction = {
    # on pourrait utiliser des locales et traduire automatiquement...
    "Monday": "Lundi",
    "Tuesday": "Mardi",
    "Wednesday": "Mercredi",
    "Thursday": "Jeudi",
    "Friday": "Vendredi",
    "Saturday": "Samedi",
    "Sunday": "Dimanche",
    "January": "janvier",
    "February": "février",
    "March": "mars",
    "April": "avril",
    "May": "mai",
    "June": "juin",
    "July": "juillet",
    "August": "août",
    "September": "septembre",
    "October": "octobre",
    "November": "novembre",
    "December": "décembre",
}


# VARIABLES
liste_fin_periode = []

for period_nb, string_fin_periode in dic_fin_periodes.items():
    date_fin_periode = datetime.datetime.strptime(string_fin_periode, "%d/%m/%Y")
    liste_fin_periode.append(date_fin_periode)

print("liste fin de période")
print(liste_fin_periode)


# dic_semaine_periode = {}


# FONCTIONS


def get_start_and_end_date_from_calendar_week(year, calendar_week):
    """
    Renvoie une liste de jours d'une semaine d'une année

    @param year: (int) numero de l'année : 2019
    @param calendar_week: (int) numero de la semaine : 36
    @return: (list of date) la liste des dates de la semaine du lundi au
        dimanche
    """
    monday = datetime.datetime.strptime(f"{year}-{calendar_week}-1", "%Y-%W-%w").date()

    list_days = []
    for d in range(7):
        days = d + 0.9
        list_days.append(monday + datetime.timedelta(days=days))
    return list_days


def create_file_content(sem):
    """
    Renvoie le contenu d'un fichier semaine.

    Le fichier est formaté markdown et on le remplit.

    @param sem: (int) numéro de semaine
    @return : (str) la chaîne de caractères qui est écrite dans le fichier
    """
    current_year = year
    # on choisit la bonne année courante
    if int(sem) < 30:
        current_year = current_year + 1

    # on récupère la liste des dates de la semaine
    list_days = get_start_and_end_date_from_calendar_week(current_year, sem)

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
    """
    Traduit une date au format français pour être écrite dans le fichier

    @param day: (date) date d'un jour
    @return : (str) le format d'un jour : Lundi 03 Septembre
    """
    day_of_the_week = traduction[day.strftime("%A")]
    month = traduction[day.strftime("%B")]
    string_day = "{0} {1} {2}".format(day_of_the_week, day.strftime("%d"), month)
    return string_day


def create_md_file(period_nb, week_number):
    """
    Crée le fichier .md de chaque semaine et le remplit
    Les dossiers existent déjà à cette étape, on se contente de les remplir
    de fichier et de remplir les fichiers.

    @param period_nb: (int) numero de période : 1
    @param week_number: (int) numero de semaine : 36
    @return : (None)
    SE : crée un fichier et écrit dedans
    """

    # 0 ---> ./calendrier/periode_1
    path = default_path_md + str(period_nb + 1)
    # 36 ---> semaine_36.md
    filename = default_file_name.format(week_number)
    with open(os.path.join(path, filename), "w+") as f:
        content = create_file_content(week_number)
        f.write(content)
        return


def create_cahier_texte(start_week=None):
    """
    Fonction principale qui crée les fichiers et les remplit pour chaque
    période et chaque semaine de chaque période.

    On parcourt chaque période de la liste des périodes.
    On crée les sous dossiers

    @param:
    @return None
    SE : plante en fin de travail, quand tout est fait, donc c'est pas important
    """
    # on cree le dossier de l'année
    pathlib.Path(default_path_year).mkdir(parents=True, exist_ok=True)

    # on crée les dossiers de période
    for periode in liste_periode:
        pathlib.Path(default_path_md + str(periode)).mkdir(parents=True, exist_ok=True)

    # on peuple les dossiers de période
    for period_nb, v in dic_fin_periodes.items():
        # on crée une liste pour chaque période
        # dic_semaine_periode[period_nb] = []
        # on compte les semaines entre les dates

        try:
            # est-ce la dernière période ?
            # on récupère les dates et semaines extrèmes de la période
            date_debut = liste_fin_periode[period_nb]
            date_fin = liste_fin_periode[period_nb + 1]
            semaine_debut_periode = date_debut.isocalendar()[1]
            semaine_fin_periode = date_fin.isocalendar()[1]
            start_year_2 = 1

            if start_week:
                if start_week < semaine_debut_periode:
                    # on débute après la nouvelle année civile
                    start_year_2 = start_week
                else:
                    # on debute qq semaines après la rentrée
                    semaine_debut_periode = start_week

            # on affiche un peu pour se repérer et voir l'avancée
            print("periode {}".format(period_nb + 1), end=" - ")
            print(
                "semaines {} jusque {}".format(
                    semaine_debut_periode, semaine_fin_periode
                )
            )
            if semaine_debut_periode < semaine_fin_periode:
                # période normale, pas de changement d'année civile
                for sem_nbr in range(semaine_debut_periode, semaine_fin_periode):
                    create_md_file(period_nb, sem_nbr)
            else:
                # changement d'année civile en cours de période
                for sem_nbr in range(semaine_debut_periode, 53):
                    create_md_file(period_nb, sem_nbr)
                for sem_nbr in range(1, semaine_fin_periode):
                    create_md_file(period_nb, sem_nbr)
        except IndexError as e:
            print("\nCalendrier généré correctement, fin du programme")
            print("\nPensez à copier le calendrier dans Github pour le publier")
            return


class EventsMonthCalendar(HTMLCalendar):
    """
    Classe qui étend HTMLCalendar en formattant les jours
    Utilisée pour générer une table d'un mois dont les jours pointent
    vers une page de la semaine.
    Les pages étant rangées dans des sous dossiers par période
    """

    def __init__(self, year, month, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.month = month
        self.year = year
        self.start_url = "https://github.com/qkzk/cours/blob/master/"
        self.end_url = ".md"

    def which_day(self, day):
        """
        Renvoie la date du jour en question
        @param day: (int) le jour
        @return: (datetime) datetime du jour
        """
        return datetime.datetime(self.year, self.month, day)

    def which_period(self, day):
        """
        Renvoie la période du jour en question
        @param day: (int) le numéro du jour
        @return: (int) le numéro de la période
        """
        theday = self.which_day(day)
        for nb_period, date_fin_period in enumerate(liste_fin_periode):
            if theday < date_fin_period:
                return nb_period

    def which_weeknumber(self, day):
        """
        Renvoie le numéro de la semaine correspondante
        @param day: (int) le numéro du jour
        @return: (int) le numéro de la semaine
        """
        theday = self.which_day(day)
        return theday.isocalendar()[1]

    def formatURL(self, nb_period, nb_week):
        """
        Formatte une url pour atteindre mon repo

        https://github.com/qkzk/cours/blob/master/2019/periode_5/semaine_18.md

        @param nb_period: (int) le numéro de la période
        @param nb_week: (int) le numéro de la semaine
        @return: (str) l'url correspondant à cette semaine

        TODO modifier le nom de l'auteur et du repo pour être plus générique
        """
        school_year = self.year if nb_week > 30 else self.year - 1
        middle_url = (
            str(school_year) + "/periode_" + str(nb_period) + "/semaine_" + str(nb_week)
        )
        return self.start_url + middle_url + self.end_url

    def formatday(self, day, weekday):
        """
        Return a day as a table cell.
        @param day: (int) le numero du jour
        @param weekday: (int) le numéro du jour de la semaine
        """
        if day == 0:
            return '<td class="noday">&nbsp;</td>'  # day outside month
        else:
            nb_period = self.which_period(day)
            if nb_period is None:
                raise ValueError(f"{day}, {weekday}, {nb_period}")
            nb_week = self.which_weeknumber(day)
            string_url = self.formatURL(nb_period, nb_week)
            return '<td class="{0}"><a href="{1}">{2}</a></td>'.format(
                self.cssclasses[weekday], string_url, day
            )


def generateMonthes():
    """
    Génère du contenu HTML dans une string
    Pour être affiché dans github

    @return: (str) une page HTML avec un calendrier de l'année scolaire.
        Chaque jour est un lien vers une page github
    """
    html_string = ""

    for month in range(9, 13):
        html_string += "\n" * 3
        html_string += EventsMonthCalendar(year, month).formatmonth(year, month)

    for month in range(1, 7):
        html_string += "\n" * 3
        html_string += EventsMonthCalendar(year + 1, month).formatmonth(year + 1, month)

    return html_string


def write_html_monthes():
    """
    Ecrit le fichier README.md avec le contenu HTML à l'adresse :
    ./calendrier/2019/README.md

    Utilise les méthodes generateMonthes et la classe EventsMonthCalendar
    @return: (None)
    SE: crée un fichier écrit dedans.
    """
    # 0 ---> ./calendrier/2019
    path = default_path_year
    filename = "README.md"
    with open(os.path.join(path, filename), "w+") as f:
        content = generateMonthes()
        f.write(content)
        return


def color_text(text, color="BOLD"):
    return TEXT_COLORS[color] + text + TEXT_COLORS["END"]


if __name__ == "__main__":
    print(color_text(WELCOME_BANNER, "DARKCYAN"))
    args = sys.argv
    if len(args) > 1:
        try:
            # on s'assure que l'user comprend qu'il va créer 45 fichiers ...
            year = int(args[1])
            if len(args) > 2:
                start_week = int(args[2])
            print(warning_periods_year.format(year))
            pprint(dic_fin_periodes)
            reponse_annee = input(
                color_text(
                    color_text("Voulez-vous continuer ? (y/N) : ", "BOLD"), "RED"
                )
            )
            if not reponse_annee == "y":
                exit("Fin du programme, aucun calendrier n'a été généré")
            print(warning_emploi_du_temps)
            pprint(content_per_day)
            reponse_edt = input(
                color_text(
                    color_text("Voulez-vous continuer ? (y/N) : ", "BOLD"), "RED"
                )
            )
            if not reponse_edt == "y":
                exit("Fin du programme, aucun calendrier n'a été généré")
            print()
        except ValueError as e:
            print(e)
            print("L'argument doit être une année, par exemple : 2019")
            raise e
    else:
        print("Aucune année fournie, on utilise l'année {} comme exemple".format(year))
    # l'user a tout compris on peut créer 45 fichiers :)
    default_path_year = "./calendrier/{}/".format(year)
    default_path_md = "./calendrier/{}/periode_".format(year)
    default_file_name = "semaine_{}.md"
    # on crée les dossiers et les fichiers de la semaine
    create_cahier_texte(start_week=start_week)
    # on crée les liens depuis un calendrier
    write_html_monthes()
