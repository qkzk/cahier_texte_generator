#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
---
Title : "Générateur de Cahier de texte"
Author : "qkzk" & "Amaroke"
Version : "1.1"
Date : "2019/08/02"
Last update : "2022/10/19"
---

"""

import locale
import datetime
import os
import pathlib
import sys
import data
from calendar import HTMLCalendar
from pprint import pprint
from datetime import datetime, timedelta

# CONSTANTES
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

Il faut suivre ce qui est indiqué dans le fichier.

Pour l'instant elle contient :
"""

# VARIABLES
# TODO Récupérer les données dans un fichier externe au code


# FONCTIONS
def get_start_and_end_date_from_calendar_week(
    year_param: int, calendar_week: int
) -> list:
    """
    Renvoie une liste de jours d'une semaine d'une année.

    @param year_param: (int) numéro de l'année : 2019
    @param calendar_week: (int) numéro de la semaine : 36
    @return: (list of date) la liste des dates de la semaine du lundi au dimanche
    """
    monday = datetime.fromisocalendar(year_param, calendar_week, 1).date()

    list_days = []
    for d in range(7):
        days = d + 0.9
        list_days.append(monday + timedelta(days=days))
    return list_days


def create_file_content(sem: int, year: int):
    """
    Renvoie le contenu d'un fichier semaine.

    Le fichier est formaté markdown et on le remplit.

    @param sem: (int) numéro de semaine
    @return : (str) la chaîne de caractères qui est écrite dans le fichier
    """
    current_year = year
    # On choisit la bonne année courante
    if int(sem) < 30:
        current_year = current_year + 1

    # On récupère la liste des dates de la semaine
    list_days = get_start_and_end_date_from_calendar_week(current_year, sem)

    # On formate toutes les dates pour énumérer plus facilement
    list_string_day = list(map(format_string_jour, list_days))
    file_content = "# Semaine {0} - du {1} au {2}\n\n".format(
        sem,
        list_string_day[0],
        list_string_day[-1],
    )

    # On itère sur les dates et ajoute le contenu de chaque journée
    for nb, _ in enumerate(list_days):
        string_day = list_string_day[nb]
        # L'entête de chaque journée
        file_content += "\n## {0}\n".format(string_day)
        # Le contenu de chaque journée
        file_content += data.content_per_day[nb]

    return file_content


def format_string_jour(day):
    """
    Traduit une date au format français pour être écrite dans le fichier

    @param day: (date) date d'un jour
    @return : (str) le format d'un jour : lundi 03 septembre
    """
    # On utilise setlocale pour ne pas avoir à traduire "manuellement".
    locale.setlocale(locale.LC_ALL, "")
    day_of_the_week = day.strftime("%A")
    month = day.strftime("%B")
    string_day = "{0} {1} {2}".format(day_of_the_week, day.strftime("%d"), month)
    return string_day


def create_md_file(
    year: int,
    period_nb_param: int,
    week_number: int,
    default_path_md: str,
    default_file_name: str,
):
    """
    Crée le fichier .md de chaque semaine et le remplit
    Les dossiers existent déjà à cette étape, on se contente de les remplir
    de fichier et de remplir les fichiers.

    @param period_nb_param: (int) numéro de période : 1
    @param week_number: (int) numéro de semaine : 36
    @return : (None)
    SE : crée un fichier et écrit dedans
    """

    # 0 ---> ./calendrier/periode_1
    path = default_path_md + str(period_nb_param + 1)
    # 36 ---> semaine_36.md
    filename = default_file_name.format(week_number)
    with open(os.path.join(path, filename), "w+") as f:
        content = create_file_content(week_number, year)
        f.write(content)
        return


def extract_week_number(dt: datetime) -> int:
    """Return the correct week for this date"""
    return dt.isocalendar()[1]


