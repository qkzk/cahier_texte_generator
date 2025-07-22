"""
User data for the next run.

Edit this file directly.
Since you should use this script once a year, it's not a big deal.
"""

"""Write the year you wish to create. Use 2024 for 2024-2025."""
year = 2025
"""Write a valid week number to edit files after this week."""
start_week = None
"""Period numbers, should be 1, 2, 3, 4, 5 in most case."""
list_periods = range(1, 6)
"""End of each period. Use the first day of the week."""
dict_period_ends = {
    0: "29/08/2025",  # prerentrée
    1: "03/11/2025",  # rentrée vacances Toussaint
    2: "05/01/2026",  # rentrée vacances Noël
    3: "02/03/2026",  # rentrée vacances d'hiver
    4: "27/04/2026",  # rentrée vacances Printemps
    5: "04/07/2026",  # fin d'année scolaire
}

# Clear the content
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
"""

# mercredi
content_per_day[
    2
] = """
"""

# jeudi
content_per_day[
    3
] = """
"""

# vendredi
content_per_day[
    4
] = """
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
