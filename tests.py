import unittest
from datetime import datetime, timedelta

from timetracking.datetime_helpers import within, calculate_time


class TimetrackingTest(unittest.TestCase):

    def test_cal_to_structure(self):
        pass


class DateTimeHelpersTest(unittest.TestCase):

    def test_within_true(self):
        from_date = datetime(2014, 1, 1)
        to_date = datetime(2014, 6, 1)
        test_date = datetime(2014, 3, 1)
        value = within(test_date, from_date, to_date)
        self.assertEquals(value, True)

    def test_within_false(self):
        from_date = datetime(2014, 1, 1)
        to_date = datetime(2014, 6, 1)
        test_date = datetime(2014, 7, 1)
        value = within(test_date, from_date, to_date)
        self.assertEquals(value, False)

    def test_within_edge(self):
        from_date = datetime(2014, 1, 1)
        to_date = datetime(2014, 6, 1)
        test_date = datetime(2014, 6, 1)
        value = within(test_date, from_date, to_date)
        self.assertEquals(value, False)

    def test_calculate_time(self):
        start = datetime(2014, 1, 1)
        end = datetime(2014, 2, 1)
        delta = timedelta(days=31)
        value = calculate_time(start, end)
        self.assertEquals(value, delta)


if __name__ == "__main__":
    unittest.main()
