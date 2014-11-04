"""Helpers to manipulate datetime objects
"""


def calculate_time(start, end):
    """Get timedelta from event, based on start/end date
    """
    return end - start


def within(test_date, from_date, to_date):
    """Check if given vEvent is between two datetimes
    :param test_date: vEvent (iCal)
    :param from_date: date start
    :param to_date: date end
    :return True if vEvent is between the two dates else False
    """
    return from_date < test_date < to_date
