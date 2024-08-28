#!/usr/bin/env python3
from __future__ import annotations

"""
---
Title : "Générateur de Cahier de texte"
Author : "qkzk" & "Amaroke"
Version : "2.0"
Date : "2019/08/02"
Last update : "2024/08/29"
---

"""

import locale
import os
import pathlib
import sys
from calendar import HTMLCalendar
from pprint import pprint
from datetime import datetime, timedelta

import data

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

WARNING_PERIODS_YEAR = """
Generation du cahier de texte de l'année {}.

Attention,
il faut modifier les dates des périodes dans les sources !
Les périodes en mémoire sont sont :
"""

WARNING_EMPLOI_DU_TEMPS = """
Attention, vous pouvez aussi modifier l'emploi du temps de chaque journée
dans les sources.

Il faut suivre ce qui est indiqué dans le fichier.

Pour l'instant elle contient :
"""

GOODBYE_MESSAGE = """
Calendrier généré correctement, fin du programme
Pensez à copier le calendrier dans Github pour le publier
"""


class DataDates:
    """Everything about scholar periods"""

    def __init__(self):
        self.year = data.year
        self.start_week = data.start_week
        self.list_periods = data.list_periods
        self.dict_period_ends = data.dict_period_ends
        self.list_period_ends = self.create_period_ends()

    def with_args(self) -> DataDates:
        if len(sys.argv) > 1:
            self.try_parse_argv(sys.argv)
        else:
            print(
                "Aucune année fournie, on utilise l'année {} comme exemple".format(
                    self.year
                )
            )
        return self

    def try_parse_argv(self, argv: list[str]):
        try:
            self.update_from_argv(argv)
        except ValueError as e:
            print(e)
            print("L'argument doit être une année, par exemple : 2019")
            raise e

    def create_period_ends(self) -> list:
        list_period_ends = []
        for _, string_fin_periode in self.dict_period_ends.items():
            date_end_period = datetime.strptime(string_fin_periode, "%d/%m/%Y")
            list_period_ends.append(date_end_period)
        return list_period_ends

    def update_from_argv(self, argv: list[str]) -> None:
        # Si l'année est fournie en paramètre
        self.year = int(argv[1])
        # Si la semaine de début est fournie en paramètre
        if len(argv) > 2:
            self.start_week = int(argv[2])

    @staticmethod
    def get_start_and_end_date_from_calendar_week(
        current_year: int, calendar_week: int
    ) -> list:
        """
        Renvoie une liste de jours d'une semaine d'une année.

        @param year_param: (int) numéro de l'année : 2019
        @param calendar_week: (int) numéro de la semaine : 36
        @return: (list of date) la liste des dates de la semaine du lundi au dimanche
        """
        monday = datetime.fromisocalendar(current_year, calendar_week, 1).date()

        list_days = []
        for d in range(7):
            days = d + 0.9
            list_days.append(monday + timedelta(days=days))
        return list_days


class Pathes:
    """Everything about used pathes"""

    def __init__(self, year: int):
        self.default_path_year = f"./calendrier/{year}/"
        self.default_path_md = f"./calendrier/{year}/periode_"
        self.default_file_name = "semaine_{}.md"