def create_cahier_texte(
    year: int,
    default_path_year: str,
    default_path_md: str,
    liste_periode: list[int],
    dic_fin_periodes: dict[int, str],
    liste_fin_periode: list,
    default_file_name: str,
    start_week_param=None,
):
    """
    Fonction principale qui crée les fichiers et les remplit pour chaque
    période et chaque semaine de chaque période.

    On parcourt chaque période de la liste des périodes.
    On crée les sous dossiers

    @param:
    @return None
    """
    # On crée le dossier de l'année
    pathlib.Path(default_path_year).mkdir(parents=True, exist_ok=True)

    # On crée les dossiers de période
    for periode in liste_periode:
        pathlib.Path(default_path_md + str(periode)).mkdir(parents=True, exist_ok=True)

    # On peuple les dossiers de période
    for period_index, _ in dic_fin_periodes.items():
        # On récupère les dates et semaines extrêmes de la période
        date_debut: datetime = liste_fin_periode[period_index]
        try:
            date_fin: datetime = liste_fin_periode[period_index + 1]
        except IndexError:
            break
        semaine_debut_periode = extract_week_number(date_debut)
        semaine_fin_periode = extract_week_number(date_fin)
        # TODO start_year_2 non pris en compte
        start_year_2 = 1

        if start_week_param:
            if start_week_param < semaine_debut_periode:
                # On débute après la nouvelle année civile
                start_year_2 = start_week_param
            else:
                # On débute quelques semaines après la rentrée
                semaine_debut_periode = start_week_param

        # On affiche un peu pour se repérer et voir l'avancée
        print("periode {}".format(period_index + 1), end=" - ")
        print(
            "semaines {} jusque {}".format(
                semaine_debut_periode,
                52 if (semaine_fin_periode - 1 == 0) else semaine_fin_periode - 1,
            )
        )
        if semaine_debut_periode < semaine_fin_periode:
            # Période normale, pas de changement d'année civile
            for sem_nbr in range(semaine_debut_periode, semaine_fin_periode):
                create_md_file(
                    year, period_index, sem_nbr, default_path_md, default_file_name
                )
        else:
            # Changement d'année civile en cours de période
            for sem_nbr in range(semaine_debut_periode, 53):
                create_md_file(
                    year, period_index, sem_nbr, default_path_md, default_file_name
                )
            for sem_nbr in range(1, semaine_fin_periode):
                create_md_file(
                    year, period_index, sem_nbr, default_path_md, default_file_name
                )

    # On affiche que tout c'est bien déroulé
    print("\nCalendrier généré correctement, fin du programme")
    print("\nPensez à copier le calendrier dans Github pour le publier")


