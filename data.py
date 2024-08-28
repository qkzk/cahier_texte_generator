# TODO faire de ce fichier de code un fichier de texte facilement éditable et compréhensible de tous.

year = 2020
start_week = None
list_periods = range(1, 6)
dict_period_ends = {
    0: "31/08/2024",  # prerentrée
    1: "07/11/2024",  # rentrée vacances Toussaint
    2: "02/01/2025",  # rentrée vacances Noël
    3: "27/02/2025",  # rentrée vacances d'hiver
    4: "01/05/2025",  # rentrée vacances Printemps
    5: "08/07/2025",  # fin d'année scolaire
}

"""
content_per_day = {
    0: "\n* 8h-8h55 - s213\n* 8h55-9h50 - s215\n* 10h-10h55 - s104\n",
    1: "\n* 8h-8h55 - s213\n* 8h55-9h50 - s215\n* 10h-10h55 - s104\n",
    2: "\n* 8h-8h55 - s213\n* 8h55-9h50 - s215\n* 10h-10h55 - s104\n",
    3: "\n* 8h-8h55 - s213\n* 8h55-9h50 - s215\n* 10h-10h55 - s104\n",
    4: "\n* 8h-8h55 - s213\n* 8h55-9h50 - s215\n* 10h-10h55 - s104\n",
    5: "\n",
    6: "\n",
}

"""

content_per_day = {}

# lundi
content_per_day[
    0
] = """
"""

# mardi
content_per_day[
    1
] = """
* 6h40-7h14 - gare - train
* 8h-9h50 - 213 - tale NSI
* 10h00-10h55 - 213 - tmg2-1
* 11h15-11h47 - gare - train
"""

# mercredi
content_per_day[
    2
] = """
* 6h40-7h14 - gare - train
* 8h-8h55 - 213 - tale NSI-1
* 8h55-9h50 - 213 - tale NSI-2
* 10h00-11h50 - 213 - 1ere NSI
* 12h15-12h47 - gare - train
"""

# jeudi
content_per_day[
    3
] = """
* 8h40-9h14 - gare - train
* 10h-11h50 - 213 - TMG2
* 12h45-13h40 - 213 - tale NSI
* 13h40-15h40 - 213 - tale NSI-1
* 15h40-17h30 - 213 - tale NSI-2
* 17h46-18h20 - gare -train
"""

# vendredi
content_per_day[
    4
] = """
* 7h40-8h14 - gare - train
* 8h55-9h50 - 213 - tmg2-2
* 11h50-12h45 - 213 - tg9 AP Q2
* 13h40-15h30 - 213 - 1ere NSI 1
* 15h40-17h30 - 213 - 1ere NSI 2
* 17h46-18h20 - gare -train
"""

# samedi
content_per_day[
    5
] = """
"""

# dimanche
content_per_day[
    6
] = """
"""
