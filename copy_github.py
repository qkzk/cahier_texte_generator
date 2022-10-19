#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# TODO incompatible open-source

'''
Copier le calendrier qu'on vient de générer vers le dossier cours de github
'''
import distutils.dir_util
import os
import os.path
import subprocess
from shutil import copyfile

import importlib.util

# colors module
filepath_color = "/home/quentin/gdrive/dev/python/linux_utils/tests/colors.py"
spec = importlib.util.spec_from_file_location(
    "color", filepath_color)
color = importlib.util.module_from_spec(spec)
spec.loader.exec_module(color)

calendar_path = "/home/quentin/gdrive/dev/python/" \
                "boulot_utils/cahier_texte_generator/calendrier/"
gitcours_path = "/home/quentin/gdrive/cours/git_cours/cours/"

which_year_msg = "Quelle année voulez-vous copier ? "
which_week_msg = "À partir de quelle semaine  ? [34] "
calendar_not_exist_msg = "Vous devez d'abord générer " \
                         "le cahier de texte de l'année {}"

start_week_invalid_msg = "La semaine proposée ne convient pas"
is_gitadd_msg = "Do you want to push this calendar to git_cours ? [yes/NO] "
gitadd_cmd = '/home/quentin/scripts/gitadd.sh {}'
gitadd_succes_msg = 'files pushed to git_cours : https://github.com/qkzk/cours/tree/master/{}'
success_msg = "All you base are belong to us"


def ask(msg, col):
    return input(color.format_color(msg, col))


def does_calendar_exists(year):
    calendar_exists = os.path.isdir(calendar_path + year)
    if not calendar_exists:
        color.print_color(calendar_not_exist_msg.format(year), "red")
        color.print_color("Exiting", "red")
        exit(0)
    return True


def get_startweek():
    start_week = ask(which_week_msg, "yellow")
    if start_week == '':
        start_week = 34
    else:
        try:
            start_week = int(start_week)
        except ValueError:
            color.print_color(start_week_invalid_msg)
            color.print_color("Exiting", "red")
            exit(0)
        if start_week > 52:
            color.print_color(start_week_invalid_msg)
            color.print_color("Exiting", "red")
            exit(0)
    return start_week


def get_range_weeks(start_week):
    if start_week < 30:
        weeks_first_year = range(0, 0)
        weeks_second_year = range(start_week, 31)
    else:
        weeks_first_year = range(start_week, 53)
        weeks_second_year = range(0, 30)
    range_weeks = {
        "weeks_first_year": weeks_first_year,
        "weeks_second_year": weeks_second_year,
        "weeks_first_year": weeks_first_year,
        "weeks_second_year": weeks_second_year,
    }
    return range_weeks


def clean_dest_folder(year, start_week, range_weeks):
    git_calendar_exists = os.path.isdir(gitcours_path + year)
    if git_calendar_exists:

        # vider le dossier
        for period in range(1, 6):
            for week in range(1, 53):
                if week in range_weeks["weeks_first_year"] \
                        or week in range_weeks["weeks_second_year"]:
                    try:
                        file = gitcours_path + year + \
                               "/periode_{}/semaine_{}.md".format(period, week)
                        os.remove(file)
                        color.print_color(f"Deleted : {file}", "white")
                    except OSError:
                        pass


def copy_if_not_exist(year, start_week, range_weeks):
    src = calendar_path + year
    dst = gitcours_path + year

    for period in range(1, 6):
        for week in range(1, 53):
            if week in range_weeks["weeks_first_year"] \
                    or week in range_weeks["weeks_second_year"]:
                src_week = src + "/periode_{}/semaine_{}.md".format(period,
                                                                    week)
                dst_week = dst + "/periode_{}/semaine_{}.md".format(period,
                                                                    week)
                dst_dir = dst + "/periode_{}/".format(period)
                try:
                    if not os.path.exists(dst_dir):
                        os.makedirs(dst_dir)
                        color.print_color(f"created directory : {dst_dir}",
                                          "white")
                    lst = copyfile(src_week, dst_week)
                    color.print_color(f"Copied to : {dst_week}", "white")
                except FileNotFoundError as e:
                    # print(e)
                    # print(src_week, dst_week)
                    pass
    # copy readme (avec le calendrier présentable dans github)
    src_readme = src + "/README.md"
    dst_readme = dst + "/README.md"
    lst = copyfile(src_readme, dst_readme)
    color.print_color(f"Readme copied to : {dst_readme}", "white")

    print()


def ask_gitadd_and_gitadd(year):
    is_gitadd = ask(is_gitadd_msg, "yellow")
    if is_gitadd in 'yesYES':
        os.chdir(gitcours_path)
        subprocess.call(gitadd_cmd.format("calendar " + year), shell=False)
        color.print_color(gitadd_succes_msg.format(year), "cyan")


def main():
    # 1 demander quelle année copier
    year = ask(which_year_msg, 'yellow')
    # 2 vérifier si le calendrier existe déjà
    does_calendar_exists(year)
    # 3 à partir de quelle semaine
    start_week = get_startweek()
    # 4 obtenir les ranges de semaine à copier
    range_weeks = get_range_weeks(start_week)
    # 4 effacer si deja existant
    clean_dest_folder(year, start_week, range_weeks)
    # 5 copier si ça n'existe pas
    copy_if_not_exist(year, start_week, range_weeks)
    # 6 gitadd
    ask_gitadd_and_gitadd(year)
    # 7 bye
    color.print_color(success_msg, "cyan")


if __name__ == '__main__':
    main()
