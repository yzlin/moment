#!/usr/bin/env python

from unittest import TestCase, main
from datetime import datetime
import pytz
import moment


class SimpleAPI(TestCase):

    def test_date_function_takes_a_string(self):
        d = moment.date("December 18, 2012", "MMMM D, YYYY")
        self.assertEquals(d, datetime(2012, 12, 18))

    def test_date_function_with_datetime(self):
        d = moment.date(datetime(2012, 12, 18))
        self.assertEquals(d, datetime(2012, 12, 18))

    def test_date_function_with_iterable(self):
        d = moment.date((2012, 12, 18))
        self.assertEquals(d, datetime(2012, 12, 18))

    def test_date_function_with_args(self):
        d = moment.date(2012, 12, 18)
        self.assertEquals(d, datetime(2012, 12, 18))

    def test_date_function_with_string(self):
        d = moment.date("2012-12-18")
        self.assertEquals(d, datetime(2012, 12, 18))

    def test_date_function_with_unicode(self):
        d = moment.date(u"2012-12-18")
        self.assertEquals(d, datetime(2012, 12, 18))

    def test_utc_function_with_args(self):
        d = moment.utc(2012, 12, 18)
        self.assertEquals(d, datetime(2012, 12, 18, tzinfo=pytz.utc))

    def test_now_function_with_current_date(self):
        d = moment.now().date
        now = datetime.now()
        self.assertEquals(d.year, now.year)
        self.assertEquals(d.month, now.month)
        self.assertEquals(d.day, now.day)
        self.assertEquals(d.hour, now.hour)
        self.assertEquals(d.second, now.second)

    def test_utcnow_function(self):
        d = moment.utcnow()
        now = datetime.utcnow()
        self.assertEquals(d.year, now.year)
        self.assertEquals(d.month, now.month)
        self.assertEquals(d.day, now.day)
        self.assertEquals(d.hour, now.hour)
        self.assertEquals(d.second, now.second)

    def test_moment_can_transfer_between_datetime_and_moment(self):
        d = moment.now().date
        self.assertEquals(d, moment.date(d).date)

    def test_moment_unix_command(self):
        d = moment.unix(1355788800000, utc=True)
        expected = moment.date((2012, 12, 18))
        self.assertEquals(d, expected)

    def test_moment_can_subtract_another_moment(self):
        d = moment.date((2012, 12, 19))
        self.assertTrue(d - moment.date((2012, 12, 18)))

    def test_moment_can_subtract_a_datetime(self):
        d = moment.date((2012, 12, 19))
        self.assertTrue(d - datetime(2012, 12, 18))

    def test_a_datetime_can_subtract_a_moment(self):
        d = moment.date((2012, 12, 18))
        self.assertTrue(datetime(2012, 12, 19) - d)

    def test_date_property(self):
        d = moment.date(2012, 12, 18).date
        self.assertEquals(d, datetime(2012, 12, 18))

    def test_zero_property(self):
        d = moment.date(2012, 12, 18, 1, 2, 3)
        self.assertEquals(d.zero.date, datetime(2012, 12, 18))


class Replacement(TestCase):

    def test_simple_chaining_commands(self):
        d = moment.date([2012, 12, 18])
        expecting = moment.date((2012, 12, 18, 1, 2, 3)).done()
        d.replace(hours=1, minutes=2, seconds=3)
        self.assertEqual(d, expecting)

    def test_chaining_with_format(self):
        d = moment.utc((2012, 12, 18))
        d.replace(hours=1).add(minutes=2).replace(seconds=3)
        expecting = "2012-12-18 01:02:03"
        self.assertEquals(d.format('YYYY-MM-DD hh:mm:ss'), expecting)

    def test_properties_after_chaining(self):
        d = moment.now().replace(years=1984, months=1, days=1)
        self.assertEquals(d.year, 1984)

    def test_add_with_keywords(self):
        d = moment.date((2012, 12, 19))
        d.add(hours=1, minutes=2, seconds=3)
        expecting = moment.date((2012, 12, 19, 1, 2, 3))
        self.assertEquals(d, expecting)

    def test_subtract_with_keywords(self):
        d = moment.date((2012, 12, 19, 1, 2, 3))
        d.subtract(hours=1, minutes=2, seconds=3)
        expecting = moment.date((2012, 12, 19))
        self.assertEquals(d, expecting)

    def test_chaining_with_replace_method(self):
        d = moment.date((2012, 12, 19))
        d.replace(hours=1, minutes=2, seconds=3)
        expecting = moment.date((2012, 12, 19, 1, 2, 3))
        self.assertEquals(d, expecting)