class EventsMonthCalendar(HTMLCalendar):
    """
    Classe qui étend HTMLCalendar en formatant les jours
    Utilisée pour générer une table d'un mois dont les jours pointent
    vers une page de la semaine.
    Les pages étant rangées dans des sous dossiers par période
    """

    def __init__(self, year_param, month, liste_fin_periode, *args_param, **kwargs):
        super().__init__(*args_param, **kwargs)
        self.month = month
        self.year = year_param
        self.liste_fin_periode = liste_fin_periode
        self.start_url = "https://github.com/qkzk/cours/blob/master/"
        self.end_url = ".md"

    def which_day(self, day: int):
        """
        Renvoie la date du jour en question
        @param day: (int) le jour
        @return: (datetime) datetime du jour
        """
        return datetime(self.year, self.month, day)

    def which_period(self, day: int, liste_fin_periode: list):
        """
        Renvoie la période du jour en question
        @param day: (int) le numéro du jour
        @return: (int) le numéro de la période
        """
        theday = self.which_day(day)
        for nb_period, date_fin_period in enumerate(liste_fin_periode):
            if theday < date_fin_period:
                return nb_period

    def which_week_number(self, day):
        """
        Renvoie le numéro de la semaine correspondante
        @param day: (int) le numéro du jour
        @return: (int) le numéro de la semaine
        """
        theday = self.which_day(day)
        return theday.isocalendar()[1]

    def formatURL(self, nb_period, nb_week):
        """
        Formate une url pour atteindre mon repo

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

    def formatday(self, day: int, weekday: int):
        """
        Return a day as a table cell.
        @param day: (int) le numéro du jour
        @param weekday: (int) le numéro du jour de la semaine
        """
        if day == 0:
            return '<td class="noday">&nbsp;</td>'  # day outside month
        else:
            nb_period = self.which_period(day, self.liste_fin_periode)
            if nb_period is None:
                raise ValueError(f"{day}, {weekday}, {nb_period}")
            nb_week = self.which_week_number(day)
            string_url = self.formatURL(nb_period, nb_week)
            return '<td class="{0}"><a href="{1}">{2}</a></td>'.format(
                self.cssclasses[weekday], string_url, day
            )


def generate_months(year: int, liste_fin_periode: list):
    """
    Génère du contenu HTML dans une string
    Pour être affiché dans github

    @return: (str) une page HTML avec un calendrier de l'année scolaire.
        Chaque jour est un lien vers une page github
    """
    html_string = ""

    for month in range(9, 13):
        html_string += "\n" * 3
        html_string += EventsMonthCalendar(year, month, liste_fin_periode).formatmonth(
            year, month
        )

    for month in range(1, 7):
        html_string += "\n" * 3
        html_string += EventsMonthCalendar(
            year + 1, month, liste_fin_periode
        ).formatmonth(year + 1, month)

    return html_string


def write_html_months(year: int, default_path_year: str, liste_fin_periode: list):
    """
    Écrit le fichier README.md avec le contenu HTML à l'adresse :
    ./calendrier/2019/README.md

    Utilise les méthodes generateMonths et la classe EventsMonthCalendar
    @return: (None)
    SE: crée un fichier écrit dedans.
    """
    # 0 ---> ./calendrier/2019
    path = default_path_year
    filename = "README.md"
    with open(os.path.join(path, filename), "w+") as f:
        content = generate_months(year, liste_fin_periode)
        f.write(content)
        return


def color_text(text, color="BOLD"):
    return TEXT_COLORS[color] + text + TEXT_COLORS["END"]


def main():
    year = data.year
    start_week = data.start_week
    liste_periode = list(data.liste_periode)
    dic_fin_periodes = data.dic_fin_periodes

    liste_fin_periode = []

    for _, string_fin_periode in dic_fin_periodes.items():
        date_fin_periode = datetime.strptime(string_fin_periode, "%d/%m/%Y")
        liste_fin_periode.append(date_fin_periode)

    print(color_text(WELCOME_BANNER, "DARKCYAN"))

    args = sys.argv
    if len(args) > 1:
        try:
            # Si l'année est fournie en paramètre
            year = int(args[1])

            # Si la semaine de début est fournie en paramètre
            if len(args) > 2:
                start_week = int(args[2])

            print(warning_periods_year.format(year))

            # TODO Changer affichage
            pprint(dic_fin_periodes)

            reponse_annee = input(
                color_text(
                    color_text("Voulez-vous continuer ? (y/N) : ", "BOLD"), "RED"
                )
            )

            if reponse_annee != "y":
                exit("Fin du programme, aucun calendrier n'a été généré")

            print(warning_emploi_du_temps)

            # TODO Changer affichage
            pprint(data.content_per_day)

            reponse_edt = input(
                color_text(
                    color_text("Voulez-vous continuer ? (y/N) : ", "BOLD"), "RED"
                )
            )

            if reponse_edt != "y":
                exit("Fin du programme, aucun calendrier n'a été généré\n")

        except ValueError as e:
            print(e)
            print("L'argument doit être une année, par exemple : 2019")
            raise e

    else:
        print("Aucune année fournie, on utilise l'année {} comme exemple".format(year))

    # L'utilisateur a tout compris on peut créer 45 fichiers :)
    default_path_year = "./calendrier/{}/".format(year)
    default_path_md = "./calendrier/{}/periode_".format(year)
    default_file_name = "semaine_{}.md"

    # On crée les dossiers et les fichiers de la semaine
    create_cahier_texte(
        year,
        default_path_year,
        default_path_md,
        liste_periode,
        dic_fin_periodes,
        liste_fin_periode,
        default_file_name,
        start_week,
    )

    # On crée les liens depuis un calendrier
    write_html_months(year, default_path_year, liste_fin_periode)


if __name__ == "__main__":
    main()
