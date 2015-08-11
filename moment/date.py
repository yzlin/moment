"""
Where the magic happens.
"""

import calendar
from datetime import datetime, timedelta

from .utils import switch, case


def add_month(date, number):
    """Add a number of months to a date."""
    month = date.month - 1 + number
    return update_month(date, month)


def subtract_month(date, number):
    """Subtract a number of months from a date."""
    month = date.month - 1 - number
    return update_month(date, month)


def update_month(date, month):
    """Create a new date with a modified number of months."""
    year = date.year + month / 12
    month = month % 12 + 1
    day = min(date.day, calendar.monthrange(year, month)[1])
    return date.replace(year=year, month=month, day=day)


class MutableDate(object):
    """Incapsulate mutable dates in one class."""

    def __init__(self, date):
        super(MutableDate, self).__init__()
        self._date = date

    def add(self, unit=None, amount=None, **kwargs):
        """Add time to the original moment."""
        if not unit and not amount and len(kwargs):
            for k, v in kwargs.iteritems():
                self.add(k, v)
        if unit in ('years', 'year'):
            self._date = add_month(self._date, amount * 12)
        elif unit in ('quarters', 'quarter'):
            self._date = add_month(self._date, amount * 3)
        elif unit in ('months', 'month'):
            self._date = add_month(self._date, amount)
        elif unit in ('weeks', 'week'):
            self._date += timedelta(weeks=amount)
        elif unit in ('days', 'day'):
            self._date += timedelta(days=amount)
        elif unit in ('hours', 'hour'):
            self._date += timedelta(hours=amount)
        elif unit in ('minutes', 'minute'):
            self._date += timedelta(minutes=amount)
        elif unit in ('seconds', 'second'):
            self._date += timedelta(seconds=amount)
        elif unit in ('milliseconds', 'millisecond'):
            self._date += timedelta(milliseconds=amount)
        elif unit in ('microseconds', 'microsecond'):
            self._date += timedelta(microseconds=amount)

        return self

    def sub(self, unit=None, amount=None, **kwargs):
        """Just in case."""
        return self.subtract(unit, amount, **kwargs)

    def subtract(self, unit=None, amount=None, **kwargs):
        """Subtract time from the original moment."""
        if not unit and not amount and len(kwargs):
            for k, v in kwargs.iteritems():
                self.subtract(k, v)
        if unit in ('years', 'year'):
            self._date = subtract_month(self._date, amount * 12)
        elif unit in ('quarters', 'quarter'):
            self._date = subtract_month(self._date, amount * 3)
        elif unit in ('months', 'month'):
            self._date = subtract_month(self._date, amount)
        elif unit in ('weeks', 'week'):
            self._date -= timedelta(weeks=amount)
        elif unit in ('days', 'day'):
            self._date -= timedelta(days=amount)
        elif unit in ('hours', 'hour'):
            self._date -= timedelta(hours=amount)
        elif unit in ('minutes', 'minute'):
            self._date -= timedelta(minutes=amount)
        elif unit in ('seconds', 'second'):
            self._date -= timedelta(seconds=amount)
        elif unit in ('milliseconds', 'millisecond'):
            self._date -= timedelta(milliseconds=amount)
        elif unit in ('microseconds', 'microsecond'):
            self._date -= timedelta(microseconds=amount)

        return self

    def start_of(self, unit):
        while switch(unit):
            if case('years', 'year'):
                self._date = self._date.replace(month=1)
            if case('quarters', 'quarter', 'months', 'month'):
                self._date = self._date.replace(day=1)
            if case('weeks', 'week', 'days', 'day'):
                self._date = self._date.replace(hour=0)
            if case('hours', 'hour'):
                self._date = self._date.replace(minute=0)
            if case('minutes', 'minute'):
                self._date = self._date.replace(second=0)
            if case('seconds', 'second'):
                self._date = self._date.replace(microsecond=0)
                break

            break

        if unit in ('weeks', 'week'):
            self._weekday(0)

        if unit in ('quarters', 'quarter'):
            self._date = self._date.replace(month=(self._date.month - 1) / 3 * 3 + 1)

        return self

    def end_of(self, unit):
        if unit in ('microseconds', 'microsecond'):
            return self

        return self.start_of(unit).add(unit=unit, amount=1).subtract(microsecond=1)

    def replace(self, **kwargs):
        """A Pythonic way to replace various date attributes."""
        for unit, value in kwargs.iteritems():
            if unit in ('years', 'year'):
                self._date = self._date.replace(year=value)
            elif unit in ('months', 'month'):
                self._date = self._date.replace(month=value)
            elif unit in ('days', 'day'):
                self._date = self._date.replace(day=value)
            elif unit in ('hours', 'hour'):
                self._date = self._date.replace(hour=value)
            elif unit in ('minutes', 'minute'):
                self._date = self._date.replace(minute=value)
            elif unit in ('seconds', 'second'):
                self._date = self._date.replace(second=value)
            elif unit in ('microseconds', 'microsecond'):
                self._date = self._date.replace(microsecond=value)
            elif unit == 'weekday':
                self._weekday(value)

        return self

    def epoch(self, rounding=True, milliseconds=False):
        """Milliseconds since epoch."""
        zero = datetime.utcfromtimestamp(0)
        delta = self._date - zero
        seconds = delta.total_seconds()
        if rounding:
            seconds = round(seconds)
        if milliseconds:
            seconds *= 1000
        return seconds

    def _weekday(self, number):
        """Mutate the original moment by changing the day of the week."""
        weekday = self._date.isoweekday()
        if number < 0:
            days = abs(weekday - number)
        else:
            days = weekday - number
        delta = self._date - timedelta(days)
        self._date = delta
        return self

    def isoformat(self):
        """Return the date's ISO 8601 string."""
        return self._date.isoformat()

    @property
    def zero(self):
        """Get rid of hour, minute, second, and microsecond information."""
        self.replace(hours=0, minutes=0, seconds=0, microseconds=0)
        return self

    @property
    def datetime(self):
        """Return the mutable date's inner datetime format."""
        return self._date

    @property
    def date(self):
        """Access the internal datetime variable."""
        return self._date

    @property
    def year(self):
        return self._date.year

    @property
    def month(self):
        return self._date.month

    @property
    def day(self):
        return self._date.day

    @property
    def weekday(self):
        return self._date.isoweekday()

    @property
    def hour(self):
        return self._date.hour

    @property
    def hours(self):
        return self._date.hour

    @property
    def minute(self):
        return self._date.minute

    @property
    def minutes(self):
        return self._date.minute

    @property
    def second(self):
        return self._date.second

    @property
    def seconds(self):
        return self._date.second

    @property
    def microsecond(self):
        return self._date.microsecond

    @property
    def microseconds(self):
        return self._date.microsecond

    @property
    def tzinfo(self):
        return self._date.tzinfo

    def __sub__(self, other):
        if isinstance(other, datetime):
            return self._date - other
        elif isinstance(other, type(self)):
            return self._date - other.date

    def __rsub__(self, other):
        return self.__sub__(other)

    def __lt__(self, other):
        if isinstance(other, datetime):
            return self._date < other
        elif isinstance(other, type(self)):
            return self._date < other.date

    def __le__(self, other):
        if isinstance(other, datetime):
            return self._date <= other
        elif isinstance(other, type(self)):
            return self._date <= other.date

    def __eq__(self, other):
        if isinstance(other, datetime):
            return self._date == other
        elif isinstance(other, type(self)):
            return self._date == other.date

    def __ne__(self, other):
        if isinstance(other, datetime):
            return self._date != other
        elif isinstance(other, type(self)):
            return self._date != other.date

    def __gt__(self, other):
        if isinstance(other, datetime):
            return self._date > other
        elif isinstance(other, type(self)):
            return self._date > other.date

    def __ge__(self, other):
        if isinstance(other, datetime):
            return self._date >= other
        elif isinstance(other, type(self)):
            return self._date >= other.date