class Weekdays(TestCase):

    def test_weekdays_can_be_manipulated(self):
        d = moment.date([2012, 12, 19])
        yesterday = moment.date([2012, 12, 18])
        self.assertEquals(d.date.isoweekday(), 3)
        self.assertEquals(d.replace(weekday=3), d)
        self.assertEquals(d.replace(weekday=2).done(), yesterday.done())

    def test_week_addition_equals_weekday_manipulation(self):
        d = moment.date([2012, 12, 19])
        upcoming = d.clone().add('weeks', 1)
        expecting = moment.date([2012, 12, 26]).date
        self.assertEquals(upcoming, expecting)
        self.assertEquals(d.replace(weekday=10), upcoming)

    def test_weekdays_with_zeros(self):
        d = moment.date([2012, 12, 19])
        sunday = moment.date([2012, 12, 16])
        self.assertEquals(d.replace(weekday=0), sunday)

    def test_weekdays_with_negative_numbers(self):
        d = moment.date((2012, 12, 19))
        expecting = moment.date([2012, 12, 9]).date
        self.assertEquals(d.replace(weekday=-7), expecting)

    def test_weekdays_with_larger_number_into_new_year(self):
        d = moment.date((2012, 12, 19))
        expecting = moment.date('2013-01-09').date
        self.assertEquals(d.replace(weekday=24).date, expecting)

