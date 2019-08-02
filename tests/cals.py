#!/usr/bin/env python
# -*- coding: utf-8 -*-

# import calendar
#
# hc = calendar.HTMLCalendar()
#
# str = hc.formatmonth(2025, 1)
# print(str)

# from IPython.display import HTML


# class EventsCalendar(HTMLCalendar):
#     def formatday(self, day, weekday):
#         """
#           Return a day as a table cell.
#         """
#         if day == 0:
#             return '<td class="noday">&nbsp;</td>'  # day outside month
#         else:
#             return '<td class="%s"><a href="%s/%s/%d">%d</a></td>' % (self.cssclasses[weekday], '2019', 'dec', day, day)
import calendar
from calendar import HTMLCalendar


class EventsCalendar(HTMLCalendar):
    def __init__(self, year, month, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.month = str(month)
        self.year = str(year)

    def formatday(self, day, weekday):
        """
          Return a day as a table cell.
        """
        if day == 0:
            return '<td class="noday">&nbsp;</td>'  # day outside month
        else:
            return '<td class="{0}"><a href="{1}/{2}/{3}">{4}</a></td>'.format(
                self.cssclasses[weekday], self.year, self.month, day, day
            )


str = EventsCalendar(2019, 11).formatmonth(2019, 11)
print(str)


# Based on https://stackoverflow.com/a/1458077/1639671
# intended for use in a Jupyter Notebook or similar.


# class HighlightedCalendar(HTMLCalendar):
#     def __init__(self, highlight=[], *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self._highlight = highlight
#
#     def formatday(self, day, weekday):
#         """
#         Return a day as a table cell.
#         """
#         if day in self._highlight:
#             return '<td class="%s" bgcolor="pink">%d</td>' % (self.cssclasses[weekday], day)
#         else:
#             return super().formatday(day, weekday)


# highlight = range(1, 7)
#
# str = HighlightedCalendar(highlight=highlight).formatmonth(2019, 11)
# print(str)


if __name__ == '__main__':
    # main()
    1
