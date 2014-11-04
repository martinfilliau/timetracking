"""Format "things" to strings
"""

from datetime import datetime


def format_timedelta(delta):
    """Format a timedelta object for human reading
    (Only handles hours/minutes for now)
    """
    seconds = delta.total_seconds()
    hours, remainder = divmod(seconds, 3600)
    minutes = remainder // 60
    if minutes == 0:
        return "{hours} h".format(hours=int(hours))
    else:
        return "{hours} h {minutes} m".format(hours=int(hours),
                                              minutes=int(minutes))


def date_from_string(date_string):
    """Date from string (input)
    :param date_string: date as string
    :return datetime object
    """
    return datetime.strptime(date_string, '%d/%m/%Y')
