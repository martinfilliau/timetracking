import unittest
from datetime import datetime, timedelta

from timetracking.datetime_helpers import within, calculate_time


class TimetrackingTest(unittest.TestCase):

    def test_cal_to_structure(self):
        pass


class DateTimeHelpersTest(unittest.TestCase):

    def test_within_true(self):
        from_date = datetime(2014, 01, 01)
        to_date = datetime(2014, 06, 01)
        test_date = datetime(2014, 03, 01)
        value = within(test_date, from_date, to_date)
        self.assertEquals(value, True)

    def test_within_false(self):
        from_date = datetime(2014, 01, 01)
        to_date = datetime(2014, 06, 01)
        test_date = datetime(2014, 07, 01)
        value = within(test_date, from_date, to_date)
        self.assertEquals(value, False)

    def test_within_edge(self):
        from_date = datetime(2014, 01, 01)
        to_date = datetime(2014, 06, 01)
        test_date = datetime(2014, 06, 01)
        value = within(test_date, from_date, to_date)
        self.assertEquals(value, False)

    def test_calculate_time(self):
        start = datetime(2014, 01, 01)
        end = datetime(2014, 02, 01)
        delta = timedelta(days=31)
        value = calculate_time(start, end)
        self.assertEquals(value, delta)


if __name__ == "__main__":
    unittest.main()
