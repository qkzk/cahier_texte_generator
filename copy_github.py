'''
Copier le calendrier qu'on vient de générer vers le dossier cours de github
'''
# colors module
import distutils.dir_util
import os
import glob
import os.path
import shutil
import subprocess

import importlib.util
filepath_color = "/home/quentin/gdrive/dev/python/linux_utils/tests/colors.py"
spec = importlib.util.spec_from_file_location(
    "color", filepath_color)
color = importlib.util.module_from_spec(spec)
spec.loader.exec_module(color)

which_year_msg = "Quelle année voulez-vous copier ? "

calendar_path = "/home/quentin/gdrive/dev/python/"\
    "boulot_utils/cahier_texte_generator/calendrier/"


which_week_msg = "À partir de quelle semaine  ? [35] "

gitcours_path = "/home/quentin/gdrive/cours/git_cours/cours/"

calendar_not_exist_msg = "Vous devez d'abord générer "\
    "le cahier de texte de l'année {}"

start_week_invalid_msg = "La semaine proposée ne convient pas"

success_msg = "All you base are belong to us"


def ask(msg, col):
    return input(color.format_color(msg, col))


# 1 demander quelle année copier
year = input(color.format_color(which_year_msg, 'yellow'))

# 2 vérifier si le calendrier existe déjà
calendar_exists = os.path.isdir(calendar_path + year)
if not calendar_exists:
    color.print_color(calendar_not_exist_msg.format(year), "red")
    color.print_color("Exiting", "red")
    exit(0)

# 3 à partir de quelle semaine
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

# 4 copier
git_calendar_exists = os.path.isdir(gitcours_path + year)
if git_calendar_exists:
    if start_week < 30:
        weeks_first_year = range(0, 0)
        weeks_second_year = range(start_week, 31)
    else:
        weeks_first_year = range(start_week, 53)
        weeks_second_year = range(0, 30)

    # vider le dossier
    for period in range(1, 6):
        for week in range(1, 53):
            if week in weeks_first_year or week in weeks_second_year:
                try:
                    file = gitcours_path + year + \
                        "/periode_{}/semaine_{}.md".format(period, week)
                    os.remove(file)
                    color.print_color(f"Deleted : {file}", "white")
                except OSError:
                    pass
    # copier si ça n'existe pas

src = calendar_path + year
dst = gitcours_path + year

lst = distutils.dir_util.copy_tree(src, dst, update=1)
for file in lst:
    color.print_color(f"Copied : {file}", "white")

color.print_color(success_msg, "cyan")
print()
# 5 gitadd

is_gitadd_msg = "Do you want to push this calendar to git_cours ? [yes/NO] "
gitadd_cmd = '/home/quentin/scripts/gitadd.sh'
gitadd_succes_msg = 'files pushed to git_cours : https://github.com/qkzk/cours/tree/master/{}'
is_gitadd = input(color.format_color(is_gitadd_msg, "yellow"))
print(is_gitadd)

if is_gitadd in 'yesYES':
    print("pushing to git_cours...")
    subprocess.call(gitadd_cmd, shell=True)
    color.print_color(gitadd_succes_msg.format(year), "cyan")
