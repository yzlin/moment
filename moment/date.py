"""
Where the magic happens.
"""

from datetime import  datetime


class MutableDate(object):
    """Incapsulate mutable dates in one class."""

    def __init__(self, date):
        self._date = date

    def epoch(self):
        """Milliseconds since epoch."""
        return self

    def year(self, number):
        return self

    def month(self, number):
        return self

    def date(self, number):
        """Mutate the original moment by changing the day of the month."""
        return self

    def weekday(self, number):
        """Mutate the original moment by changing the day of the week."""
        return self

    def hours(self, amount):
        return self

    def minutes(self, amount):
        return self

    def seconds(self, amount):
        return self

    def milliseconds(self, amount):
        """Add milliseconds to the original moment."""
        return self

    def datetime(self):
        """Return the mutable date's inner datetime format."""
        return self._date

    def to_date(self):
        """Return the mutable date's inner datetime format."""
        return self._date