class StartEndOfUnit(TestCase):

    def test_start_of_year(self):
        d = moment.date(2015, 8, 25)
        expecting = moment.date(2015, 1, 1)
        self.assertEquals(d.start_of('year'), expecting)
        self.assertEquals(d.start_of('years'), expecting)

    def test_start_of_quarter(self):
        expecting = moment.date(2015, 1, 1)
        d = moment.date(2015, 1, 25)
        self.assertEquals(d.start_of('quarter'), expecting)
        self.assertEquals(d.start_of('quarters'), expecting)
        d = moment.date(2015, 2, 25)
        self.assertEquals(d.start_of('quarter'), expecting)
        self.assertEquals(d.start_of('quarters'), expecting)
        d = moment.date(2015, 3, 25)
        self.assertEquals(d.start_of('quarter'), expecting)
        self.assertEquals(d.start_of('quarters'), expecting)

        expecting = moment.date(2015, 4, 1)
        d = moment.date(2015, 4, 25)
        self.assertEquals(d.start_of('quarter'), expecting)
        self.assertEquals(d.start_of('quarters'), expecting)
        d = moment.date(2015, 5, 25)
        self.assertEquals(d.start_of('quarter'), expecting)
        self.assertEquals(d.start_of('quarters'), expecting)
        d = moment.date(2015, 6, 25)
        self.assertEquals(d.start_of('quarter'), expecting)
        self.assertEquals(d.start_of('quarters'), expecting)

        expecting = moment.date(2015, 7, 1)
        d = moment.date(2015, 7, 25)
        self.assertEquals(d.start_of('quarter'), expecting)
        self.assertEquals(d.start_of('quarters'), expecting)
        d = moment.date(2015, 8, 25)
        self.assertEquals(d.start_of('quarter'), expecting)
        self.assertEquals(d.start_of('quarters'), expecting)
        d = moment.date(2015, 9, 25)
        self.assertEquals(d.start_of('quarter'), expecting)
        self.assertEquals(d.start_of('quarters'), expecting)

        expecting = moment.date(2015, 10, 1)
        d = moment.date(2015, 10, 25)
        self.assertEquals(d.start_of('quarter'), expecting)
        self.assertEquals(d.start_of('quarters'), expecting)
        d = moment.date(2015, 11, 25)
        self.assertEquals(d.start_of('quarter'), expecting)
        self.assertEquals(d.start_of('quarters'), expecting)
        d = moment.date(2015, 12, 25)
        self.assertEquals(d.start_of('quarter'), expecting)
        self.assertEquals(d.start_of('quarters'), expecting)

    def test_start_of_month(self):
        d = moment.date(2015, 8, 25)
        expecting = moment.date(2015, 8, 1)
        self.assertEquals(d.start_of('month'), expecting)
        self.assertEquals(d.start_of('months'), expecting)

    def test_start_of_day(self):
        d = moment.date(2015, 8, 25, 12)
        expecting = moment.date(2015, 8, 25, 0)
        self.assertEquals(d.start_of('day'), expecting)
        self.assertEquals(d.start_of('days'), expecting)

    def test_start_of_hour(self):
        d = moment.date(2015, 8, 25, 12, 33)
        expecting = moment.date(2015, 8, 25, 12, 0)
        self.assertEquals(d.start_of('hour'), expecting)
        self.assertEquals(d.start_of('hours'), expecting)

    def test_start_of_minute(self):
        d = moment.date(2015, 8, 25, 12, 33, 49)
        expecting = moment.date(2015, 8, 25, 12, 33, 0)
        self.assertEquals(d.start_of('minute'), expecting)
        self.assertEquals(d.start_of('minutes'), expecting)

    def test_start_of_second(self):
        d = moment.date(2015, 8, 25, 12, 33, 49, 123456)
        expecting = moment.date(2015, 8, 25, 12, 33, 49, 0)
        self.assertEquals(d.start_of('second'), expecting)
        self.assertEquals(d.start_of('seconds'), expecting)

    def test_end_of_year(self):
        d = moment.date(2015, 8, 25)
        expecting = moment.date(2015, 12, 31, 23, 59, 59, 999999)
        self.assertEquals(d.end_of('year'), expecting)
        self.assertEquals(d.end_of('years'), expecting)

    def test_end_of_quarter(self):
        expecting = moment.date(2015, 3, 31, 23, 59, 59, 999999)
        d = moment.date(2015, 1, 25)
        self.assertEquals(d.end_of('quarter').date, expecting.date)
        self.assertEquals(d.end_of('quarters'), expecting)
        d = moment.date(2015, 2, 25)
        self.assertEquals(d.end_of('quarter'), expecting)
        self.assertEquals(d.end_of('quarters'), expecting)
        d = moment.date(2015, 3, 25)
        self.assertEquals(d.end_of('quarter'), expecting)
        self.assertEquals(d.end_of('quarters'), expecting)

        expecting = moment.date(2015, 6, 30, 23, 59, 59, 999999)
        d = moment.date(2015, 4, 25)
        self.assertEquals(d.end_of('quarter'), expecting)
        self.assertEquals(d.end_of('quarters'), expecting)
        d = moment.date(2015, 5, 25)
        self.assertEquals(d.end_of('quarter'), expecting)
        self.assertEquals(d.end_of('quarters'), expecting)
        d = moment.date(2015, 6, 25)
        self.assertEquals(d.end_of('quarter'), expecting)
        self.assertEquals(d.end_of('quarters'), expecting)

        expecting = moment.date(2015, 9, 30, 23, 59, 59, 999999)
        d = moment.date(2015, 7, 25)
        self.assertEquals(d.end_of('quarter'), expecting)
        self.assertEquals(d.end_of('quarters'), expecting)
        d = moment.date(2015, 8, 25)
        self.assertEquals(d.end_of('quarter'), expecting)
        self.assertEquals(d.end_of('quarters'), expecting)
        d = moment.date(2015, 9, 25)
        self.assertEquals(d.end_of('quarter'), expecting)
        self.assertEquals(d.end_of('quarters'), expecting)

        expecting = moment.date(2015, 12, 31, 23, 59, 59, 999999)
        d = moment.date(2015, 10, 25)
        self.assertEquals(d.end_of('quarter'), expecting)
        self.assertEquals(d.end_of('quarters'), expecting)
        d = moment.date(2015, 11, 25)
        self.assertEquals(d.end_of('quarter'), expecting)
        self.assertEquals(d.end_of('quarters'), expecting)
        d = moment.date(2015, 12, 25)
        self.assertEquals(d.end_of('quarter'), expecting)
        self.assertEquals(d.end_of('quarters'), expecting)

    def test_end_of_month(self):
        d = moment.date(2015, 8, 25)
        expecting = moment.date(2015, 8, 31, 23, 59, 59, 999999)
        self.assertEquals(d.end_of('month'), expecting)
        self.assertEquals(d.end_of('months'), expecting)

    def test_end_of_day(self):
        d = moment.date(2015, 8, 25, 12)
        expecting = moment.date(2015, 8, 25, 23, 59, 59, 999999)
        self.assertEquals(d.end_of('day'), expecting)
        self.assertEquals(d.end_of('days'), expecting)

    def test_end_of_hour(self):
        d = moment.date(2015, 8, 25, 12, 33)
        expecting = moment.date(2015, 8, 25, 12, 59, 59, 999999)
        self.assertEquals(d.end_of('hour'), expecting)
        self.assertEquals(d.end_of('hours'), expecting)

    def test_end_of_minute(self):
        d = moment.date(2015, 8, 25, 12, 33, 49)
        expecting = moment.date(2015, 8, 25, 12, 33, 59, 999999)
        self.assertEquals(d.end_of('minute'), expecting)
        self.assertEquals(d.end_of('minutes'), expecting)

    def test_end_of_second(self):
        d = moment.date(2015, 8, 25, 12, 33, 49, 123456)
        expecting = moment.date(2015, 8, 25, 12, 33, 49, 999999)
        self.assertEquals(d.end_of('second'), expecting)
        self.assertEquals(d.end_of('seconds'), expecting)

if __name__ == '__main__':
    main()
