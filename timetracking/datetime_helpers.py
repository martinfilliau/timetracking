def calculate_time(event):
    """Get timedelta from event, based on start/end date
    """
    start = event['DTSTART'].dt
    end = event['DTEND'].dt
    return end - start


def within(event, from_date, to_date):
    """Check if given vEvent is between two datetimes
    :param event: vEvent (iCal)
    :param from_date: date start
    :param to_date: date end
    :return True if vEvent is between the two dates else False
    """
    return from_date < event['DTSTART'].dt < to_date