class CahierTexteCreator:
    def __init__(self, dates: DataDates, pathes: Pathes):
        self.dates = dates
        self.pathes = pathes
        self.content_per_day = data.content_per_day

    def pick_correct_year(self, sem: int) -> int:
        current_year = self.dates.year
        # On choisit la bonne année courante
        if int(sem) < 30:
            current_year = current_year + 1
        return current_year

    def format_dates(self, list_days: list):
        return list(map(self.format_string_jour, list_days))

    def format_file_content(self, sem: int, list_string_day: list) -> str:
        return "# Semaine {0} - du {1} au {2}\n\n".format(
            sem,
            list_string_day[0],
            list_string_day[-1],
        )

    def push_day_content(self, file_content: str, nb: int, string_day: str) -> str:
        # L'entête de chaque journée
        file_content += "\n## {0}\n".format(string_day)
        # Le contenu de chaque journée
        file_content += self.content_per_day[nb]
        return file_content

    def create_file_content(self, sem: int):
        """
        Renvoie le contenu d'un fichier semaine.

        Le fichier est formaté markdown et on le remplit.

        @param sem: (int) numéro de semaine
        @return : (str) la chaîne de caractères qui est écrite dans le fichier
        """
        # On récupère la liste des dates de la semaine
        list_days = self.dates.get_start_and_end_date_from_calendar_week(
            self.pick_correct_year(sem), sem
        )

        # On formate toutes les dates pour énumérer plus facilement
        list_string_day = self.format_dates(list_days)
        file_content = self.format_file_content(sem, list_string_day)

        # On itère sur les dates et ajoute le contenu de chaque journée
        for nb, _ in enumerate(list_days):
            file_content = self.push_day_content(file_content, nb, list_string_day[nb])

        return file_content

    def format_string_jour(self, day):
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

    def create_md_filename(self, period_nb_param: int, week_number: int):
        # 0 ---> ./calendrier/periode_1
        path = self.pathes.default_path_md + str(period_nb_param + 1)
        # 36 ---> semaine_36.md
        filename = self.pathes.default_file_name.format(week_number)
        return os.path.join(path, filename)

    def create_md_file(
        self,
        period_nb_param: int,
        week_number: int,
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

        md_content = self.create_file_content(week_number)
        with open(
            self.create_md_filename(period_nb_param, week_number), "w+"
        ) as md_file:
            md_file.write(md_content)

    @staticmethod
    def extract_week_number(dt: datetime) -> int:
        """Return the correct week for this date"""
        return dt.isocalendar()[1]

    def create_cahier_texte(self):
        """
        Fonction principale qui crée les fichiers et les remplit pour chaque
        période et chaque semaine de chaque période.

        On parcourt chaque période de la liste des périodes.
        On crée les sous dossiers

        @param:
        @return None
        """
        # On crée le dossier de l'année
        pathlib.Path(self.pathes.default_path_year).mkdir(parents=True, exist_ok=True)

        # On crée les dossiers de période
        for periode in self.dates.list_periods:
            pathlib.Path(self.pathes.default_path_md + str(periode)).mkdir(
                parents=True, exist_ok=True
            )

        # On peuple les dossiers de période
        for period_index in self.dates.dict_period_ends:
            # On récupère les dates et semaines extrêmes de la période
            date_debut: datetime = self.dates.list_period_ends[period_index]
            try:
                date_fin: datetime = self.dates.list_period_ends[period_index + 1]
            except IndexError:
                break
            semaine_debut_periode = self.extract_week_number(date_debut)
            semaine_fin_periode = self.extract_week_number(date_fin)
            # TODO start_year_2 non pris en compte
            start_year_2 = 1

            if (
                self.dates.start_week
                and not self.dates.start_week < semaine_debut_periode
            ):
                semaine_debut_periode = self.dates.start_week

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
                    self.create_md_file(
                        period_index,
                        sem_nbr,
                    )
            else:
                # Changement d'année civile en cours de période
                for sem_nbr in range(semaine_debut_periode, 53):
                    self.create_md_file(period_index, sem_nbr)
                for sem_nbr in range(1, semaine_fin_periode):
                    self.create_md_file(period_index, sem_nbr)

        # On affiche que tout c'est bien déroulé
        print(GOODBYE_MESSAGE)


class EventsMonthCalendar(HTMLCalendar):
    """
    Classe qui étend HTMLCalendar en formatant les jours
    Utilisée pour générer une table d'un mois dont les jours pointent
    vers une page de la semaine.
    Les pages étant rangées dans des sous dossiers par période
    """

    START_URL = "https://github.com/qkzk/cours/blob/master/"
    END_URL = ".md"

    def __init__(self, year_param, month, liste_fin_periode, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.month = month
        self.year = year_param
        self.liste_fin_periode = liste_fin_periode

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
        return self.START_URL + middle_url + self.END_URL

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


class LinkCalendar:
    def __init__(self, dates: DataDates, pathes: Pathes):
        self.dates = dates
        self.pathes = pathes

    def generate_months(self):
        """
        Génère du contenu HTML dans une string
        Pour être affiché dans github

        @return: (str) une page HTML avec un calendrier de l'année scolaire.
            Chaque jour est un lien vers une page github
        """
        html_string = ""

        for month in range(9, 13):
            html_string += "\n" * 3
            html_string += EventsMonthCalendar(
                self.dates.year, month, self.dates.list_period_ends
            ).formatmonth(self.dates.year, month)

        for month in range(1, 7):
            html_string += "\n" * 3
            html_string += EventsMonthCalendar(
                self.dates.year + 1, month, self.dates.list_period_ends
            ).formatmonth(self.dates.year + 1, month)

        return html_string

    def write_html_months(self):
        """
        Écrit le fichier README.md avec le contenu HTML à l'adresse :
        ./calendrier/2019/README.md

        Utilise les méthodes generateMonths et la classe EventsMonthCalendar
        @return: (None)
        SE: crée un fichier écrit dedans.
        """
        # 0 ---> ./calendrier/2019
        content = self.generate_months()
        print(content[:100])

        path = self.pathes.default_path_year
        filename = "README.md"
        file_path = os.path.join(path, filename)
        print(file_path)
        with open(file_path, "w+") as f:
            f.write(content)
            return


def color_text(text, color="BOLD"):
    return TEXT_COLORS[color] + text + TEXT_COLORS["END"]


def user_input(dates: DataDates):
    print(WARNING_PERIODS_YEAR.format(dates.year))

    # TODO Changer affichage
    pprint(dates.dict_period_ends)

    reponse_annee = input(
        color_text(color_text("Voulez-vous continuer ? (y/N) : ", "BOLD"), "RED")
    )

    if reponse_annee != "y":
        exit("Fin du programme, aucun calendrier n'a été généré")

    print(WARNING_EMPLOI_DU_TEMPS)

    # TODO Changer affichage
    pprint(data.content_per_day)

    reponse_edt = input(
        color_text(
            color_text(
                "Voulez-vous continuer ? (y/N) : ",
                "BOLD",
            ),
            "RED",
        )
    )

    if reponse_edt != "y":
        exit("Fin du programme, aucun calendrier n'a été généré\n")


def main():
    print(color_text(WELCOME_BANNER, "DARKCYAN"))
    dates = DataDates().with_args()
    user_input(dates)

    pathes = Pathes(dates.year)
    # L'utilisateur a tout compris on peut créer 45 fichiers :)

    # On crée les dossiers et les fichiers de la semaine
    CahierTexteCreator(dates, pathes).create_cahier_texte()

    # On crée les liens depuis un calendrier
    LinkCalendar(dates, pathes).write_html_months()


if __name__ == "__main__":
    main()
